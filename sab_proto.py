#!/usr/bin/env python

from fast_com import fast_com

print "Starting Speed test against fast.com"


print "Speed test [Mbps]:",
print fast_com(maxtime=7)
print "Speed test, IPv4 [Mbps]:", 
print fast_com(maxtime=7, forceipv4=True)
print "Speed test, IPv6 [Mbps]:", 
print fast_com(maxtime=7, forceipv6=True)

