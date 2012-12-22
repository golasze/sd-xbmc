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
notification = ptv.getSetting('maxvideo_notify')


class Maxvideo:
  def __init__(self):
    log.info('Loading ' + SERVICE)
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.cm = pCommon.common()
    self.api = API()


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
    if notification == 'true': notify = True
    else: notify = False
    
    if name == 'None':
      self.api.Login(login, password, notify)
      self.addList(self.getMenuTable(),'main-menu')
    else:
      if name <> 'playSelectedMovie':
	self.addList(self.getMovieTab(name),'movie')
      else:	
	videoUrl = self.api.getVideoUrl(url, COOKIEFILE, notify)
	self.LOAD_AND_PLAY_VIDEO(videoUrl) 	


class API:
  def __init__(self):
    self.cm = pCommon.common()
  
  
  def Login(self, username, password, notification):
    self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    if login=='':
	uname = ''
	log_desc = 'Nie zalogowano'
	log_time = 10000
	retVal = False
    else:
	uname = username + ': '
	query_data = {'url': apiLogin, 'use_host': False, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIEFILE, 'use_post': True, 'return_data': True}
	data = self.cm.getURLRequestData(query_data, {'login' : username, 'password' : password})
	result = simplejson.loads(data)
	if 'error' in result:
	    log_desc = result['error'].encode('UTF-8')
	    log_time = 20000
	    retVal = False
	else:
	    log_desc = result['ok']
	    log_time = 5000
	    retVal = True
    if notification:

      notification = '(maxvideo.pl,' + uname + log_desc + ',' + str(log_time) + ')'
      xbmc.executebuiltin("XBMC.Notification" + notification +'"')
    return retVal
      

  def getVideoUrl(self, videoHash, cookiefile, notification):
    if cookiefile == '': load_cookie = False
    else: load_cookie = True
    query_data = { 'url': apiVideoUrl, 'use_host': False, 'use_cookie': True, 'load_cookie': load_cookie, 'save_cookie': False, 'cookiefile': cookiefile, 'use_post': True, 'return_data': True }
    data = self.cm.getURLRequestData(query_data, {'v' : videoHash, 'key' : authKey})
    result = simplejson.loads(data)
    result = dict([(str(k), v) for k, v in result.items()])
    log.info(str(result))
    if 'error' in result: videoUrl = ''
    else:
      if (not result['premium']):
	if notification:   
	  xbmc.executebuiltin("XBMC.Notification(maxvideo.pl,wykup konto premium by w pelni korzystac z serwisu,15000)")
      videoUrl = result['ok'].encode('UTF-8')
    return videoUrl