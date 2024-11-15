#!/usr/bin/python

import datetime
import subprocess
import glob
import os
import sys
import netCDF4
from PIL import ImageOps
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
import numpy as np
import matplotlib as mpl
mpl.use('Agg')


def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0, 1, 256)
    if position == None:
        position = np.linspace(0, 1, len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red': [], 'green': [], 'blue': []}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
    return cmap


if __name__ == '__main__':

    os.chdir('/work/NSIDC_Ice')

    figxsize = 10
    figysize = 10
    framestat = 'False'

    imgDate = sys.argv[1]  # Expects integer year and month (e.g., 201401)
    yyyy = imgDate[0:4]
    mm = imgDate[4:6]

    imgsiz = sys.argv[2]  # Expects small, large, broadcast, diy

    if(imgsiz == 'small'):
        imgdir = '/work/NSIDC_Ice/Images/01-small/'
        imsuf = 'small'
    if(imgsiz == 'large'):
        imgdir = '/work/NSIDC_Ice/Images/02-large/'
        imsuf = 'large'
    if(imgsiz == 'broadcast'):
        imgdir = '/work/NSIDC_Ice/Images/03-broadcast/'
        imsuf = 'broadcast'
    if(imgsiz == 'diy'):
        imgdir = '/work/NSIDC_Ice/Images/04-full_res_zips/'
        imsuf = 'fullres'

    infile = glob.glob('/work/NSIDC_Ice/Data/*'+yyyy+'*')[0]

    # Load data
    dataset = netCDF4.Dataset(infile, 'r')

    # Extract variables & close the file
    time = dataset.variables['time'][:]
    lons = dataset.variables['longitude'][:, :]
    lats = dataset.variables['latitude'][:, :]
    alldata = dataset.variables['age_of_sea_ice'][:, :, :]
    dataset.close()

    # Get the time variable into actual dates
    timeOrigin = datetime.date(1970, 1, 1)
    yyyymmdd = []
    dyyyy = []
    months = []
    days = []
    for i in range(len(time)):
        thisDate = timeOrigin + datetime.timedelta(days=time[i])
        yyyymmdd.append(thisDate.strftime('%Y%m%d'))
        dyyyy.append(thisDate.strftime('%Y'))
        months.append(thisDate.strftime('%m'))
        days.append(thisDate.strftime('%d'))

    ndx = []
    for i in range(len(months)):
        if(months[i] == mm and dyyyy[i] == yyyy):
            ndx.append(i)

    if(len(ndx) == 0):
        print(' ')
        print('Sorry, data are not available for '+yyyy+'-'+mm)
        sys.exit()

    for d in range(len(ndx)):
        timeIndx = ndx[d]

        data = alldata[timeIndx, :, :]

        outpng = imgdir+'IceSnow--Weekly--Sea-Ice-Age--Arctic--'+yyyy + \
            '-'+months[timeIndx]+'-'+days[timeIndx]+'--'+imsuf+'.png'

        # Set the upper values to zero
        data[data >= 20] = 0

        fig = plt.figure(figsize=(figxsize, figysize))
        ax1 = fig.add_axes([0.0, 0.0, 1.0, 1.0],
                           frameon=False, facecolor='#F5F5F5')

        m = Basemap(llcrnrlon=-45.0, llcrnrlat=29.71270, urcrnrlon=135.0,
                    urcrnrlat=29.71270, resolution='i', area_thresh=1000., epsg=3408)
        m.fillcontinents(color='#808080', lake_color='#808080', zorder=9)
        m.drawcoastlines(color='#333333', linewidth=0.5, zorder=10)
        m.drawrivers(color='#808080', linewidth=1, zorder=10)
        m.drawcountries(color='#333333', linewidth=0.35, zorder=10)
        # m.readshapefile('./Shapefiles/ne_50m_admin_0_countries_lakes', 'countries', color='#333333', linewidth=0.5, zorder=10)

        levs = [0, 1, 2, 3, 4, 5, 6]
        colors = [(80, 80, 80), (40, 59, 79), (23, 81, 149),
                  (43, 140, 190), (123, 204, 196), (255, 255, 255)]
        my_cmap = make_cmap(colors, bit=True)
        bounds = [0, 1, 2, 3, 4, 5, 6]
        norm = mpl.colors.BoundaryNorm(bounds, my_cmap.N)

        m.imshow(data, cmap=my_cmap, norm=norm,
                 interpolation='nearest', ax=ax1, zorder=8)

        plt.savefig('tmp.png', dpi=300, orientation='landscape',
                    bbox_inches='tight', pad_inches=0.0)

        img = Image.open('tmp.png')
        # img1.rotate(90).save('tmp.png')
        img.rotate(95).save('tmp.png')

        img1 = Image.open('tmp.png')
        img1 = ImageOps.crop(img1, 475)  # was 410
        img1 = ImageOps.fit(img1, (2405, 1600),
                            centering=(0.0, 0.5))  # was 2545,1695

        img1.save('tmp.png')

        print('Creating: '+outpng)

        if(imgsiz == 'small'):
            logo_im = Image.open('./noaa_logo_ice_42.png')
            logo_x = 620 - logo_im.size[0]
            logo_y = 400 - logo_im.size[1]

            img2 = Image.open('tmp.png')
            img2 = img2.resize((620, 400), Image.ANTIALIAS)

            fnt = ImageFont.truetype('./Fonts/Trebuchet_MS_Bold.ttf', 12)
            draw = ImageDraw.Draw(img2)
            draw.text((50, 325), "Alaska", font=fnt, color='#FFFFFF')
            draw.text((410, 275), "Greenland", font=fnt, color='#FFFFFF')
            draw.text((65, 32), "Russia", font=fnt, color='#FFFFFF')

            # draw.text((580,210), "open", font=fnt, color='#FFFFFF')
            # draw.text((580,223), "water", font=fnt, color='#FFFFFF')

            img2.paste(logo_im, (logo_x, logo_y))

            imgday = yyyy+months[timeIndx]+days[timeIndx]
            cmd = "python ./IceAgeColorbar.py "+imgday+" "+imgsiz
            subprocess.call(cmd, shell=True)

            img3 = Image.open('temporary_cbar.png')

            img4 = Image.new('RGBA', size=(
                img2.size[0], img2.size[1]+img3.size[1]))
            img4.paste(img3, (0, img2.size[1]))
            img4.paste(img2, (0, 0))

            img4.save(outpng)

            img.close()
            img1.close()
            img2.close()

        if(imgsiz == 'large'):
            logo_im = Image.open('./noaa_logo_ice_42.png')
            logo_x = 1000 - logo_im.size[0]
            logo_y = 670 - logo_im.size[1]

            img2 = Image.open('tmp.png')
            img2 = img2.resize((1000, 670), Image.ANTIALIAS)

            fnt = ImageFont.truetype('./Fonts/Trebuchet_MS.ttf', 18)
            draw = ImageDraw.Draw(img2)
            draw.text((80, 544), "Alaska", font=fnt, color='#FFFFFF')
            draw.text((660, 460), "Greenland", font=fnt, color='#FFFFFF')
            draw.text((118, 75), "Russia", font=fnt, color='#FFFFFF')

            # draw.text((940,356), "open", font=fnt, color='#FFFFFF')
            # draw.text((940,375), "water", font=fnt, color='#FFFFFF')

            img2.paste(logo_im, (logo_x, logo_y))

            imgday = yyyy+months[timeIndx]+days[timeIndx]
            cmd = "python ./IceAgeColorbar.py "+imgday+" "+imgsiz
            subprocess.call(cmd, shell=True)

            img3 = Image.open('temporary_cbar.png')

            img4 = Image.new('RGBA', size=(
                img2.size[0], img2.size[1]+img3.size[1]))
            img4.paste(img3, (0, img2.size[1]))
            img4.paste(img2, (0, 0))

            img4.save(outpng)

            img.close()
            img1.close()
            img2.close()

        if(imgsiz == 'diy'):
            imgday = yyyy+months[timeIndx]+days[timeIndx]
            imname = 'IceSnow--Weekly--Sea-Ice-Age--Arctic--'+yyyy + \
                '-'+months[timeIndx]+'-'+days[timeIndx]+'--fullres'
            #cmd = 'mv tmp.png '+imname+'.png'
            #subprocess.call(cmd, shell=True)

            img = Image.open('tmp.png')

            fnt = ImageFont.truetype('./Fonts/Trebuchet_MS.ttf', 36)
            draw = ImageDraw.Draw(img)
            draw.text((192, 1299), "Alaska", font=fnt, color='#FFFFFF')
            draw.text((1587, 1098), "Greenland", font=fnt, color='#FFFFFF')
            draw.text((280, 200), "Russia", font=fnt, color='#FFFFFF')

            # draw.text((2260,860), "open", font=fnt, color='#FFFFFF')
            # draw.text((2260,897), "water", font=fnt, color='#FFFFFF')
            # 2405x1600

            img.save(imname+'.png')

            cmd = "python ./IceAgeColorbar.py "+imgday+" "+imgsiz
            subprocess.call(cmd, shell=True)
            cmd = 'mv temporary_cbar.eps '+imname+'_colorbar.eps'
            subprocess.call(cmd, shell=True)
            cmd = 'zip '+imname+'.zip '+imname+'.png '+imname+'_colorbar.eps noaa_logo.eps'
            subprocess.call(cmd, shell=True)
            cmd = 'mv '+imname+'.zip /work/NSIDC_Ice/Images/04-full_res_zips'
            subprocess.call(cmd, shell=True)
            cmd = 'rm IceSnow--Weekly--Sea-Ice-Age--Arctic*'
            subprocess.call(cmd, shell=True)

            img.close()

        if(imgsiz == 'broadcast'):
            logo_im = Image.open('./noaa_logo_ice_100.png')
            logo_x = 1920 - logo_im.size[0]
            logo_y = 936 - logo_im.size[1]
            img2 = Image.open('tmp.png')
            img2 = img2.resize((1920, 936), Image.ANTIALIAS)

            fnt = ImageFont.truetype('./Fonts/Trebuchet_MS.ttf', 26)
            draw = ImageDraw.Draw(img2)
            draw.text((153, 759), "Alaska", font=fnt, color='#FFFFFF')
            draw.text((1266, 642), "Greenland", font=fnt, color='#FFFFFF')
            draw.text((200, 75), "Russia", font=fnt, color='#FFFFFF')

            # draw.text((1800,500), "open", font=fnt, color='#FFFFFF')
            # draw.text((1800,527), "water", font=fnt, color='#FFFFFF')

            img2.paste(logo_im, (logo_x, logo_y))

            imgday = yyyy+months[timeIndx]+days[timeIndx]
            cmd = "python ./IceAgeColorbar.py "+imgday+" "+imgsiz
            subprocess.call(cmd, shell=True)

            img3 = Image.open('temporary_cbar.png')

            img4 = Image.new('RGBA', size=(
                img2.size[0], img2.size[1]+img3.size[1]))
            img4.paste(img3, (0, img2.size[1]))
            img4.paste(img2, (0, 0))

            img4.save(outpng)

            img.close()
            img1.close()
            img2.close()

        cmd = 'rm tmp.png'
        subprocess.call(cmd, shell=True)
