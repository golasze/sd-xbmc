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

SERVICE_MENU_TABLE = {
                        1: "Telewiza na zywo",
			2: "Najnowsze",
			3: "Najpopularniejsze"}


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


  def getLiveListTable(self):
    strTab = []
    valTab = []
    query_data = {'url': apiLiveList, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True}
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
      strTab.append(int(channel['concurents_views'].encode('UTF-8')))
      if channel['error'] != None: strTab.append(channel['error'].encode('UTF-8'))
      else: strTab.append('')
      valTab.append(strTab)
      strTab = []
    valTab.sort(key = lambda x: x[3], reverse=True)
    #[name,icon,rtmp,views,error_msg]
    return valTab


  def addList(self, table, category):
    for i in range(len(table)):
      if category == 'video':
        self.add(SERVICE, 'playSelectedMovie', table[i][0], table[i][1], table[i][2], table[i][4], False, False)
      else:
	self.add(SERVICE, table[i], table[i], '', '', '', True, False)
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
        d.ok('popler.tv','Dostęp do video jest płatny, obecnie można', 'oglądać go wyłącznie na stronie WWW')
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
      self.addList(self.getLiveListTable(), 'video')
      
    if name == self.setTable()[2]:
      print "waiting for API"
      #self.addList(self.getMovieTable('najnowsze'), 'video')
    if name == self.setTable()[3]:
      print "waiting for API"
      #self.addList(self.getMovieTable('najnowsze'), 'video')
    if name == 'playSelectedMovie':
      self.LOAD_AND_PLAY_VIDEO(url, title, error)
      
