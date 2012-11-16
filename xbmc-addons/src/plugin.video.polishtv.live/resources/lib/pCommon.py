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
    
    def getURLFromFileCookieData(self, url, COOKIEFILE):
        cj.load(COOKIEFILE)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        data = response.read()
        response.close()    
        return data

    def postURLFromFileCookieData(self, url, COOKIEFILE, POST = {}):
        cj.load(COOKIEFILE)
        headers = { 'User-Agent' : HOST }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        dataPost = urllib.urlencode(POST)
        req = urllib2.Request(url, dataPost, headers)
        response = opener.open(req)
        data = response.read()
        response.close()
        return data
    
    def saveURLToFileCookieData(self, url, COOKIEFILE, POST = {}):
        headers = { 'User-Agent' : HOST }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        dataPost = urllib.urlencode(POST)
        req = urllib2.Request(url, dataPost, headers)
        response = opener.open(req)
        data = response.read()
        response.close()
        cj.save(COOKIEFILE)
        return data
        
    def makeABCList(self):
        strTab = []
        strTab.append('0 - 9');
        for i in range(65,91):
            strTab.append(str(unichr(i)))	
        return strTab
    
    def getItemByChar(self, char, tab):
        strTab = []
        char = char[0]
        for i in range(len(tab)):
            if ord(char) >= 65:
                if tab[i][0].upper() == char:
                    strTab.append(tab[i])
            else:
                if ord(tab[i][0]) >= 48 and ord(tab[i][0]) <= 57:
                    strTab.append(tab[i])
        return strTab       
    
    def isNumeric(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False