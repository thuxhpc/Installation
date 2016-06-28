"""hpcproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib import admin
from openstack.views import queryVM, rebootVM ,startVM, stopVM ,statusVM ,index, getVNC ,queryFlavors ,deleteVM ,getVMlist

urlpatterns = [
    # url(r'^YukiIloveU/$', love),
    # url(r'^pq/(.*)/$', pq),
    

    url(r'^admin/', include(admin.site.urls)),
    url(r'^queryVM/$', queryVM),
    url(r'^rebootVM/(.*)/$', rebootVM),
    url(r'^startVM/(.*)/$', startVM),
    
    url(r'^stopVM/(.*)/$', stopVM),
    url(r'^statusVM/(.*)/$', statusVM),
    url(r'^deleteVM/(.*)/$', deleteVM),
    url(r'^getVNC/(.*)/$', getVNC),
    url(r'^queryFlavors/$', queryFlavors),

    # url(r'^vmlist/$', TemplateView.as_view(template_name='page/vmlist.html')),
    url(r'^vmlist/$', getVMlist),
   
    url(r'^$', index),
    # url(r'^flavors/$', flavor_page),

    url( r'^js/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': '/home/hpcctr/hpcproject/resources/js/' }
    ),
    url( r'^css/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': '/home/hpcctr/hpcproject/resources/css/' }
    ),
    url( r'^fonts/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': '/home/hpcctr/hpcproject/resources/fonts/' }
    ),

    url( r'^images/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': '/home/hpcctr/hpcproject/resources/images/' }
    ),
]
