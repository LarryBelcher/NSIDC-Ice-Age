#!/usr/bin/python

import glob, sys, os, subprocess, datetime, netCDF4
import matplotlib.font_manager as font_manager
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import from_levels_and_colors
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from simplekml import (Kml, OverlayXY, ScreenXY, Units,
                       RotationXY, AltitudeMode, Camera)

from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
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
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
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
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap

def compare_nan_array(func, a, thresh):
    out = ~np.isnan(a)
    out[out] = func(a[out], thresh)
    return out


def gmtColormap(fileName):

    import colorsys
    import numpy as N
    try:
        f = open(fileName)
    except:
        print("file ", fileName, "not found")
        return None

    lines = f.readlines()
    f.close()

    x = []
    r = []
    g = []
    b = []
    colorModel = "RGB"
    for l in lines:
        ls = l.split()
        if l[0] == "#":
            if ls[-1] == "HSV":
                colorModel = "HSV"
                continue
            else:
                continue
        if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
            pass
        else:
            x.append(float(ls[0]))
            r.append(float(ls[1]))
            g.append(float(ls[2]))
            b.append(float(ls[3]))
            xtemp = float(ls[4])
            rtemp = float(ls[5])
            gtemp = float(ls[6])
            btemp = float(ls[7])

    x.append(xtemp)
    r.append(rtemp)
    g.append(gtemp)
    b.append(btemp)

    nTable = len(r)
    x = N.array(x, N.float32)
    r = N.array(r, N.float32)
    g = N.array(g, N.float32)
    b = N.array(b, N.float32)
    if colorModel == "HSV":
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i]/360., g[i], b[i])
            r[i] = rr
            g[i] = gg
            b[i] = bb
    if colorModel == "HSV":
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i]/360., g[i], b[i])
            r[i] = rr
            g[i] = gg
            b[i] = bb
    if colorModel == "RGB":
        r = r/255.
        g = g/255.
        b = b/255.
    xNorm = (x - x[0])/(x[-1] - x[0])

    red = []
    blue = []
    green = []
    for i in range(len(x)):
        red.append([xNorm[i], r[i], r[i]])
        green.append([xNorm[i], g[i], g[i]])
        blue.append([xNorm[i], b[i], b[i]])
    colorDict = {"red": red, "green": green, "blue": blue}
    return (colorDict)


def int2str(mm):
    if(mm == '00'):
        ms = 'No Data'
    if(mm == '01'):
        ms = 'January'
    if(mm == '02'):
        ms = 'February'
    if(mm == '03'):
        ms = 'March'
    if(mm == '04'):
        ms = 'April'
    if(mm == '05'):
        ms = 'May'
    if(mm == '06'):
        ms = 'June'
    if(mm == '07'):
        ms = 'July'
    if(mm == '08'):
        ms = 'August'
    if(mm == '09'):
        ms = 'September'
    if(mm == '10'):
        ms = 'October'
    if(mm == '11'):
        ms = 'November'
    if(mm == '12'):
        ms = 'December'
    return ms


def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
             figs, colorbar=None, **kw):

    kml = Kml()
    altitude = kw.pop('altitude', 2e7)
    roll = kw.pop('roll', 0)
    tilt = kw.pop('tilt', 0)
    altitudemode = kw.pop('altitudemode', AltitudeMode.relativetoground)
    camera = Camera(latitude=90.,
                    longitude=-135.,
                    altitude=altitude, roll=roll, tilt=tilt,
                    altitudemode=altitudemode)

    kml.document.camera = camera
    draworder = 0
    for fig in figs:  # NOTE: Overlays are limited to the same bbox.
        draworder += 1
        ground = kml.newgroundoverlay(name='GroundOverlay')
        ground.draworder = draworder
        ground.visibility = kw.pop('visibility', 1)
        ground.name = kw.pop('name', 'overlay')
        ground.color = kw.pop('color', '9effffff')
        ground.latlonbox.rotation = kw.pop('rotation', 360)
        ground.description = kw.pop(
            'description', 'Age of Sea Ice')
        ground.gxaltitudemode = kw.pop('gxaltitudemode',
                                       'clampToGround')
        ground.icon.href = fig
        
        ground.latlonbox.east = llcrnrlon
        ground.latlonbox.south = llcrnrlat
        ground.latlonbox.north = urcrnrlat
        ground.latlonbox.west = urcrnrlon

        #ground.gxlatlonquad.coords = [(29.71270,-45.),(29.71270,45.),(29.71270,135.),(29.71270,-135.)]

    if colorbar:  # Options for colorbar are hard-coded (to avoid a big mess).
        screen = kml.newscreenoverlay(name='ScreenOverlay')
        screen.icon.href = colorbar
        screen.overlayxy = OverlayXY(x=0, y=0,
                                     xunits=Units.fraction,
                                     yunits=Units.fraction)
        screen.screenxy = ScreenXY(x=0.015, y=0.075,
                                   xunits=Units.fraction,
                                   yunits=Units.fraction)
        screen.rotationXY = RotationXY(x=0.5, y=0.5,
                                       xunits=Units.fraction,
                                       yunits=Units.fraction)
        screen.size.x = 0
        screen.size.y = 0
        screen.size.xunits = Units.fraction
        screen.size.yunits = Units.fraction
        screen.visibility = 1

    filename = figs[0].split('.png')[0]+'.kmz'
    kmzfile = kw.pop('kmzfile', figs[0])
    kml.savekmz(kmzfile)


def gearth_fig(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, pixels=1024):
    """Return a Matplotlib `fig` and `ax` handles for a Google-Earth Image."""
    aspect = np.cos(np.mean([llcrnrlat, urcrnrlat]) * np.pi/180.0)
    xsize = np.ptp([urcrnrlon, llcrnrlon]) * aspect
    ysize = np.ptp([urcrnrlat, llcrnrlat])
    aspect = ysize / xsize

    if aspect > 1.0:
        figsize = (10.0 / aspect, 10.0)
    else:
        figsize = (10.0, 10.0 * aspect)

    if False:
        plt.ioff()  # Make `True` to prevent the KML components from poping-up.

    fig = plt.figure(figsize=figsize, frameon=False, dpi=pixels//10)

    # KML friendly image.  If using basemap try: `fix_aspect=False`.
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(llcrnrlon, urcrnrlon)
    ax.set_ylim(llcrnrlat, urcrnrlat)
    ax.axis('off')
    return fig, ax


if __name__ == "__main__":

    os.chdir('/work/NSIDC_Ice')

    imgDate = sys.argv[1]  # Expects integer year and month (e.g., 201401)
    yyyy = imgDate[0:4]
    mm = imgDate[4:6]

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
    months = []
    days = []
    for i in range(len(time)):
        thisDate = timeOrigin + datetime.timedelta(days=time[i])
        yyyymmdd.append(thisDate.strftime('%Y%m%d'))
        months.append(thisDate.strftime('%m'))
        days.append(thisDate.strftime('%d'))

    ndx = []
    for i in range(len(months)):
        if(months[i] == mm):
            ndx.append(i)

    if(len(ndx) == 0):
        print(' ')
        print('Sorry, data are not available for '+yyyy+'-'+mm)
        sys.exit()

    for n in ndx:
        
        
        levs = [0, 1, 2, 3, 4, 5, 6]
        colors = [(80,80,80), (40,59,79), (23,81,149), (43,140,190), (123,204,196), (255,255,255)]
        my_cmap = make_cmap(colors, bit=True)
        bounds = [0, 1, 2, 3, 4, 5, 6]
        norm = mpl.colors.BoundaryNorm(bounds, my_cmap.N)
        
        
        data = alldata[n,:,:]

        
        #Set the upper values to zero
        data[data >= 20] = 0
        
        pixels = 1024 * 10
        
        lllon, lllat, urlon, urlat = [-179.92053, 29.80484, 179.92053 , 89.920296]
        
        #glllon, glllat, gurlon, gurlat = [-179.92053, 89.920296, 179.92053, 29.80484]
        
        
        ofile = 'IceSnow--Weekly--Sea-Ice-Age--Arctic--'+yyyy+'-'+months[n]+'-'+days[n]+'--'

        ms = int2str(months[n])
        
        fig, ax = gearth_fig(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, pixels=pixels)


        #fig = plt.figure(figsize=(10,10))
        #ax = fig.add_axes([0.0,0.0,1.0,1.0], frameon=False, facecolor='#F5F5F5')

        m = Basemap(llcrnrlon=lllon,llcrnrlat=lllat,urcrnrlon=urlon,urcrnrlat=urlat,resolution='c',area_thresh=10000.,lat_ts=30,projection='cea')
        m.pcolormesh ( lons, lats, data, latlon=True, cmap=my_cmap, norm=norm)
        #m.drawcoastlines()

        fig.savefig(ofile+'transparent.png', transparent='True')

        make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'transparent.png'], 
                kmzfile=ofile+'transparent.kmz', name='Weekly Sea Ice Age for '+ms+', '+yyyy)

        '''
        m = Basemap(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, resolution='c', area_thresh=10000., fix_aspect=False, projection='cea')
        
        
        m.imshow(data, cmap=my_cmap, norm=norm, interpolation='nearest', ax=ax)#, zorder=8)

        m.drawcoastlines(linewidth=0.25)
        m.drawcountries(linewidth=0.25)

        fig.savefig(ofile+'transparent.png', transparent='True')

        
        make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'transparent.png'], 
                kmzfile=ofile+'transparent.kmz', name='Weekly Sea Ice Age for '+ms+', '+yyyy)
    

        fig1, ax1 = gearth_fig(llcrnrlon=lllon,
                        llcrnrlat=lllat,
                        urcrnrlon=urlon,
                        urcrnrlat=urlat,
                        pixels=pixels)
    

        pdat = ax1.pcolormesh(lons, lats, data, cmap=my_cmap, vmin=0., vmax=8.) 
        fig1.savefig(ofile+'opaque.png', transparent='True')


    
    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'transparent.png'], 
                kmzfile=ofile+'transparent.kmz', name='Total precipitation for '+ms+', '+yyyy)

    cmd = "unzip "+ofile+"transparent.kmz 'doc.kml' > "+ofile+"transparent.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'transparent.kml'
    subprocess.call(cmd, shell=True)

    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'opaque.png'], 
                kmzfile=ofile+'opaque.kmz', name='Total precipitation for '+ms+', '+yyyy)
    
    cmd = "unzip "+ofile+"opaque.kmz 'doc.kml'"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'opaque.kml'
    subprocess.call(cmd, shell=True)

    p1 = subprocess.Popen("python precipColorbarKMZ.py "+fdate, shell=True)
    p1.wait()

    cmd = 'mkdir files'
    subprocess.call(cmd, shell=True)
    cmd = 'mv '+ofile+'*.png files/'
    subprocess.call(cmd, shell=True)
    cmd = 'mv precipKMZ_cbar.png '+ofile+'legend.png'
    subprocess.call(cmd, shell=True)

    cmd = 'zip '+ofile+'KML-assets.zip '+ofile+'transparent.kml '+ofile+'opaque.kml '+ofile+'legend.png files/*'
    subprocess.call(cmd, shell=True)

    cmd = 'mv '+ofile+'KML-assets.zip Images/Precipitation/05-kml/'
    subprocess.call(cmd, shell=True)

    #Cleanup
    cmd = 'rm *.kml'
    subprocess.call(cmd, shell=True)
    cmd = 'rm *.kmz'
    subprocess.call(cmd, shell=True)
    cmd = 'rm -rf files/'
    subprocess.call(cmd, shell=True)
    cmd = 'rm Precipitation--Monthly--Total--CONUS*.png'
    subprocess.call(cmd, shell=True)

    '''
