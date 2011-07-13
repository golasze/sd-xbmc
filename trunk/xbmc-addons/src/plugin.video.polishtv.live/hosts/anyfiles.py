# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, megavideo

log = pLog.pLog()

mainUrl = 'http://video.anyfiles.pl'

ANYFILES_MENU_TABLE = { 1: "Podział według kategorii",
			2: "Najnowsze",
			3: "Popularne" }
			

class AnyFiles:
  def __init__(self):
    log.info('Loading AnyFiles')
    
    
  def setTable(self):
    return ANYFILES_MENU_TABLE
    
    
  def getMenuTable(self):
    nTab = []
    for num, val in ANYFILES_MENU_TABLE.items():
      nTab.append(val)
    return nTab
    
    
  def getCategories(self):
    valTab = []
    strTab = []
    url = mainUrl
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      expr = re.match(r'.+?<li><a href="(.+?)">(.+?)</a></li>$', line, re.M|re.I)
      if expr:
	strTab.append(mainUrl + expr.group(1))
	strTab.append(expr.group(2))
	#log.info(str(strTab))
	valTab.append(strTab)
	strTab = []
    return valTab 
    

  def getCategoryName(self):
    nameTab = []
    origTab = self.getCategories()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      nameTab.append(name)
    nameTab.sort()
    return nameTab
    
    
  def getCategoryURL(self, key):
    link = ''
    origTab = self.getCategories()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      if key in name:
	link = value[0]
	break
    return link
    
    
