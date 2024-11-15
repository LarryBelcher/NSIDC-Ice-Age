#!/usr/bin/python


import sys, datetime, subprocess, os


if __name__ == '__main__':

	thisyyyy = datetime.datetime.now().year
	yyyy = datetime.datetime.now().year
	
	if(len(sys.argv) == 2):
		yyyy = sys.argv[1]
	
	#Cleanup Local Data Directory
	dataDir = '/work/NSIDC_Ice/Data/'
	cmd = 'rm '+dataDir+'*'+str(yyyy)+'*'
	subprocess.call(cmd,shell=True)
	
	#cURL the server and get the actual filename
	url = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0611_seaice_age_v4/data/'
	if(int(yyyy) == thisyyyy):
		url = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0749_ql_iceage/'
	
		
	cmd = 'curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n '+url+' | grep '+str(yyyy)+' | grep .nc'	
	fn = os.popen(cmd).read()
	filename = 'iceage'+fn.split('iceage')[-2].split('"')[0]
	
	
	#Now download the file and store it in the data directory	
	cmd = 'curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -O '+url+filename
	subprocess.call(cmd,shell=True)
	cmd = 'mv '+filename+' '+dataDir
	subprocess.call(cmd,shell=True)