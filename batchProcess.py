#!/usr/bin/python


import sys, datetime, subprocess
import numpy as np

if __name__ == '__main__':

	#years = years = np.arange(2000,2019,1)
	years = ['2024']
	#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	months = ['01']
	siz = ['small', 'large', 'diy', 'broadcast']
	#siz = ['diy']
	
	for i in range(len(years)):
		for j in range(len(months)):
			for k in range(len(siz)):
				cmd = 'python IceAgeMapandDriver.py '+str(years[i])+months[j]+' '+siz[k]
				subprocess.call(cmd,shell=True)
				
				cmd = './UploadIceImages.csh'
				subprocess.call(cmd,shell=True)