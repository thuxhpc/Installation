# -*- coding: utf-8 -*-
from novaclient import client
nova = client.Client(2,"admin","hpc123","admin","http://140.128.101.69:5000/v2.0")

hl = nova.hypervisors.list()
print(hl[0])