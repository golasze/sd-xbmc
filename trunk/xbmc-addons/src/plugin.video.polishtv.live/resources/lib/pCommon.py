# -*- coding: utf-8 -*-
import re, os, sys, cookielib
import urllib, urllib2, re, sys, math

scriptID = sys.modules[ "__main__" ].scriptID
scriptname = "Polish Live TV"

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

cj = cookielib.LWPCookieJar()

class common:
    def __init__(self):
        pass
    
    def requestData(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        data = response.read()
        response.close()    
        return data
    
    def isNumeric(self,s):
	try:
	    float(s)
	    return True
	except ValueError:
	    return False