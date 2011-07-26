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

import pLog, settings, weebtv, ekinotv, anyfiles, itvp, ipla

log = pLog.pLog()


TV_ONLINE_TABLE = { 100: "Weeb TV [wyświetl kanały]",
		    101: "Justin TV [wyświetl kanały]" }

VOD_ONLINE_TABLE = { 200: "Ekino TV [filmy, seriale]",
		     201: "iTVP [filmy, seriale, vod]",
		     202: "AnyFiles [różne filmy]",
		     203: "IPLEX",
		     204: "IPLA" }



class PolishLiveTV:
  def __init__(self):
    log.info('Starting Polish Live TV')
    self.settings = settings.TVSettings()


  def showListOptions(self):
  	mode = str(self.settings.paramMode)
  	name = str(self.settings.paramName)
  	service = str(self.settings.paramService)
  	#log.info( 'mode: ' + str(mode))
  	if mode == 'None' and name == 'None':
  		log.info('Wyświetlam kategorie')
  		self.CATEGORIES()
  	elif mode == '1':
		self.LIST(TV_ONLINE_TABLE)
	elif mode == '100' or service == 'weebtv':
		tv = weebtv.WeebTV()
		tv.handleService()
	elif mode == '2':
		log.info('Wejście do TV internetowej')
		self.LIST(VOD_ONLINE_TABLE)
	elif mode == '200' or service == 'ekinotv':
		vod = ekinotv.EkinoTV()
		vod.handleService()
	elif mode == '201':
		vod = itvp.iTVP()
		vod.handleService()
	elif mode == '202':
		vod = anyfiles.AnyFiles()
		vod.handleService()
	#elif mode == '203':
	#	vod = anyfiles.AnyFiles()
	#	vod.handleService()
	elif mode == '204' or service == 'ipla':
		#self.LOAD_AND_PLAY_VIDEO('http://redirector.redefine.pl/movies/e5a064aac8f20f7289c09bd533dc1bdf.flv')
		vod = ipla.IPLA()
		vod.handleService()
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
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def CATEGORIES(self):
	self.addDir("Telewizja", 1, False, False)
	self.addDir("Filmy, Seriale", 2, False, False)
	self.addDir('Ustawienia', 20, True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def LIST(self, table = {}):
  	for num, val in table.items():
  		self.addDir(val, num, False, False)
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
    icon = "DefaultVideoPlaylists.png"
    if autoplay:
      icon= "DefaultVideo.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)


init = PolishLiveTV()
init.showListOptions()
