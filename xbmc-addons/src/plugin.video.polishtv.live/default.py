# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( os.getcwd(), "hosts" ) )

import pLog, settings, weebtv, ekinotv, anyfiles, itvp

log = pLog.pLog()


TV_ONLINE_TABLE = { 1: "Weeb TV [wyświetl kanały]",
		    2: "Justin TV [wyświetl kanały]" }

VOD_ONLINE_TABLE = { 1: "Ekino TV [filmy, seriale]",
		     2: "iTVP [filmy, seriale, vod]",
		     3: "AnyFiles [różne filmy]",
		     4: "IPLEX" }



class PolishLiveTV:
  def __init__(self):
    log.info('Starting Polish Live TV')
    self.settings = settings.TVSettings()


  def showListOptions(self):
    mode = str(self.settings.paramMode)
    log.info( 'mode: ' + str(mode))
    if mode == 'None':
      log.info('Wyświetlam kategorie')
      self.CATEGORIES()
    elif mode == '1':
      menu = self.listsMenu(self.listsTable(TV_ONLINE_TABLE), "Wybór z listy")
      if menu == TV_ONLINE_TABLE[1]:
	  	tv = weebtv.WeebTV()
	  	tv.handleService()
      elif menu == TV_ONLINE_TABLE[2]:
	#rtmp = 'rtmp://199.9.255.45/app swfUrl=http://www-cdn.justin.tv/widgets/live_site_player.r34305490c2b0abacd260523181fc486d496372ee.swf pageUrl=http://pl.justin.tv/akisla live=true'
	rtmp = 'http://195.245.213.202/snode14/eaf92f195c6aa949-5a810d9fd83d06bb-bdb68c032c5a3917.ranczo-odc-1-spadek-vegas..wmv'
	self.LOAD_AND_PLAY_VIDEO(rtmp)
    elif mode == '2':
      log.info('Wejście do TV internetowej')
      menu = self.listsMenu(self.listsTable(VOD_ONLINE_TABLE), "Wybór z listy")
      if menu == VOD_ONLINE_TABLE[1]:
	  	   vod = ekinotv.EkinoTV()
	  	   vod.handleService()

      if menu == VOD_ONLINE_TABLE[2]:
	  	   vod = itvp.iTVP()
	  	   vod.handleService()
	
      #if menu == VOD_ONLINE_TABLE[4]:

      if menu == VOD_ONLINE_TABLE[4]:
		  self.LOAD_AND_PLAY_VIDEO('http://195.245.213.202/snode14/bea50eddc79748dc-c4ad8e4acdd35690-4ef16670ecc2bb47.inferno-vegas.-sq.wmv')
			 #self.LOAD_AND_PLAY_VIDEO('http://127.0.0.1:4001/megavideo/megavideo.caml?videoid=Y8ZPZLM0&amp;')
    elif mode == '20':
      log.info('Wyświetlam ustawienia')
      self.settings.showSettings()


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


  def CATEGORIES(self):
    ##self.addDir("Weeb TV [wyświetl kanały]", 1, True, False)
    ##self.addDir("Twoja Telewizja [wyświetl kanały]", 2, True, False)
    ##self.addDir("Ekino TV [Filmy, Seriale]", 3, True, False)
    ##self.addDir('Ustawienia', 20, True, False)
    self.addDir("Telewizja", 1, True, False)
    self.addDir("Filmy, Seriale", 2, True, False)
    self.addDir('Ustawienia', 20, True, False)
    #log.info(int(sys.argv[1]))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


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
        

  def addDir(self, name, mode, autoplay, isPlayable = True):
    u=sys.argv[0] + "?mode=" + str(mode)
    log.info(u)
    icon = "DefaultVideoPlaylists.png"
    if autoplay:
      icon= "DefaultVideo.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    log.info(name)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)


init = PolishLiveTV()
init.showListOptions()
