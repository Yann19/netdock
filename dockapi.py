#!/usr/bin/python

from docker import Client
import requests
import re


def get(name, server):
  c=Client('http://'+server)
  for dock in c.containers(all=True):
    if '/'+name in dock['Names']:
      return dock['Id']

#def isstart(name, server):
#  c=Client('http://'+server)
#  for dock in c.containers():
#    if '/'+name in dock['Names']:
#      return True
#  return False

def create(name, image, server, force=False):
  #force can be set with a registry url value
  c=Client('http://'+server)
  if not c.images(name=image):
    if force:
      r=requests.get('http://'+force+'/v1/search')
      if r.status_code == 200:
        for i in r.json()['results']:
          if image.split('/').pop() == i['name'].split('/').pop():
            out=c.pull(force+'/'+image.split('/').pop(),insecure_registry=True,stream=False)
            if not re.search('errorDetail', out):
              r=c.create_container(image=image, network_disabled=True, name=name)
              return r['Id']
            else:
              return False
      else:
        return False
  else: 
    r=c.create_container(image=image, network_disabled=True, name=name)
    return r['Id']

def start(name, server):
  id=get(name, server)
  if id:
    c=Client('http://'+server)
    c.start(container=name, network_mode=None)
    return id
  else:
    return False

def stop(name, server):
  dock=get(name, server)
  if dock:
    c=Client('http://'+server)
    c.stop(container=name)
  else:
    return False

def destroy(name, server):
  c=Client('http://'+server)
  c.remove_container(container=name, force=True)

  
