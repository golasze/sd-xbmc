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
	log.info('Wejście do TV komercyjnej')
	#tt = weebtv.WeebTV()
	#tt.handle()
	try:
	  tv = weebtv.WeebTV()
	  chn = self.listsMenu(tv.getChannelNames(), "Wybór kanału")
	  if chn != '':
	    link = tv.getChannelURL(chn)
	    if self.settings.WeebTVEnable == 'true':
	      #log.info('podany login: ' + self.settings.WeebTVLogin)
	      #log.info('podane hasło: ' + self.settings.WeebTVPassword)
	      if tv.login(self.settings.WeebTVLogin, self.settings.WeebTVPassword):
		#log.info('zalogowany')
		self.LOAD_AND_PLAY_VIDEO(tv.videoLink(link))
	    else:
	      #log.info('bez logowania')
	      self.LOAD_AND_PLAY_VIDEO(tv.videoLink(link))
	except:
	  d = xbmcgui.Dialog()
	  d.ok('Nie można pobrać kanałów.', 'Przyczyną może być tymczasowa awaria serwisu.', 'Spróbuj ponownie za jakiś czas')
      elif menu == TV_ONLINE_TABLE[2]:
	#rtmp = 'rtmp://199.9.255.45/app swfUrl=http://www-cdn.justin.tv/widgets/live_site_player.r34305490c2b0abacd260523181fc486d496372ee.swf pageUrl=http://pl.justin.tv/akisla live=true'
	rtmp = 'http://195.245.213.202/snode14/eaf92f195c6aa949-5a810d9fd83d06bb-bdb68c032c5a3917.ranczo-odc-1-spadek-vegas..wmv'
	self.LOAD_AND_PLAY_VIDEO(rtmp)
    elif mode == '2':
      log.info('Wejście do TV internetowej')
      menu = self.listsMenu(self.listsTable(VOD_ONLINE_TABLE), "Wybór z listy")
      if menu == VOD_ONLINE_TABLE[1]:
	vod = ekinotv.EkinoTV()
	cm = self.listsMenu(vod.getMenuTable(), "Wybór typu")
	if cm == vod.setTable()[1]:
	  categoryMovies = self.listsMenu(vod.getCategoryName(), "Kategorie filmów")
	  if categoryMovies != '':
	    #log.info(categoryMovies)
	    page = self.listsMenu(vod.getSortMovies(categoryMovies), "Wybór strony")
	    if page != '':
	      title = self.listsMenu(vod.getMovieCatNames(page, categoryMovies), "Wybór tytułu filmu")
	      if title != '':
		urlLink = vod.getMovieCatURL(page, categoryMovies, title)
		if urlLink.startswith('http://'):
		  if self.settings.MegaVideoUnlimit == 'false':
		    self.LOAD_AND_PLAY_VIDEO(vod.videoMovieLink(urlLink))
		  elif self.settings.MegaVideoUnlimit == 'true':
		    self.LOAD_AND_PLAY_VIDEO(vod.getUnlimitVideoLink(urlLink))
	elif cm == vod.setTable()[2]:
	  page = self.listsMenu(vod.getSortLinkMovies(vod.setDubLink()) , "Wybór strony")
	  if page != '':
	    title = self.listsMenu(vod.getMovieDubNames(page), "Wybór tytułu filmu")
	    if title != '':
	      urlLink = vod.getMovieDubURL(page, title)
	      if urlLink.startswith('http://'):
		if self.settings.MegaVideoUnlimit == 'false':
		  self.LOAD_AND_PLAY_VIDEO(vod.videoMovieLink(urlLink))
		elif self.settings.MegaVideoUnlimit == 'true':
		  self.LOAD_AND_PLAY_VIDEO(vod.getUnlimitVideoLink(urlLink))
	elif cm == vod.setTable()[3]:
	  page = self.listsMenu(vod.getSortLinkMovies(vod.setSubLink()) , "Wybór strony")
	  if page != '':
	    title = self.listsMenu(vod.getMovieSubNames(page), "Wybór tytułu filmu")
	    if title != '':
	      urlLink = vod.getMovieSubURL(page, title)
	      if urlLink.startswith('http://'):
		if self.settings.MegaVideoUnlimit == 'false':
		  self.LOAD_AND_PLAY_VIDEO(vod.videoMovieLink(urlLink))
		elif self.settings.MegaVideoUnlimit == 'true':
		  self.LOAD_AND_PLAY_VIDEO(vod.getUnlimitVideoLink(urlLink))
	elif cm == vod.setTable()[4]:
	  title = self.listsMenu(vod.getMoviePopNames(), "Wybór tytułu filmu")
	  if title != '':
	    urlLink = vod.getMoviePopURL(title)
	    if urlLink.startswith('http://'):
		if self.settings.MegaVideoUnlimit == 'false':
		  self.LOAD_AND_PLAY_VIDEO(vod.videoMovieLink(urlLink))
		elif self.settings.MegaVideoUnlimit == 'true':
		  self.LOAD_AND_PLAY_VIDEO(vod.getUnlimitVideoLink(urlLink))
  	if cm == vod.setTable()[5]:
	  title = self.listsMenu(vod.getSerialNames(), "Wybór tytułu serialu")
	  if title != '':
	    season = self.listsMenu(vod.getSeasonsTab(vod.getSerialURL(title)), "Wybór sezonu")
	    if season != '':
	      part = self.listsMenu(vod.getSeasonPartsTitle(season, title), "Wybór odcinka")
	      if part != '':
		urlLink = vod.getPartURL(part, title)
		if urlLink.startswith('http://'):
		  if self.settings.MegaVideoUnlimit == 'false':
		    self.LOAD_AND_PLAY_VIDEO(vod.videoMovieLink(urlLink))
		  elif self.settings.MegaVideoUnlimit == 'true':
		    self.LOAD_AND_PLAY_VIDEO(vod.getUnlimitVideoLink(urlLink))
	if cm == vod.setTable()[6]:
	  text = vod.searchInputText()
	  if text != None:
	    title = self.listsMenu(vod.getMovieSearchNames(text), "Wybór tytułu")
	    if title != '':
	      urlLink = vod.getMovieURL(vod.searchTab(text), title)
	      if urlLink.startswith('http://'):
		if self.settings.MegaVideoUnlimit == 'false':
		  self.LOAD_AND_PLAY_VIDEO(vod.videoMovieLink(urlLink))
		elif self.settings.MegaVideoUnlimit == 'true':
		  self.LOAD_AND_PLAY_VIDEO(vod.getUnlimitVideoLink(urlLink))

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
