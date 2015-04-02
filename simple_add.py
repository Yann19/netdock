#!/usr/bin/python
# mapper for web container, map on private bridge

from sys import argv
from netdock import *

if len(argv) != 5:
  print 'usage : '
  print "\t"+argv[0]+" <name> <bridge> <ip> <gateway>"
  print "\t <name> : docker name"
  print "\t <bridge> : ovs bridge name"
  print "\t <ip> : ip and mask eg: a.b.c.d/xy"
  print "\t <gateway> : gateway eg: a.b.c.e"
  exit(0)
else:
  name=argv[1]
  bridge=argv[2]
  ip=argv[3]
  gateway=argv[4]


print "map "+name+" to "+bridge+" bridge with "+ip
Id=get_dock_id(name)
print str(Id)
ns=ensure_netns(Id)
print str(ns)
heth,deth=create_veth(ns)
add_ip(deth, ip, ns)
add_route('default', gateway, ns)
add_port(bridge, heth)
int_up(heth)

print 'ok, test ping to : '+ip


