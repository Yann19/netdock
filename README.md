# netdock
python library for docker and openvswitch

it's a first step for create a tool to attach docker container in complex networks

the goal is to create a powerfull snd api using openflow

based on : https://github.com/jpetazzo/pipework

ovs_lib (part of neutron : https://github.com/openstack/neutron/) so you have to install oslo components to make it works.

     aptitude install python-dev  
     aptitude install python-pastedeploy
     pip install --upgrade oslo.config
     pip install --upgrade oslo.log
     pip install --upgrade oslo.rootwrap
     pip install --upgrade oslo.db
     pip install --upgrade oslo.messaging
     pip install --upgrade oslo.concurrency
     pip install --upgrade retrying
     pip install --upgrade babel
     pip install --upgrade iso8601
     pip install --upgrade python-keystoneclient
     pip install --upgrade routes

pyroute2

     pip install --upgrade pyroute2

I work on ubuntu 14.04 with docker 1.5

     aptitude install software-properties-common
     add-apt-repository ppa:docker-maint/testing
     aptitude update
     aptitude install docker.io

I launch docker with : '-H tcp://127.0.0.1:8080 -H unix:///var/run/docker.sock' (/etc/default/docker)

..
