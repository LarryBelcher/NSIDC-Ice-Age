#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.font_manager as font_manager
from matplotlib.patches import Rectangle

def int2str(mm):
	ms = ''
	if(mm == '00'): ms = 'No Data'
	if(mm == '01'): ms = 'January'
	if(mm == '02'): ms = 'February'
	if(mm == '03'): ms = 'March'
	if(mm == '04'): ms = 'April'
	if(mm == '05'): ms = 'May'
	if(mm == '06'): ms = 'June'
	if(mm == '07'): ms = 'July'
	if(mm == '08'): ms = 'August'
	if(mm == '09'): ms = 'September'
	if(mm == '10'): ms = 'October'
	if(mm == '11'): ms = 'November'
	if(mm == '12'): ms = 'December'
	return ms

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


if __name__ == '__main__':	

	fdate = sys.argv[1]   #(expects format like: 20190120)
	yyyy = fdate[0:4]
	mm = fdate[4:6]
	dd = fdate[6:]

	monstr = int2str(mm)
	labeldate = monstr+' '+dd+', '+yyyy
	if(mm == '00'): labeldate = ms

	imgsize = sys.argv[2]   #(expects small, large, diy, broadcast)

	path = './Fonts/Trebuchet_MS.ttf'
	propr = font_manager.FontProperties(fname=path)
	path = './Fonts/Trebuchet_MS_Bold.ttf'
	propb = font_manager.FontProperties(fname=path)

	if(imgsize == 'small'):
		figxsize = 8.62
		figysize = 0.695
		figdpi = 72
		fsiz1 = 12
		fsiz2 = 11
		cbx = 0.2258; cbw = 0.5463; cby = 0.33; cbh = 0.259
		t1x = 0.385; t1y = 0.684
		#cbx = 0.2258+0.068; cbw = 0.5463; cby = 0.33; cbh = 0.259
		#t1x = 0.385+0.068; t1y = 0.684
		t2x = 0.654; t2y = 0.686
		t3x = 0.004; t3y = 0.77
		t4x = 0.899; t4y = 0.77
		t5x = 0.899; t5y = 0.55
		t6x = 0.278; t6y = 0.14
		t7x = 0.495; t7y = 0.14
		t8x = 0.700; t8y = 0.14
		pngfile = "temporary_cbar.png"
	
	if(imgsize == 'large'):
		figxsize = 13.89
		figysize = 0.695
		figdpi = 72
		fsiz1 = 12
		fsiz2 = 11
		cbx = 0.33; cbw = 0.339; cby = 0.33; cbh = 0.259
		t1x = 0.43; t1y = 0.685
		#cbx = 0.33+0.036; cbw = 0.339; cby = 0.33; cbh = 0.259
		#t1x = 0.43+0.036; t1y = 0.685
		t2x = 0.596; t2y = 0.684
		t3x = 0.003; t3y = 0.77
		t4x = 0.938; t4y = 0.77
		t5x = 0.938; t5y = 0.55
		pngfile = "temporary_cbar.png"

	if(imgsize == 'diy'):
		figxsize = 8.89
		figysize = 2.44
		figdpi = 72
		fsiz1 = 12
		fsiz2 = 11
		cbx = 0.185; cbw = 0.63; cby = 0.36; cbh = 0.1
		t1x = 0.4; t1y = 0.565
		t2x = 0.67; t2y = 0.565
		t3x = 0.05; t3y = 0.82
		t4x = 0.85; t4y = 0.82
		t5x = 0.85; t5y = 0.73
		pngfile = "temporary_cbar.eps"
	
	if(imgsize == 'broadcast'):
		figxsize = 26.68
		figysize = 2
		figdpi = 72
		fsiz1 = 32
		fsiz2 = 28
		cbx = 0.185; cbw = 0.63; cby = 0.5; cbh = 0.2
		t1x = 0.39; t1y = 0.78	
		#cbx = 0.185+0.06; cbw = 0.63; cby = 0.5; cbh = 0.2
		#t1x = 0.39+0.06; t1y = 0.78
		t2x = 0.57; t2y = 0.565
		t3x = 0.003; t3y = 0.83
		t4x = 0.92; t4y = 0.83
		t5x = 0.92; t5y = 0.62
		pngfile = "temporary_cbar.png"
	

	fig = plt.figure(figsize=(figxsize,figysize))

	# create an axes instance, leaving room for colorbar at bottom.
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], facecolor='#F5F5F5')
	ax1.set_frame_on(False)
	ax1.set_xticks([])
	ax1.set_xticklabels([])
	ax1.set_yticks([])
	ax1.set_yticklabels([])



	dval = "Arctic sea ice age (years)"
	plt.text(t1x, t1y, dval, fontproperties=propb, size=fsiz1, color='#333333')
	if(mm != '00'):
		plt.text(t3x, t3y, labeldate, fontproperties=propr, size=fsiz2, color='#8D8D8D')
		plt.text(t4x, t4y, 'Climate.gov', fontproperties=propr, size=fsiz2, color='#8D8D8D')
		plt.text(t5x, t5y, 'Data: NSIDC', fontproperties=propr, size=fsiz2, color='#8D8D8D')
		
		
		'''
		if(imgsize == 'small'):
			plt.gca().add_patch(Rectangle((0.17,0.33),0.1, 0.25, linewidth=1.0, edgecolor='k', facecolor='#505050'))
										#   x     y   xsz   ysz
			plt.text(0.171, 0.115, 'Open Ocean/', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.171, -0.05, 'Coastal Zones', fontproperties=propr, size=fsiz2, color='#000000')
			
		if(imgsize == 'large'):
			plt.gca().add_patch(Rectangle((0.29,0.33),0.06, 0.25, linewidth=1.0, edgecolor='k', facecolor='#505050'))
			plt.text(0.29, 0.115, 'Open Ocean/', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.29, -0.1, ' ', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.29, -0.05, 'Coastal Zones', fontproperties=propr, size=fsiz2, color='#000000')
			
		if(imgsize == 'broadcast'):
			plt.gca().add_patch(Rectangle((0.13,0.5),0.09, 0.2, linewidth=1.0, edgecolor='k', facecolor='#505050'))
			plt.text(0.13, 0.33, 'Open Ocean/', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.13, -0.1, ' ', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.13, 0.1, 'Coastal Zones', fontproperties=propr, size=fsiz2, color='#000000')
		
		if(imgsize == 'diy'):
			plt.gca().add_patch(Rectangle((0.45,0.15),0.1, 0.1, linewidth=1.0, edgecolor='k', facecolor='#505050'))
			plt.text(0.45, 0.08, 'Open Ocean/', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.45, -0.1, ' ', fontproperties=propr, size=fsiz2, color='#000000')
			plt.text(0.45, 0.01, 'Coastal Zones', fontproperties=propr, size=fsiz2, color='#000000')
	
		'''
	
	if(mm == '00'): 
		plt.text(t3x, t3y, labeldate, fontproperties=propr, size=fsiz2, color='#8D8D8D')
		plt.text(t4x, t4y, 'Climate.gov', fontproperties=propr, size=fsiz2, color='#8D8D8D')
		plt.text(t5x, t5y, 'Data: NSIDC', fontproperties=propr, size=fsiz2, color='#8D8D8D')




	levs = [1, 2, 3, 4, 5, 6]
	colors = [(40,59,79), (23,81,149), (43,140,190), (123,204,196), (255,255,255)]
	cmap = make_cmap(colors, bit=True)
	bounds = [1, 2, 3, 4, 5, 6]
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

	ax2 = fig.add_axes([cbx,cby,cbw,cbh], facecolor='#F5F5F5')
	ax2.set_frame_on(False)
	ax2.set_xticks([])
	ax2.set_xticklabels([])
	ax2.set_yticks([])
	ax2.set_yticklabels([])

	
	barticks = levs
	'''
	l1 = '0'; l1l = len(l1)+19; l1 = l1.rjust(l1l)
	l2 = '1'; l2l = len(l2)+19; l2 = l2.rjust(l2l)
	l3 = '2'; l3l = len(l3)+19; l3 = l3.rjust(l3l)
	l4 = '3'; l4l = len(l4)+19; l4 = l4.rjust(l4l)
	l5 = '4'; l5l = len(l5)+21; l5 = l5.rjust(l5l)
	l6 = '5+'; l6l = len(l6)+21; l6 = l6.rjust(l6l)
	'''
	if(imgsize == 'small' or imgsize == 'large'):
		l1 = '0'
		l2 = '1'; l2 = l2.ljust(2)
		l3 = '2'; l3 = l3.ljust(2)
		l4 = '3'; l4 = l4.ljust(2)
		l5 = '4'; l5 = l5.ljust(2)
		l6 = '5+'
		
	if(imgsize == 'broadcast' or imgsize == 'diy'):
		l1 = '0'
		l2 = '1'
		l3 = '2'
		l4 = '3'
		l5 = '4'
		l6 = '5+'
	
	barlevs = [l1, l2, l3, l4, l5, l6]
	
	bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	if(imgsize == 'diy'):
		bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
		bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	bar.outline.set_visible(True)
	bar.outline.set_linewidth(0.5)
	if( imgsize == 'broadcast'):
		bar.outline.set_linewidth(1.0)
	bar.ax.tick_params(size=0.01)
	bar.ax.set_xticklabels(barlevs, fontproperties=propr, size=fsiz2, va='top')
	
	

	if(imgsize != 'diy'):
		plt.savefig(pngfile, dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.0)
	
	if(imgsize == 'diy'):
		plt.savefig(pngfile, dpi=figdpi, orientation='portrait', bbox_inches='tight', pad_inches=0.0)
