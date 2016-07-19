# -*- coding: utf-8 -*-
#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2
page_num=1
max_page_num=23
for page_num in range(max_page_num):
    page = urllib2.urlopen('https://tw.bid.yahoo.com/booth/Y8334107322?page='+str(page_num)+'&bfe=1').read()
    soup = BeautifulSoup(page)
    print "now:"+str(page_num)
    i = 0
    for i in range(50):
        href = soup.select('.item-wrap')[i].a.attrs['href']
        print href
        content_page = urllib2.urlopen(href).read()
        content_soup = BeautifulSoup(content_page)
        wrap = content_soup.select(".main")[0].text
        # print wrap
        if "cherrybabyovo" in wrap:
    	    print "NONONO  "+href
 