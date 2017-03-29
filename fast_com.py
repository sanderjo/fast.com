#!/usr/bin/env python

'''
Python CLI-tool (without need for a GUI) to measure Internet speed with fast.com

'''


import os
import json
import urllib
import urllib2
import sys
#import jsbeautifier
import time
#import threading
from threading import Thread


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
	# convert bytes (at application layer) to bits (at network layer)
	return bytes * 8 * 1.0415
	# 8 for bits versus bytes
	# 1.0416 for application versus network layers


def findipv4(fqdn):
	'''
		find IPv4 address of fqdn
	'''
	import socket
	ipv4 = socket.getaddrinfo(fqdn, 80, socket.AF_INET)[0][4][0]
	return ipv4

def findipv6(fqdn):
	'''
		find IPv6 address of fqdn
	'''
	import socket
	ipv6 = socket.getaddrinfo(fqdn, 80, socket.AF_INET6)[0][4][0]
	return ipv6


def fast_com(verbose=False, maxtime=15, forceipv4=False, forceipv6=False):
	'''
		verbose: print debug output
		maxtime: max time in seconds to monitor speedtest 
		forceipv4: force speed test over IPv4
		forceipv6: force speed test over IPv6
 	'''
	# go to fast.com to get the javascript file
	url = 'https://fast.com/'
	try:
		urlresult = urllib.urlopen(url)
	except:
		# no connection at all?
		return 0
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
	'''
	# OLD STUFF ... beautiful, but needs the js-beautifier module, which was a non-stardard requirement
	res = jsbeautifier.beautify(allJSstuff)	# ... so un-obfuscate it
	for line in res.split('\n'):
		if line.find('token:') >= 0:
			token = line.split('"')[1]
	if verbose: print "token is", token
	'''

	'''
	We're searching for the "token:" in this string:
	.dummy,DEFAULT_PARAMS={https:!0,token:"YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm",urlCount:3,e
	'''
	for line in allJSstuff.split(','):
		if line.find('token:') >= 0:
			if verbose: print "line is", line
			token = line.split('"')[1]
			if verbose: print "token is", token
			if token:
				break

	# https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3
	# https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3
	# lynx --dump  'https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3'  | python -mjson.tool
	#url = 'https://api.fast.com/netflix/speedtest?https=true&token=YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm&urlCount=3'


	# With the token, get the (3) speed-test-URLS from api.fast.com (which will be in JSON format):
	baseurl = 'https://api.fast.com/'
	if forceipv4:
		# force IPv4 by connecting to an IPv4 address of api.fast.com (over ... HTTP)
		ipv4 = findipv4('api.fast.com')
		baseurl = 'http://' + ipv4 + '/'	# HTTPS does not work IPv4 addresses, thus use HTTP
	elif forceipv6:
		# force IPv6 
		ipv6 = findipv6('api.fast.com')
		baseurl = 'http://[' + ipv6 + ']/'

	url = baseurl + 'netflix/speedtest?https=true&token=' + token + '&urlCount=3'	# Not more than 3 possible
	if verbose: print "API url is", url
	try:
		urlresult = urllib2.urlopen(url, None, 2)	# 2 second time-out
	except:
		# not good
		if verbose: print "No connection possible"	# probably IPv6, or just no network
		return 0	# no connection, thus no speed

	jsonresult = urlresult.read()
	parsedjson = json.loads(jsonresult)

	# Prepare for getting those URLs in a threaded way:
	amount = len(parsedjson)
	if verbose: print "Number of URLs:", amount
	threads = [None] * amount
	results = [0] * amount
	urls = [None] * amount
	i = 0
	for jsonelement in parsedjson:
	    urls[i] = jsonelement['url']	# fill out speed test url from the json format
            if verbose: print jsonelement['url']
	    i = i+1

	# Let's check whether it's IPv6:
	for url in urls:
		fqdn = url.split('/')[2]
		try:
			socket.getaddrinfo(fqdn, None, socket.AF_INET6)
			if verbose: print "IPv6"
		except:
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
	print "let's speed test:"
	print "\nSpeed test, without logging:"
	print fast_com()
	print "\nSpeed test, with logging:"
	print fast_com(verbose=True)
	print "\nSpeed test, IPv4, with verbose logging:"
	print fast_com(verbose=True, maxtime=18, forceipv4=True)
	print "\nSpeed test, IPv6:"
	print fast_com(maxtime=12, forceipv6=True)
	print "\n30 second speed test:"
	fast_com(verbose=True, maxtime=30)

	print "\ndone"


