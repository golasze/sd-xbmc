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

HOST = 'XBMC'
SERVICE = 'poplertv'

mainUrl = 'http://www.popler.tv'
apiLiveList = mainUrl + '/api/live_list.php'
apiVOD = mainUrl + '/api/vod.php'

SERVICE_MENU_TABLE = {
                        1: "Telewizja na żywo",
			2: "Najnowsze nagrania",
			3: "Najpopularniejsze nagrania",
			4: "Polecane nagrania",}


class poplertv:
  def __init__(self):
    log.info('Loading ' + SERVICE)
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.common = pCommon.common()
    
    
  def setTable(self):
    return SERVICE_MENU_TABLE


  def getMenuTable(self):
    nTab = []
    for num, val in SERVICE_MENU_TABLE.items():
      nTab.append(val)
    return nTab

      
  def getVideoTable(self, url):
    strTab = []
    valTab = []
    query_data = {'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True}
    response = self.common.getURLRequestData(query_data)
    result = simplejson.loads(response)  
    for channel in result:
      name = channel['name'].encode('UTF-8')
      if name == '':
	path = channel['path'].split('/')
	name = path[-1]
      strTab.append(name)
      strTab.append(channel['thumb'])
      strTab.append(channel['rtmp'])
      
      if 'error' in channel:
	if channel['error'] != None: strTab.append(channel['error'].encode('UTF-8'))
	else: strTab.append('')
      else: strTab.append('')	
      
      valTab.append(strTab)
      strTab = []

    #[name,icon,rtmp,error_msg]
    return valTab


  def addList(self, table, category):
    for i in range(len(table)):
      if category == 'video':
        self.add(SERVICE, 'playSelectedMovie', table[i][0], table[i][1], table[i][2], table[i][3], False, False)
      else:
	iconimage = os.path.join(ptv.getAddonInfo('path'), "images/") + SERVICE + '.png'
	self.add(SERVICE, table[i], table[i], iconimage, '', '', True, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def add(self, service, name, title, iconimage, url, error, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)+ "&title=" + urllib.quote_plus(title)+ "&error=" + urllib.quote_plus(error)
    print u
    if name == 'playSelectedMovie': name = title
    if error != '': label = "[COLOR FFFF0000]" + name + "[/COLOR]"
    else: label = name
    liz=xbmcgui.ListItem(label, iconImage=iconimage, thumbnailImage=iconimage)
    if isPlayable: liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": title } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
 
 
  def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, error):
    log.info(error)
    ok=True
    if videoUrl == '' or error != '':
      d = xbmcgui.Dialog()
      if error != '':
	msg = self.common.formatDialogMsg(error)
        d.ok('popler.tv',msg[0], msg[1], msg[2])
      else:	
	d.ok('Nie znaleziono streamingu', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas.')
      return False
    thumbnail = xbmc.getInfoImage("ListItem.Thumb")
    liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    liz.setInfo( type="Video", infoLabels={ "Title": title } )
    try:
      xbmcPlayer = xbmc.Player()
      xbmcPlayer.play(videoUrl, liz)
    except:
      d = xbmcgui.Dialog()
      d.ok("Błąd", "Odtwarzanie wstrzymane", "z powodu błędnego linku rtmp")        
    return ok
  
  
  def handleService(self):
    params = self.parser.getParams()
    name = str(self.parser.getParam(params, "name"))
    title = str(self.parser.getParam(params, "title"))
    url = str(self.parser.getParam(params, "url"))
    error = str(self.parser.getParam(params, "error"))

    if name == 'None':
      self.addList(self.getMenuTable(), 'menu')  
    if name == self.setTable()[1]:
      self.addList(self.getVideoTable(apiLiveList), 'video')
    if name == self.setTable()[2]:
      self.addList(self.getVideoTable(apiVOD + '?func=nowe'), 'video')
    if name == self.setTable()[3]:
      self.addList(self.getVideoTable(apiVOD + '?func=popularne'), 'video')
    if name == self.setTable()[4]:
      self.addList(self.getVideoTable(apiVOD + '?func=polecane'), 'video')
    if name == 'playSelectedMovie':
      self.LOAD_AND_PLAY_VIDEO(url, title, error)
      
