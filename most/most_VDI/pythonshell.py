# -*- coding: utf-8 -*-
from novaclient import client
import demjson
nova = client.Client(2,"admin","hpc123","admin","http://140.128.101.69:5000/v2.0")
image_id =  nova.images.list()[1].id
image =  nova.images.get(image_id)
flavor = nova.flavors.list()[0]
# # nova.servers.delete(nova.servers.list()[3])

# print nova.servers.get('eaf0b4b8-d274-4a72-a615-fde8e6677917')
for i in range(10):
    nova.servers.create(str(i),image,flavor)


