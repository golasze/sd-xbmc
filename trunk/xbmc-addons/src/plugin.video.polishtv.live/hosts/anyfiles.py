# -*- coding: utf-8 -*-
import os, string, cookielib, StringIO
import time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, urlparser, pCommon

log = pLog.pLog()

HOST = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
SERVICENAME = 'anyfiles'
MAINURL = 'http://video.anyfiles.pl'
IMGURL = MAINURL + '/img/nlogo.png'
NEW_LINK = MAINURL + '/najnowsze/0'
HOT_LINK = MAINURL + '/najpopularniejsze/0'

SERVICE_MENU_TABLE = { 1: "Kategorie",
			2: "Najnowsze",
			3: "Popularne",
			4: "Szukaj",
			5: "Historia Wyszukiwania"}
			


class AnyFiles:
  def __init__(self):
    log.info('Loading ' + SERVICENAME)
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.up = urlparser.urlparser()
    self.common = pCommon.common()
    self.history = pCommon.history()
    
 
  def setTable(self):
    return SERVICE_MENU_TABLE
    
    
  def getMenuTable(self):
    nTab = []
    for num, val in SERVICE_MENU_TABLE.items():
      nTab.append(val)
    return nTab
   
    
  def searchInputText(self):
    text = None
    k = xbmc.Keyboard()
    k.doModal()
    if (k.isConfirmed()):
      text = k.getText()
    return text  
  
  
  def searchTab(self, text):
    strTab = []
    valTab = []
    searchUrl = MAINURL + '/Search.jsp'
    values = { 'q': text, 'oe': 'polish' }
    headers = { 'User-Agent' : HOST }
    data = urllib.urlencode(values)
    req = urllib2.Request(searchUrl, data, headers)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('src="(.+?)" class="icon-img "></a>.+?<a class="box-title" href="(.+?)">(.+?)</a></td></tr>').findall(link)
    if len(match) > 0:
      for i in range(len(match)):
	value = match[i]
	strTab.append(value[2])
	strTab.append(MAINURL + value[1])
	strTab.append(value[0])	
	valTab.append(strTab)
	strTab = []
    return valTab
     
    
  def getCategories(self):
    valTab = []
    strTab = []
    link = self.common.requestData(MAINURL)
    match = re.compile('<tr><td><a href="(.+?)" class="kat-box-title">.+?</a></td></tr>').findall(link)
    if len(match) > 0:
      for i in range(len(match)):	
	c = match[i].split('/')
	#cat = c[1].replace('+',' ')
	strTab.append(c[1].replace('+',' '))
	strTab.append(MAINURL + match[i])
	valTab.append(strTab)
	strTab = []
    return valTab 
    
  
  def getMovieTab(self, url):
    strTab = []
    valTab = []
    link = self.common.requestData(url)
    match = re.compile('src="(.+?)".+?(?:\n|\r\n?).+?(?:\n|\r\n?).+?(?:\n|\r\n?)<tr><td><a href="(.+?)" class="kat-box-name">(.+?)</a>', re.MULTILINE).findall(link)
    if len(match) > 0:
      for i in range(len(match)):
	value = match[i]
	strTab.append(value[2])
	strTab.append(MAINURL + value[1])
	strTab.append(value[0])	
	valTab.append(strTab)
	strTab = []
      match = re.search('Paginator.+?,(.+?), 8, (.+?),',link)
    if match:
      if int(match.group(2)) < int(match.group(1)):
	p = url.split('/')
	size = len(p)
	nextpage = (int(match.group(2))+1) * 20
	strTab.append("pokaz wiecej")
	if len(p) == 7:
	  strTab.append(MAINURL + "/" + p[3] + "/" + p[4] + "/" + p[5] + "/" + str(nextpage))
	else:
	  strTab.append(MAINURL + "/" + p[3] + "/" + str(nextpage))	  
	strTab.append("")
	valTab.append(strTab)
    return valTab
  
   
  def listsAddLinkMovie(self, table):
    for i in range(len(table)):
      value = table[i]
      title = value[0]
      url = value[1]
      iconimage = value[2]
      if title == 'pokaz wiecej':
	self.add(SERVICENAME, title, 'movie', 'None', title, iconimage, url, True, False)
      else:
	self.add(SERVICENAME, 'playSelectedMovie', 'movie', 'None', title, iconimage, url, True, False)	
    #zmien view na "Thumbnail"
    xbmcplugin.setContent(int(sys.argv[1]),'movies')
    xbmc.executebuiltin("Container.SetViewMode(500)")    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
  
  def listsAddDirMenu(self, table, name, category, page):
    for i in range(len(table)):
      if name == 'None':
	self.add(SERVICENAME, table[i], 'None', 'None', table[i], IMGURL, 'None', True, False)
      if name == 'category':
	self.add(SERVICENAME, table[i][0], table[i][0], 'None', table[i][0], 'None', table[i][1], True, False)
    #zmien view na "List"
    xbmcplugin.setContent(int(sys.argv[1]),'movies')
    xbmc.executebuiltin("Container.SetViewMode(502)")    	
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

  def listsHistory(self, table):
    print str(table)
    for i in range(len(table)):
      print str(table[i])
      if table[i] <> '':
	self.add(SERVICENAME, table[i], 'history', 'None', table[i], IMGURL, 'None', True, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
  def add(self, service, name, category, page, title, iconimage, url, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&category=" + urllib.quote_plus(category) + "&page=" + urllib.quote_plus(page) + "&title=" + urllib.quote_plus(title) + "&url=" + urllib.quote_plus(url)
    #log.info(str(u))
    if name == 'playSelectedMovie':
    	name = title
    if iconimage == '':
    	iconimage = "DefaultVideo.png"
    liz=xbmcgui.ListItem(name.decode('iso8859-2'), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if isPlayable:
	liz.setProperty("IsPlayable", "true")
    liz.setInfo('video', {'title' : title.decode('iso8859-2')} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
  

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
      d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')		
    return ok
    

  def handleService(self):
    params = self.parser.getParams()
    name = str(self.parser.getParam(params, "name"))
    title = str(self.parser.getParam(params, "title"))
    category = str(self.parser.getParam(params, "category"))
    page = str(self.parser.getParam(params, "page"))
    url = str(self.parser.getParam(params, "url"))
    name = name.replace("+", " ")
    title = title.replace("+", " ")
    category = category.replace("+", " ")
    page = page.replace("+", " ")
    
    #log.info('nazwa: ' + name)
    #log.info('cat: ' + category)
    #log.info('page: ' + page)
    #log.info('tytuł: ' + title)
    #log.info('url: ' + url)
  	
    if name == 'None':
      self.listsAddDirMenu(self.getMenuTable(), 'None', 'None', 'None')
    #Kategorie
    if name == self.setTable()[1]:
      self.listsAddDirMenu(self.getCategories(), 'category', 'None', 'None')      
    #Najnowsze
    if name == self.setTable()[2]:
      self.listsAddLinkMovie(self.getMovieTab(NEW_LINK))
    #Popularne	
    if name == self.setTable()[3]:
      self.listsAddLinkMovie(self.getMovieTab(HOT_LINK))      
    #lista tytulow w kategorii
    if category != 'None' and url != 'None' and name != 'playSelectedMovie':
      self.listsAddLinkMovie(self.getMovieTab(url))
    #Szukaj
    if name == self.setTable()[4]:
      text = self.searchInputText()
      if text != None:
	self.history.addHistoryItem(SERVICENAME, text)
	self.listsAddLinkMovie(self.searchTab(text))
    #Historia Wyszukiwania
    if name == self.setTable()[5]:
      t = self.history.loadHistoryFile(SERVICENAME)
      self.listsHistory(t)
    if category == 'history':
      self.listsAddLinkMovie(self.searchTab(name))
    
    #odtwarzaj video
    if name == 'playSelectedMovie':
      urlLink = self.up.getVideoLink(url)
      log.info("urlLink: "+ urlLink)
      self.LOAD_AND_PLAY_VIDEO(urlLink) 

