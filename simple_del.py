#!/usr/bin/python
# used to destroy network mappage before destroy docker

from sys import argv
from netdock import *

if len(argv) != 3:
  print 'usage : '
  print "\t"+argv[0]+" <name> <bridge>"
  exit(0)
else:
  name=argv[1]
  bridge=argv[2]

print "destroy network for :"+name
Id=get_dock_id(name)
ns=ensure_netns(Id)
for eth in get_eth():
  if ns in eth:
    del_port(bridge, eth)
    del_veth(eth)
    del_netns(ns)
    print "done"
