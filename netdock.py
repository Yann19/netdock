#!/usr/bin/python
# network mapper docker / openvwitch

from sys import argv
from pyroute2 import IPDB
from pyroute2 import NetNS
from os import symlink, path
from requests import get
import re

#ovs_lib is part of neutron library, you can get it on github
# copy neutron directory in a python path like /usr/local and install oslo (.config, .log etc .. list!)
import neutron.agent.common.ovs_lib as ovs_lib


##api docker
def get_dock_id(name):
  base_url="http://127.0.0.1:8080/"
  r = get(base_url+'/containers/json')
  if r.status_code == 200:
    for dock in r.json():
      if '/'+name in dock['Names']:
        Id=dock['Id']
    if Id:
      return Id
    else:
       return False


def create_netns(Id):
  #do not work as sudo, only as root (sudo docker start ? or for symlinks ? .. see to use rootwrapper ..)
  ns_file='/sys/fs/cgroup/devices/docker/'+str(Id)+'/tasks'
  file=open(ns_file)
  ns=file.readlines()[0]
  file.close()
  ns=ns.rstrip()
  ns_src='/proc/'+str(ns)+'/ns/net'
  ns_dst='/var/run/netns/'+str(ns)
  print str(ns)
  if not path.isfile(ns_dst):
    try:
      #add test for valid symlink .. 
      symlink(ns_src, ns_dst)
      return ns
    except:
      return False
  else:
    return ns

def create_veth(ns, prefix=''):
  #prefix can be usefull if there are more than one interface.. to see
  eth_host=prefix+'heth_'+str(ns)
  eth_dock=prefix+'deth_'+str(ns)
  #init ipdb
  ipdb=IPDB()
  #create veth interface
  ipdb.create(ifname=eth_host, kind='veth', peer=eth_dock).commit()
  #set peer interface in namespace
  ipdb.interfaces[eth_dock].net_ns_fd=ns
  ipdb.interfaces[eth_dock].commit()
  ipdb.release()
  return (eth_host,eth_dock)

def add_ip(eth, ip='', ns=''):
  if ns:
    ipdb=IPDB(nl=NetNS(ns))
  else:
    ipdb=IPDB()
  if ip:
    ipdb.interfaces[eth].add_ip(ip)
  ipdb.interfaces[eth].up()
  ipdb.interfaces[eth].commit()
  ipdb.release()

def add_route(dst, gateway, ns=''):
  if ns:
    ipdb=IPDB(nl=NetNS(ns))
  else:
    ipdb=IPDB()
  ipdb.routes.add({'dst':dst, 'gateway':gateway}).commit()
  ipdb.release()

def int_up(eth, ns=''):
  if ns:
    ipdb=IPDB(nl=NetNS(ns))
  else:
    ipdb=IPDB()
  ipdb.interfaces[eth].up()
  ipdb.interfaces[eth].commit()

def add_port(br, eth):
  ovs=ovs_lib.BaseOVS()
  if not br in ovs.get_bridges():
    return False
  ovs.add_bridge(br).add_port(eth)


