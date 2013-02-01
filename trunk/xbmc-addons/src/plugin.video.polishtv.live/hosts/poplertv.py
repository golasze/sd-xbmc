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

mainUrl = 'http://www.popler.tv'
apiLiveList = mainUrl + '/api/live_list.php'

SERVICE = 'poplertv'

class poplertv:
  def __init__(self):
    log.info('Loading ' + SERVICE)
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.common = pCommon.common()


  def getLiveListTable(self):
    strTab = []
    valTab = []
    query_data = {'url': apiLiveList, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True}
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
      valTab.append(strTab)
      strTab = []
    valTab.sort(key = lambda x: x[3], reverse=True)
    #[name,icon,rtmp,views]
    return valTab


  def addList(self, table):
    for i in range(len(table)):
      self.add(SERVICE, 'playSelectedMovie', table[i][0], table[i][1], table[i][2], False, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def add(self, service, name, title, iconimage, url, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)+ "&title=" + urllib.quote_plus(title)
    if name == 'playSelectedMovie': name = title
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    if isPlayable: liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": title } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
 
 
  def LOAD_AND_PLAY_VIDEO(self, videoUrl, title):
    ok=True
    if videoUrl == '':
      d = xbmcgui.Dialog()
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


    if name == 'None':
      self.addList(self.getLiveListTable())
    if name == 'playSelectedMovie':
      self.LOAD_AND_PLAY_VIDEO(url, title)
      
