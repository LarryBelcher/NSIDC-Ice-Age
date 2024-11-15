#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from urllib.request import urlopen
import gdal 

# This requires https://github.com/jswhit/basemap/commit/4cc223c1f47891e9430b29c3780b264d9761428d


m = Basemap(llcrnrlon=-180.,llcrnrlat=-90,urcrnrlon=180.,urcrnrlat=90.,resolution='c',area_thresh=10000.,lat_ts=30,projection='cea')
m.pcolormesh ( lons, lats, smm, latlon=True)
m.drawcoastlines()
