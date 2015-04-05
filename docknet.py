#!/usr/bin/python
# network mapper docker / openvwitch

from sys import argv
from pyroute2 import IPDB
from pyroute2 import NetNS
from os import symlink, path, remove

#ovs_lib is part of neutron library, you can get it on github
# copy neutron directory in a python path like /usr/local and install oslo (see readme)
import neutron.agent.common.ovs_lib as ovs_lib


##api docker

def ensure_netns(Id):
  ns_file='/sys/fs/cgroup/devices/docker/'+str(Id)+'/tasks'
  file=open(ns_file)
  ns=file.readlines()[0]
  file.close()
  ns=ns.rstrip()
  ns_src='/proc/'+str(ns)+'/ns/net'
  ns_dst='/var/run/netns/'+str(ns)
  if not path.isfile(ns_dst):
    try:
      #add test for valid symlink .. 
      symlink(ns_src, ns_dst)
      return ns
    except:
      return False
  else:
    return ns

def del_netns(ns):
  remove('/var/run/netns/'+str(ns))

def get_eth(ns=''):
  if ns:
    ipdb=IPDB(nl=NetNS(ns))
  else:
    ipdb=IPDB()
  return ipdb.by_name.keys()

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

def del_veth(eth):
  ipdb=IPDB()
  ipdb.interfaces[eth].remove().commit()
  ipdb.release() 

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
  ipdb.release()

def get_bridge(eth):
  ovs=ovs_lib.BaseOVS()
  for br in ovs.get_bridges():
    if eth in ovs.add_bridge(br).get_port_name_list():
      return br 

def add_port(br, eth):
  ovs=ovs_lib.BaseOVS()
  if not br in ovs.get_bridges():
    return False
  ovs.add_bridge(br).add_port(eth)

def del_port(br, eth):
  ovs=ovs_lib.BaseOVS()
  ovs.add_bridge(br).delete_port(eth)

