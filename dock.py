#!/usr/bin/python
# cli 

from sys import argv
import re
import docknet as net
import dockapi as api

def usage():
  print 'usage : '
  print "\t"+argv[0]+" <server> <up> <name> <bridge> <ip> <gateway>"
  print "\t"+argv[0]+" <server> <down> <name>"
  print "\t <server> : server ip, eg a.b.c.d:xxxx"
  print "\t <name> : docker name"
  print "\t <bridge> : ovs bridge name"
  print "\t <ip> : ip and mask eg: a.b.c.d/xy"
  print "\t <gateway> : gateway eg: a.b.c.e"
  print "\t [image] : if image, try to create container eg: registry:5000/image"
  exit(0)

def start(server, name, bridge, ip, gateway):
  id=api.start(name, server)
  if id:
    ns=net.ensure_netns(id)
    heth,deth=net.create_veth(ns)
    net.add_ip(deth, ip, ns)
    net.add_route('default', gateway, ns)
    net.add_port(bridge, heth)
    net.int_up(heth)
    return True
  else:
    return False

def stop(server, name):
  ns=net.ensure_netns(api.get(name, server))
  l_eth=net.get_eth(ns)
  l_eth.remove('lo')
  for eth in l_eth:
    heth=re.sub('deth','heth',eth)
    br=net.get_bridge(heth)
    if br:
      net.del_port(br, heth)
      net.del_veth(heth)
  net.del_netns(ns)
  api.stop(name, server)  

def create(server, image, name):
  force=image.split('/')[0]
  api.create(name, image, server, force)

if  __name__ == '__main__':
  def iscidr(cidr):
    reg_cidr=re.compile('^(?:[1-2]?[0-9]?[0-9]\.){3}[1-2]?[0-9]?[0-9]/[1-3]?[0-9]$')
    if reg_cidr.match(cidr):
      return True
  def isip(ip):
    reg_ip=re.compile('^(?:[1-2]?[0-9]?[0-9]\.){3}[1-2]?[0-9]?[0-9]$')
    if reg_ip.match(ip):
      return True

  if len(argv) < 4:
    usage()
  elif argv[2] == 'down': 
    server=argv[1]
    name=argv[3]
    stop(server, name)
  elif argv[2] == 'up':
    if len(argv) < 7:
      usage()
    server=argv[1]
    name=argv[3]
    bridge=argv[4]
    if not iscidr(argv[5]):
      usage()
    ip = argv[5]
    if not isip(argv[6]):
      usage()
    gateway = argv[6]      
    res=start(server, name, bridge, ip, gateway)
    if not res and argv[7]:
      create(server, argv[7], name)
      start(server, name, bridge, ip, gateway)
  else:
    usage()
