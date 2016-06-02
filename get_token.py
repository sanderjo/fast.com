import urllib




verbose = True
if True:

	jsname = '/app-40647a.js'
	url = 'https://fast.com' + jsname
	if verbose: print "javascript url is", url
	urlresult = urllib.urlopen(url)
	allJSstuff = urlresult.read()	# this is a obfuscated Javascript file 
	'''
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


	
