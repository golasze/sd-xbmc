# -*- coding: utf-8 -*-
import os, string, cookielib, StringIO
import time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import simplejson

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, pCommon, xppod

log = pLog.pLog()

SERVICE = 'anyfiles'
THUMB_SERVICE = os.path.join(ptv.getAddonInfo('path'), "images/") + SERVICE + '.png'
THUMB_NEXT = os.path.join(ptv.getAddonInfo('path'), "images/") + 'dalej.png'
THUMB_PREV = os.path.join(ptv.getAddonInfo('path'), "images/") + 'wroc.png'
COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + SERVICE +".cookie"

MAINURL = 'http://video.anyfiles.pl'
SEARCHURL = MAINURL + '/Search.jsp'
NEW_LINK = MAINURL + '/najnowsze/0'
HOT_LINK = MAINURL + '/najpopularniejsze/0'

SERVICE_MENU_TABLE = { 1: "Kategorie",
			2: "Najnowsze",
			3: "Popularne",
			4: "Szukaj",
			5: "Historia Wyszukiwania"}

			
dbg = ptv.getSetting('default_debug')

class AnyFiles:
  def __init__(self):
    log.info('Loading ' + SERVICE)
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.common = pCommon.common()
    self.history = pCommon.history()
    self.anyfiles = serviceParser()
    
 
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
    self.common.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    if SEARCHURL in text:
      query_data = {'url': text, 'use_host': False, 'use_cookie': True, 'load_cookie': True, 'save_cookie': False, 'cookiefile': COOKIEFILE, 'use_post': False, 'return_data': True}    
      data = self.common.getURLRequestData(query_data)
    else:  
      query_data = {'url': SEARCHURL, 'use_host': False, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIEFILE, 'use_post': True, 'return_data': True}
      data = self.common.getURLRequestData(query_data, {'q': text, 'oe': 'polish'})
   
    match = re.compile('src="(.+?)" class="icon-img "></a>.+?<a class="box-title" href="(.+?)">(.+?)</a></td></tr>').findall(data)
    if len(match) > 0:
      for i in range(len(match)):
	value = match[i]
	strTab.append(value[2])
	strTab.append(MAINURL + value[1])
	strTab.append(value[0])	
	valTab.append(strTab)
	strTab = []
      match = re.search('Paginator.+?,(.+?), 8, (.+?),',data)
      if match:
	if int(match.group(2)) < int(match.group(1)):
	  nextpage = (int(match.group(2))+1) * 18
	  nUrl = SEARCHURL + "?st=" + str(nextpage)
	  strTab.append("pokaz wiecej")
	  strTab.append(nUrl)	  
	  strTab.append(THUMB_NEXT)
	  valTab.append(strTab)
    return valTab
     
    
  def getCategories(self):
    valTab = []
    strTab = []

    query_data = { 'url': MAINURL, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    data = self.common.getURLRequestData(query_data)
    match = re.compile('<tr><td><a href="(.+?)" class="kat-box-title">.+?</a></td></tr>').findall(data)
    if len(match) > 0:
      for i in range(len(match)):	
	c = match[i].split('/')
	strTab.append(c[1].replace('+',' '))
	strTab.append(MAINURL + match[i])
	valTab.append(strTab)
	strTab = []
    return valTab 
    
  
  def getMovieTab(self, url):
    strTab = []
    valTab = []
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    data = self.common.getURLRequestData(query_data)
    match = re.compile('src="(.+?)".+?(?:\n|\r\n?).+?(?:\n|\r\n?).+?(?:\n|\r\n?)<tr><td><a href="(.+?)" class="kat-box-name">(.+?)</a>', re.MULTILINE).findall(data)
    if len(match) > 0:
      for i in range(len(match)):
	value = match[i]
	strTab.append(value[2])
	strTab.append(MAINURL + value[1])
	strTab.append(value[0])	
	valTab.append(strTab)
	strTab = []
      match = re.search('Paginator.+?,(.+?), 8, (.+?),',data)
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
	strTab.append(THUMB_NEXT)
	valTab.append(strTab)
    return valTab
  
   
  def listsAddLinkMovie(self, table):
    #name,url,iconimage
    for i in range(len(table)):
      value = table[i]
      if value[0] == 'pokaz wiecej':
	self.add(SERVICE, value[0], 'movie', 'None', value[0], value[2], value[1], True, False)
      else:
	self.add(SERVICE, 'playSelectedMovie', 'movie', 'None', value[0], value[2], value[1], True, False)	
    #zmien view na "Thumbnail"
    xbmcplugin.setContent(int(sys.argv[1]),'movies')
    xbmc.executebuiltin("Container.SetViewMode(500)")    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
  
  def listsAddDirMenu(self, table, name, category, page):
    for i in range(len(table)):
      if name == 'None':
	self.add(SERVICE, table[i], 'None', 'None', table[i], THUMB_SERVICE, 'None', True, False)
      if name == 'category':
	self.add(SERVICE, table[i][0], table[i][0], 'None', table[i][0], THUMB_SERVICE, table[i][1], True, False)
    #zmien view na "List"
    xbmcplugin.setContent(int(sys.argv[1]),'movies')
    xbmc.executebuiltin("Container.SetViewMode(502)")    	
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def listsHistory(self, table):
    for i in range(len(table)):
      if table[i] <> '':
	self.add(SERVICE, table[i], 'history', 'None', 'None', THUMB_SERVICE, 'None', True, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    

  def add(self, service, name, category, page, title, iconimage, url, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&category=" + urllib.quote_plus(category) + "&page=" + urllib.quote_plus(page) + "&title=" + urllib.quote_plus(title) + "&url=" + urllib.quote_plus(url)
    if name == 'playSelectedMovie':
    	name = title
    if iconimage == '':
    	iconimage = "DefaultVideo.png"
    liz=xbmcgui.ListItem(name.decode('UTF-8'), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if isPlayable:
	liz.setProperty("IsPlayable", "true")
    liz.setInfo('video', {'title' : title.decode('utf-8')} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
   

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
	self.history.addHistoryItem(SERVICE, text)
	self.listsAddLinkMovie(self.searchTab(text))
	
    if name == 'pokaz wiecej':
      self.listsAddLinkMovie(self.searchTab(url))
      
    #Historia Wyszukiwania
    if name == self.setTable()[5]:
      self.listsHistory(self.history.loadHistoryFile(SERVICE))
    if category == 'history':
      self.listsAddLinkMovie(self.searchTab(name))
    
    #odtwarzaj video
    if name == 'playSelectedMovie':
      videoUrl = self.anyfiles.getVideoUrl(url)
      if videoUrl != False:
	log.info("videoUrl: "+ videoUrl)
	self.common.LOAD_AND_PLAY_VIDEO(videoUrl, title)
  
      
class serviceParser:
    def __init__(self):
      self.cm = pCommon.common()
     
    
    def getVideoUrl(self,url):
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      #show adult content
      self.cm.addCookieItem(COOKIEFILE, {'name': 'AnyF18', 'value': 'mam18', 'domain': 'video.anyfiles.pl'}, False)
      
      query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'cookiefile': COOKIEFILE, 'load_cookie': True, 'save_cookie': True, 'use_post': False, 'return_data': True }
      data = self.cm.getURLRequestData(query_data)
      #var flashvars = {"uid":"player-vid-8552","m":"video","st":"c:1LdwWeVs3kVhWex2PysGP45Ld4abN7s0v4wV"};
      match = re.search("""var flashvars = {.+?"st":"(.+?)"}""",data)
      if match:
	nUrl = xppod.Decode(match.group(1)[2:]).encode('utf-8').strip()
	if 'http://' in nUrl: url2 = nUrl
	else: url2 = 'http://video.anyfiles.pl' + nUrl
	
	query_data = { 'url': url2+ "&ref=" +urllib.quote_plus(url), 'use_host': False, 'use_cookie': True, 'cookiefile': COOKIEFILE, 'load_cookie': True, 'save_cookie': False, 'use_post': False, 'return_data': True }
	data = self.cm.getURLRequestData(query_data)
	data = xppod.Decode(data).encode('utf-8').strip()

	#json cleanup
	while data[-2:] != '"}': data = data[:-1]
	result = simplejson.loads(data)
	if (result['ytube']=='0'):
	  vUrl = result['file'].split("or")
	  return vUrl[0]
	else:
	  p = result['file'].split("/")
          if 'watch' in p[3]: videoid = p[3][8:19]
	  else: videoid = p[3]
	  plugin = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + videoid
	  return plugin
      return False  
