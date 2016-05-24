#!/usr/bin/env python

'''
Python CLI-tool (without need for a GUI) to measure Internet speed with fast.com

'''


import os
import json
import urllib
import sys
import jsbeautifier
import urllib2
import time
#import threading
from threading import Thread


def gethtml(url):
	print "fetching testfile:", url
	response = urllib2.urlopen(url)
	result = response.read()
	print "Fetched: ", len(result)
	return len(result)



def gethtmlresult(url,result,index):
	'''
	get the stuff from url in chuncks of size CHUNK, and keep writing the number of bytes retrieved into result[index]
	'''
	#print url, index, result[index]
	req = urllib2.urlopen(url)
	CHUNK = 100 * 1024
	i=1
	while True:
	    chunk = req.read(CHUNK)
	    if not chunk: break
	    result[index] = i*CHUNK
	    i=i+1

def application_bytes_to_networkbits(bytes):
	return bytes * 8 * 1.0415
	# 8 for bits versus bytes
	# 1.0416 for application versus network layers




def fast_com(verbose=False, maxtime=15):
	'''
		verbose: print debug output
		maxtime: max time in seconds to monitor speedtest 
	'''
	# go to fast.com to get the javascript file
	url = 'https://fast.com/'
	urlresult = urllib.urlopen(url)
	response = urlresult.read()
	for line in response.split('\n'):
		# We're looking for a line like
		#           <script src="/app-40647a.js"></script> 
		if line.find('script src') >= 0:
			#print line
			jsname = line.split('"')[1]	# At time of writing: '/app-40647a.js'


	# From that javascript file, get the token:
	url = 'https://fast.com' + jsname
	if verbose: print "javascript url is", url
	urlresult = urllib.urlopen(url)
	allJSstuff = urlresult.read()	# this is a obfuscated Javascript file 
	res = jsbeautifier.beautify(allJSstuff)	# ... so un-obfuscate it
	for line in res.split('\n'):
		if line.find('token:') >= 0:
			token = line.split('"')[1]
	if verbose: print "token is", token

	# https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3
	# https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3
	# lynx --dump  'https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3'  | python -mjson.tool
	#url = 'https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3'

	# With the token, get the (3) speed-test-URLS from api.fast.com:
	url = 'https://api.fast.com/netflix/speedtest?https=true&token=' + token + '&urlCount=3'	# Not more than 3 possible
	urlresult = urllib.urlopen(url)
	jsonresult = urlresult.read()
	parsedjson = json.loads(jsonresult)
	for item in parsedjson:
		if verbose: print item['url']


	# Prepare for getting those URLs in a threaded way:
	amount = len(parsedjson)
	if verbose: print "Number of URLs:", amount
	threads = [None] * amount
	results = [0] * amount
	urls = [None] * amount
	i = 0 # or 1
	for item in parsedjson:
	    urls[i] = item['url']
	    i = i+1

	# Let's check whether it's IPv6:
	import socket
	# socket.getaddrinfo("www.google.com", None, socket.AF_INET)
	# socket.getaddrinfo("www.google.com", None, socket.AF_INET6)
	for url in urls:
		#print url
		fqdn = url.split('/')[2]
		#print fqdn
		try:
			socket.getaddrinfo(fqdn, None, socket.AF_INET6)
			if verbose: print "IPv6"
		except:
			# print "IPv4"
			pass
		try:
			socket.getaddrinfo(fqdn, None, socket.AF_INET)
			#print "IPv4"
		except:
			# print "IPv6"
			pass

	# Now start the threads
	for i in range(len(threads)):
	    #print "Thread: i is", i
	    threads[i] = Thread(target=gethtmlresult, args=(urls[i], results, i))
	    threads[i].daemon=True
	    threads[i].start()

	# Monitor the amount of bytes (and speed) of the threads 
	time.sleep(1)
	sleepseconds = 3	# 3 seconds sleep
	lasttotal = 0
	highestspeedkBps = 0
	maxdownload = 60 #MB
	nrloops = maxtime / sleepseconds
	for loop in range(nrloops):
		total = 0
		for i in range(len(threads)):
			#print i, results[i]
			total += results[i]
		delta = total-lasttotal
		speedkBps = (delta/sleepseconds)/(1024)
		if verbose:
			print "Loop", loop, "Total MB", total/(1024*1024), "Delta MB", delta/(1024*1024), "Speed kB/s:", speedkBps, "aka Mbps %.1f" % (application_bytes_to_networkbits(speedkBps)/1024)
		'''
		if total/(1024*1024) > maxdownload:
			break
		'''
		lasttotal = total
		if speedkBps > highestspeedkBps:
			highestspeedkBps = speedkBps
		time.sleep(sleepseconds)
	'''
	print "Now wait for threads to end:"
	for i in range(len(threads)):
	    threads[i].join()
	'''

	Mbps = (application_bytes_to_networkbits(highestspeedkBps)/1024)
	Mbps = float("%.1f" % Mbps)
	if verbose: print "Highest Speed (kB/s):", highestspeedkBps,  "aka Mbps ", Mbps

	#print "Debug: total in bytes", total

	return Mbps


######## MAIN #################


if __name__ == "__main__": 
	print "let's go:"
	fast_com(verbose=True, maxtime=25)
	print "done"


