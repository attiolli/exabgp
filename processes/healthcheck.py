#!/usr/bin/env python3
#
# Author: Olli Attila
# Date: 2024-01-14
# Description:
#   Exabgp script to monitor DNS server and based on its reply,
#   announce/withdraw its service IP using BGP.


import dns.resolver
from collections import namedtuple
from sys import stdout
from time import sleep
from datetime import datetime

# Set some variables
logfile_path = '/etc/exabgp/log/bgp.log'

def check_dns_record(host, dns_server):
    """ Check if a specific A record exists for a host using a specific DNS server """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.timeout = 1
    resolver.lifetime = 1

    try:
        answers = resolver.resolve(host, 'A')
        return any(answers)
    except dns.resolver.NXDOMAIN:
        return False
    except dns.exception.Timeout:
        return False
    except dns.exception.DNSException:
        return False

# Add namedtuple object for easy reference below
TrackedObject = namedtuple('EndHost', ['host', 'dns_server', 'prefix', 'nexthop'])

# Make a list of these tracked objects
tracked_objects = [
    TrackedObject('google.fi', '10.127.127.127', '10.127.127.127', 'self'),
    TrackedObject('google.fi', '10.127.127.127', '10.128.128.128', 'self'),
]

while True:
    for host in tracked_objects:
        if check_dns_record(host.host, host.dns_server):
            announcement = 'announce route {} next-hop {}\n'.format(host.prefix, host.nexthop)
            stdout.write(announcement)
            # Log the announcement to the file with timestamp
            with open(logfile_path, 'a') as logfile:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logfile.write('{}: {}\n'.format(timestamp, announcement))
            stdout.flush()
        else:
            withdrawal = 'withdraw route {} next-hop {}\n'.format(host.prefix, host.nexthop)
            stdout.write(withdrawal)
            # Log the withdrawal to the file with timestamp
            with open(logfile_path, 'a') as logfile:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logfile.write('{}: {}\n'.format(timestamp, withdrawal))
            stdout.flush()
    sleep(2)
