# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()

mainUrl = 'http://video.anyfiles.pl'

ANYFILES_MENU_TABLE = { 1: "Podział według kategorii",
			2: "Najnowsze",
			3: "Popularne" }
			

HOST = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

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
	    req.add_header('User-Agent', HOST)
	    response = urllib2.urlopen(req)
	    link = response.read()
	    response.close()
	    tabURL = link.replace('\t', '').split('\n')
	    for line in tabURL:
	    	#log.info(line)
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


  def getMovieTab(self, url):
  	strTab = []
  	valTab = []
  	req = urllib2.Request(url)
  	req.add_header('User-Agent', HOST)
  	response = urllib2.urlopen(req)
  	link = response.read()
  	response.close()
  	match = re.compile('<tr><td align="center"><img class="items_img" title="<span>.+?</span>(.+?)<br><span>.+?</span>.+?<br><span>.+?</span>.+?<br><span>.+?</span>.+?<br><span.+?</span>.+?<br><span>.+?</span>.+?<br><span>.+?</span>.+?<br><span>.+?</span>.+?"  onclick="javascript:window.open\(\'(.+?)\',\'\',\'\'\)" src="(.+?)"  alt=".+?"></td></tr>').findall(link)
  	if len(match) > 0:
  		for i in range(len(match)):
  			value = match[i]
  			#log.info(str(value))
  			strTab.append(value[0])
  			strTab.append(mainUrl + value[1])
  			strTab.append(value[2])
  			valTab.append(strTab)
  			strTab = []
  	#log.info(str(valTab))
  	return valTab
  
  
  def getMovieNames(self, url):
  	out = []
  	tab = self.getMovieTab(url)
  	for i in range(len(tab)):
  		value = tab[i]
  		out.append(value[0])
  	return out
  

  def getMovieURL(self, url, key):
  	link = ''
  	tab = self.getMovieTab(url)
  	for i in range(len(tab)):
  		value = tab[i]
  		if key in value[0]:
  			link = value[1]
  			break
  	return link


  def videoMovieLink(self, url):
  	req = urllib2.Request(url)
  	req.add_header('User-Agent', HOST)
  	response = urllib2.urlopen(req)
  	link = response.read()
  	log.info(link)
  	response.close()
  	match = re.compile('<param name="flashvars" value="config={.+?;(.+?)&quot;.+?}"></object></div>').findall(link)
  	if len(match) == 1:
  		log.info(str(match[0]))
  		return match[0]
  		 	


  def listsMenu(self, table, title):
    value = ''
    if len(table) > 0:
      d = xbmcgui.Dialog()
      choice = d.select(title, table)
      for i in range(len(table)):
        #log.info(table[i])
        if choice == i:
            value = table[i]
    return value


  def listsTable(self, table):
    nTab = []
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def LOAD_AND_PLAY_VIDEO(self, videoUrl):
  	ok=True
  	if videoUrl == '':
		d = xbmcgui.Dialog()
		d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
		return False
	try:
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(videoUrl)
	except:
		d = xbmcgui.Dialog()
		d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')		
	return ok
    

  def handleService(self):
   	cm = self.listsMenu(self.getMenuTable(), "Wybór")
   	if cm == self.setTable()[1]:
   		category = self.listsMenu(self.getCategoryName(), "Wybór kategorii")
   		if category != '':
   			mm = self.listsMenu(self.getMovieNames(self.getCategoryURL(category)), "Wybór tytułu")
   			if mm != '':
   				urlLink = self.getMovieURL(self.getCategoryURL(category), mm)
   				#urlLink = self.getCategoryURL(category)
   				log.info(urlLink)
   				if urlLink.startswith('http://'):
   					log.info(self.videoMovieLink(urlLink))
   					self.LOAD_AND_PLAY_VIDEO(self.videoMovieLink(urlLink))
   					
   		
   	
