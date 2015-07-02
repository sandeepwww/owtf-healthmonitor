import time
import urllib
import urllib2
import simplejson
import logging
import sys

#Gets a list of target URLs using the API request
def get_targeturls():
	try:
		url="http://localhost:8009/api/targets/1"
		req = urllib2.Request(url, None, {'user-agent':'Mozilla'})
		opener = urllib2.build_opener()
		f = opener.open(req) 
		a=simplejson.load(f) 
		curr_target_urls=[]
		curr_target_urls.append(a['target_url'])
		return curr_target_urls
	except Exception,e:
		print e
		print "Error: Please Start OWTF script!\n"
		sys.exit(0)
#Initialisations
i=0
error=False
starttime=time.time()
freeze_time=10
code=""


#Check if the URL is up
def check_targets(url):
	code=urllib.urlopen(url).getcode()
	return code

#Timing Manager
while True:
	target_urls=[]
	target_urls=get_targeturls()
	print target_urls
	for i in range(len(target_urls)):	
		finalcode=check_targets(target_urls[i])
		print "Attempt "+str(i+1)+": Status Code is "+str(finalcode)
		if(finalcode!=200):
			error=True			
			break
	
	if error:
		print "Error !"
		logging.basicConfig(filename='health_monitor.log',level=logging.INFO)
		logging.info("Bad Status Code : " + str(finalcode))
		logging.warning("Check your internet connection")	
		break
	else:		
		time.sleep(int(freeze_time) - ((time.time() - starttime) % int(freeze_time)))
