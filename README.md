# netdock
python library for docker and openvswitch

it's a first step for create a tool to attach docker container in complex networks

the goal is to create a powerfull snd api using openflow

based on : https://github.com/jpetazzo/pipework

Cause I use ovs_lib (part of neutron : https://github.com/openstack/neutron/) you have to install oslo components to make it works.
     
     aptitude install python-dev  
     python-keystoneclient
     pip install --upgrade oslo.config
     pip install --upgrade oslo.log
     pip install --upgrade oslo.rootwrap
     pip install --upgrade oslo.db
     pip install --upgrade oslo.messaging
     pip install --upgrade oslo.concurrency
     pip install --upgrade retrying

I use pyroute2

     pip install --upgrade pyroute2

I work on ubuntu 14.04

I launch docker with : '-H tcp://127.0.0.1:8080 -H unix:///var/run/docker.sock' (/etc/default/docker)

..
