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

import pLog, settings, Parser, pCommon

log = pLog.pLog()

mainUrl = 'http://maxvideo.pl'
logoUrl = mainUrl + '/refresh140820/style/img/maxVideo.png'
apiLogin = mainUrl + '/api/login.php'
apiFrontList = mainUrl + '/api/front_list.php'
apiVideoUrl = mainUrl + '/api/get_link.php'
authKey = 'key=8d00321f70b85a4fb0203a63d8c94f97'

SERVICE = 'maxvideo'
COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + SERVICE +".cookie"

login = ptv.getSetting('maxvideo_login')
password = ptv.getSetting('maxvideo_password')


class Maxvideo:
  def __init__(self):
    log.info('Loading ' + SERVICE)
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.cm = pCommon.common()
    self.api = API()
    self.api.Login()


  def getFrontListTable(self):
    strTab = []
    valTab = []
    query_data = {'url': apiFrontList, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True}
    response = self.cm.getURLRequestData(query_data)
    result = simplejson.loads(response)  
    for majorkey, value in result.iteritems():
      for subkey, v in value.iteritems():
	    strTab.append(v)
      valTab.append(strTab)
      strTab = []
    return valTab


  def getMenuTable(self):
    valTab = []
    nTab = self.getFrontListTable() 
    for i in range(len(nTab)):
      if not nTab[i][0] in valTab:
	valTab.append(nTab[i][0])
    return valTab
 
  
  def getMovieTab(self, name):
    valTab = []
    strTab = []
    nTab = self.getFrontListTable()
    for i in range(len(nTab)):
      if nTab[i][0].encode('UTF-8') == name:
	strTab.append(nTab[i][1])
	strTab.append(nTab[i][2])
	valTab.append(strTab)
      strTab = []    
    #[hash, title]
    return valTab
  
  
  def addList(self, table, category):
    if category == 'movie':
      for i in range(len(table)):
	self.add(SERVICE, 'playSelectedMovie', category, 'None', table[i][1].encode('UTF-8'), logoUrl, table[i][0], False, True)
    if category == 'main-menu':
      for i in range(len(table)):
	print table[i].encode('UTF-8')
	self.add(SERVICE, table[i].encode('UTF-8'), category, 'None', table[i].encode('UTF-8'), logoUrl, 'None', True, False)      
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
  

  def add(self, service, name, category, page, title, iconimage, url, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&category=" + urllib.quote_plus(category) + "&page=" + urllib.quote_plus(page) + "&url=" + urllib.quote_plus(url)
    if name == 'playSelectedMovie':
    	name = title
    if iconimage == '':
    	iconimage = "DefaultVideo.png"
    liz=xbmcgui.ListItem(name.decode('utf-8'), iconImage=iconimage, thumbnailImage=iconimage)
    if isPlayable:
	liz.setProperty("IsPlayable", "true")
    liz.setInfo('video', {'title' : title.decode('utf-8')} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
  

  def LOAD_AND_PLAY_VIDEO(self, videoUrl):
    ok=True
    if videoUrl == '':
      d = xbmcgui.Dialog()
      d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
    try:
      log.info ("playing: " + videoUrl)
      xbmcPlayer = xbmc.Player()
      xbmcPlayer.play(videoUrl)
    except:
      d = xbmcgui.Dialog()
      d.ok('Blad przy przetwarzaniu.', 'Najprawdopodobniej video zostalo usuniete')        
    return ok


  def handleService(self):
    params = self.parser.getParams()
    name = str(self.parser.getParam(params, "name"))
    title = str(self.parser.getParam(params, "title"))
    category = str(self.parser.getParam(params, "category"))
    page = str(self.parser.getParam(params, "page"))
    url = str(self.parser.getParam(params, "url"))
    name = name.replace("+", " ")
    category = category.replace("+", " ")
    page = page.replace("+", " ")
    
    if name == 'None':
      self.addList(self.getMenuTable(),'main-menu')
    else:
      if name <> 'playSelectedMovie':
	self.addList(self.getMovieTab(name),'movie')
      else:	
	videoUrl = self.api.getVideoUrl(url, False)
	self.LOAD_AND_PLAY_VIDEO(videoUrl) 	


class API:
  def __init__(self):
    self.cm = pCommon.common()
  
  
  def Login(self):
    self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    if login=='':
	log_error = False
	log_desc = 'Nie zalogowano'
    else:
	query_data = {'url': apiLogin, 'use_host': False, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIEFILE, 'use_post': True, 'return_data': True}
	data = self.cm.getURLRequestData(query_data, {'login' : login, 'password' : password})
	result = simplejson.loads(data)	  
	try:
	    if (result['error']):
	      	log_error = True
		log_desc = result['error'].encode('UTF-8')
	except:
	    log_error = False
	    log_desc = result['ok']	  

  #videoHash - 8 or 16 char video hash
  #notify - Ture/False; premium notification. if no premium, notification will show anyway
  def getVideoUrl(self, videoHash, notify):
    query_data = { 'url': apiVideoUrl, 'use_host': False, 'use_cookie': True, 'load_cookie': True, 'save_cookie': False, 'cookiefile': COOKIEFILE, 'use_post': True, 'return_data': True }
    data = self.cm.getURLRequestData(query_data, {'v' : videoHash, 'key' : authKey})
    result = simplejson.loads(data)
    result = dict([(str(k), v) for k, v in result.items()])
      
    log_desc = ''
    log_dec2 = ''
    try:
      if (result['error']): return videoUrl
    except:
      if (result['premium']):
	premium_until = result['premium_until'].split(' ')
	log_desc2 = 'premium aktywne do ' + premium_until[0]
	log_time = 15000
      else:
	notify = True
	if (log_error): log_desc2 = 'sprawdz ustawienia wtyczki'
	else: log_desc2 = 'wykup konto premium maxvideo.pl by w pelni korzystac z serwisu'
	log_time = 30000
      notification = '(' + log_desc + ',' + log_desc2 + ',' + str(log_time) + ')'
      videoUrl = result['ok'].encode('UTF-8')
    if notify: xbmc.executebuiltin("XBMC.Notification" + notification +'"')
    return videoUrl