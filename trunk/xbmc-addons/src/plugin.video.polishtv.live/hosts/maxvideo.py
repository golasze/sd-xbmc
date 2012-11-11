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

mainUrl = 'http://maxvideo.pl'
logoUrl = mainUrl + '/refresh140820/style/img/maxVideo.png'


HOST = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


class Maxvideo:
  def __init__(self):
    log.info('Loading Maxvideo')
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.up = urlparser.urlparser()
    self.cm = pCommon.common()

    
  def getMenuTable(self):
    nTab = []
    data = self.cm.requestData(mainUrl)
    match = re.compile('<li.+?>\n.+?<a href="(.+?)">(.+?)</a>\n.+?</li>').findall(data)
    if len(match) > 0:
      nTab = match	
    return nTab
  
  
  def getMovieTab(self, url):
    log.info("reading: " + url)
    strTab = []
    valTab = []
    data = self.cm.requestData(url)
    match = re.compile("""<h1 class="indexVideoTitle">.+?</a>(.+?)<br/>""").findall(data)
    if len(match) > 0:
      titles = match
    else:
      titles = []
 
    #file: "http://s171.maxvideo.pl/flv/unlimited/3d/3d19a5515e4e6e77e37d6a443b83a76e.flv",
    match = re.compile("""file: "(.+?)",\n.+?,\n.+?,\n.+?,\n.+?,\n.+?'(.+?)'""").findall(data)
    if len(match) > 0:
      for i in range(len(match)):
	value = match[i]
	strTab.append(titles[i])
	strTab.append(value[0])
	strTab.append(value[1])	
	valTab.append(strTab)
	strTab = []
    
    #pokaz wiecej
    match = re.compile("""<span class="navFont">\&raquo;</span>""").findall(data) 
    if len(match) > 0:
      strTab.append('pokaz wiecej')
      strTab.append('')
      strTab.append('')
      valTab.append(strTab)
    #[title, url, image]
    return valTab
  

  def listsAddLinkMovie(self, table, category, page):
    if page == 'None':
      page = 1
    else:
      page = int(page)
    page = str (page + 1)
    
    for i in range(len(table)):
      value = table[i]
      title = value[0]
      url = value[1]
      iconimage = value[2]
      if title == 'pokaz wiecej':
	url = category + page
	self.add('maxvideo', title, category, page, title, iconimage, url, True, False)
      else:
	self.add('maxvideo', 'playSelectedMovie', 'movie', 'None', title, iconimage, url, False, True)	
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
  
  def listsAddDirMenu(self, table):
    for i in range(len(table)):
      if not 'kategoria' in table[i][0]:
	category = table[i][0] + '/kategoria/'
      else:
	category = table[i][0] + '/'
      print category
      n = table[i][1]
      self.add('maxvideo', n, category, 'None', 'None', logoUrl, category, True, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def add(self, service, name, category, page, title, iconimage, url, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&category=" + urllib.quote_plus(category) + "&page=" + urllib.quote_plus(page) + "&url=" + urllib.quote_plus(url)
    #"&title=" + urllib.quote_plus(title) + 
    #log.info(str(u))
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
    
    log.info('nazwa: ' + name)
    log.info('cat: ' + category)
    log.info('page: ' + page)
    log.info('url: ' + url)
  	
    if name == 'None':
      self.listsAddDirMenu(self.getMenuTable())
    else:
      if name <> 'playSelectedMovie':
	self.listsAddLinkMovie(self.getMovieTab(url), category, page)
      else:	
      #odtwarzaj video
	self.LOAD_AND_PLAY_VIDEO(url) 	

