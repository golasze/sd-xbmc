# -*- coding: utf-8 -*-
import re, os, sys, cookielib
import urllib, urllib2, re, sys, math
import elementtree.ElementTree as ET
import xbmcaddon

scriptID = sys.modules[ "__main__" ].scriptID
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.28'
HISTORYFILE = ptv.getAddonInfo('path') + os.path.sep + "searchhistory.xml"

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

    def checkDir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
            
	
class history:
    def __init__(self):
        pass
    
    
    def readHistoryFile(self):
	file = open(HISTORYFILE, 'r')
	root = ET.parse(file).getroot()
	file.close()
	return root


    def writeHistoryFile(self, root):
	file = open(HISTORYFILE, 'w')
	ET.ElementTree(root).write(file)
	file.close() 


    def loadHistoryFile(self, service):
	if not os.path.isfile(HISTORYFILE):
	    self.makeHistoryFile(service)
	history = self.parseHistoryFile(service)
	return history
    

    def addHistoryItem(self, service, item):
	if not os.path.isfile(HISTORYFILE):
	    self.makeHistoryFile(service)
	strTab = []
	root = self.readHistoryFile()
	#check if item already exists
	exists = False
	for node in root.getiterator(service):
	    for child in node.getchildren():
		if child.text != None:
		    strTab.append(child.text)
		else:
		    strTab.append('')
		if child.text == item:
		    exists = True
	    if not exists:
		print "tab: " + str(strTab)
		i=0
		for node in root.getiterator(service):
		    for child in node.getchildren():
			if i==0: child.text = item
			else: child.text = strTab[i-1]
			i = i + 1
		self.writeHistoryFile(root)
		
		
    def clearHistoryItems(self, service):
	root = self.readHistoryFile()
	for node in root.getiterator(service):
	    for child in node.getchildren():
		child.text = ''
	self.writeHistoryFile(root)


    def parseHistoryFile(self, service):
	strTab = []
	root = self.readHistoryFile()
	serviceList = root.findall(service)
	if len(serviceList) == 0:
	    child = ET.Element(service)
	    root.append(child)   
	    for i in range(5):
		item = ET.Element('search')
		child.append(item)
	    self.writeHistoryFile(root)
	    
	for node in root.getiterator(service):
	    for child in node.getchildren():
		if child.text != None:
		    strTab.append(child.text)
		else:
		    strTab.append('')
	return strTab

    
    def makeHistoryFile(self, service):
	root = ET.Element('history')
	child = ET.Element(service)
	root.append(child)   
	for i in range(5):
	    item = ET.Element('search')
	    child.append(item)
	self.writeHistoryFile(root)

