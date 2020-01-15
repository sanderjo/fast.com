#!/usr/bin/env python2
import argparse

parser = argparse.ArgumentParser(description='Run speed test.')
parser.add_argument('-4', '--ipv4', dest='ipv4', help='IPv4 source address')
parser.add_argument('-6', '--ipv6', dest='ipv6', help='IPv6 source address')
parser.add_argument('-i', '--interface', dest='interface', help='Set network interface')
parser.add_argument('-t', '--timeout', help='HTTP timeout in seconds.')

args = parser.parse_args()
ipv4_source = None
ipv6_source = None

ipv4_source = args.ipv4
ipv6_source = args.ipv6
network_interface = args.interface
network_timeout = args.timeout

import socket
from patch_socket_create_connection import CustomSocket
my_socket = CustomSocket(
        ipv4_source=ipv4_source, ipv6_source=ipv6_source, 
        network_interface=network_interface, network_timeout=network_timeout)
socket.create_connection = my_socket.create_connection_with_custom_network_interface

import fast_com

print "Start speedtest against fast.com ..."
print "Result:", fast_com.fast_com(), "Mbps"
print "... Done"

