# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from novaclient import client
from openstack.models import VmModel
import demjson


##
from bs4 import BeautifulSoup
import urllib2
##


# Create your views here.

nova = client.Client(2,"admin","hpc123","admin","http://172.23.2.49:5000/v2.0")


def queryVM(request):
    global nova
    # my_vmlist=[]
    servers = nova.servers
    servers_dict = []


    for item in servers.list():
        item_array={'id':item.id,'name':item.name,'vnc_url':item.get_vnc_console('novnc')['console']['url'],'status':item.status}
        servers_dict.append(item_array)
    
    json = demjson.encode(servers_dict)
    return render_to_response('queryVM.html',locals())
   


def rebootVM(request, vm_name):
    global nova
    for n in nova.servers.list():
        if n.name == vm_name:
            n.reboot(reboot_type='SOFT')
    	    
    return render_to_response('queryVM.html',locals())

def stopVM(request, vm_name):
    global nova
    for n in nova.servers.list():
        if n.name == vm_name:
            n.stop()
    	    
    return render_to_response('queryVM.html',locals())

def startVM(request, vm_name):
    global nova
    for n in nova.servers.list():
        if n.name == vm_name:
    	    n.start()
    return render_to_response('queryVM.html',locals())
    
def statusVM(request, vm_name):
    global nova
    for n in nova.servers.list():
        if n.name == vm_name:
    	    json = n.status
    return render_to_response('queryVM.html',locals())





def getVNC(request, vm_name):
    
    global nova
    s = nova.servers.list()
   
    for n in nova.servers.list():
        if n.name == vm_name:
            json = n.get_vnc_console('novnc')['console']['url']

                
    return render_to_response('queryVM.html',locals())



def queryFlavors(request):
    global nova
    my_vmlist=[]
    s = nova.flavors.list()
        #依序列出VM 放入dic
    for i in range(0,len(s)):    
                               
        my_array={'name':str(s[i].name),'ram':str(s[i].ram),'vcpus':str(s[i].vcpus ),'disk':str(s[i].disk),'swap':str(s[i].swap ),'rxtx_factor':str(s[i].rxtx_factor)}
        my_vmlist.append(my_array)
    
    json =  demjson.encode(my_vmlist)
   
    return render_to_response('queryVM.html',locals())

def index( request ):
    global nova
    s = nova.servers.list() #get vm list
    flavors = nova.flavors.list() #get flavors list
    return render_to_response('index.html',locals())
    # return render_to_response( 'index.html',
    #         {"mytitle":"customize_title"})

def deleteVM(request ,vm_id):
    global nova
    
    vm = nova.servers.get(vm_id)
    nova.servers.delete(vm)

    return render_to_response('queryVM.html',locals())

def addVM(request ,vm_name):
    global nova
    
    image_id =  nova.images.list()[1].id
    image =  nova.images.get(image_id)
    flavor = nova.flavors.list()[0]
    nova.servers.create(vm_name,image,flavor)

    return render_to_response('queryVM.html',locals())

def getVMlist(request):
    s = nova.servers.list() #get vm list
    return render_to_response('page/vmlist.html',locals())