 # -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)
language = ptv.getLocalizedString
t = sys.modules[ "__main__" ].language

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( ptv.getAddonInfo('path'), "hosts" ) )

import pLog, settings, Parser, serviceinfo
import weebtv, stations, tvp, tvn, iplex, tvpvod, wlacztv, poplertv
import maxvideo, serialnet, anyfiles, teledyski #, filmin
import ekinotv, iitvinfo, bestplayer, kinopecetowiec, kinomaniak, kabarety
#import ipla

log = pLog.pLog()

TV_ONLINE_TABLE = {
		     100 : ["Weeb TV [wyświetl kanały]", 'weebtv'],
		     101 : ["Włącz TV [wyświetl kanały]", 'wlacztv'],
		     102 : ["Stacje TV [strumienie]", 'stations'],
		     #103 : ["Popler TV", 'poplertv'],
}


VOD_ONLINE_TABLE = {
                     200: ["AnyFiles [różne filmy]", 'anyfiles'],
                     201: ["Ekino TV [filmy, seriale]", 'ekinotv'],
                     202: ["iiTV info [seriale]", 'iitvinfo'],
                     #203: ["IPLA", 'ipla'], 
                     204: ["IPLEX", 'iplex'],
                     205: ["TVN Player", 'tvn'],
                     206: ["TVP [info]", 'tvp'],
                     207: ["TVP VOD", 'tvpvod'],
                     208: ["SerialNet [seriale]", 'serialnet'],
                     209: ["BestPlayer [filmy]", 'bestplayer'],
		     210: ["Kino Pecetowiec [filmy]", 'kinopecetowiec'],
		     211: ["Maxvideo [różne filmy]", 'maxvideo'],
		     #212: ["Kinomaniak", 'kinomaniak'],
		     #213: ["Film.in", 'filmin'],
}

ROZRYWKA_TABLE = {
		     400: ["Kabarety", 'kabarety'],
                     401: ["Teledyski", 'teledyski'],
}

REC_DOWN_TABLE = {
		     300: ["Weeb TV", 'weebtv'],
		     301: ["Włącz TV", 'wlacztv'],
}


class PolishLiveTV:
  def __init__(self):
    log.info('Starting Polish Live TV')
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()


  def showListOptions(self):
        params = self.parser.getParams()
        mode = self.parser.getIntParam(params, "mode")
        name = self.parser.getParam(params, "name")
        service = self.parser.getParam(params, 'service')
	
        if mode == None and name == None and service == None:
                log.info('Wyświetlam kategorie')
                self.CATEGORIES()
		
        elif mode == 1:
                self.LIST(TV_ONLINE_TABLE)
        elif mode == 100 or service == TV_ONLINE_TABLE[100][1]:
                tv = weebtv.WeebTV()
                tv.handleService()
        elif mode == 101 or service == TV_ONLINE_TABLE[101][1]:
                tv = wlacztv.WlaczTV()
                tv.handleService()            
        elif mode == 102 or service == TV_ONLINE_TABLE[102][1]:
                tv = stations.StreamStations()
                tv.handleService()
        elif mode == 103 or service == 'poplertv':
                tv = poplertv.poplertv()
                tv.handleService()	
        
	elif mode == 2:
                self.LIST(VOD_ONLINE_TABLE)
        elif mode == 200 or service == VOD_ONLINE_TABLE[200][1]:
                vod = anyfiles.AnyFiles()
                vod.handleService()
        elif mode == 201 or service == VOD_ONLINE_TABLE[201][1]:
                vod = ekinotv.EkinoTV()
                vod.handleService()
        elif mode == 202 or service == VOD_ONLINE_TABLE[202][1]:
                vod = iitvinfo.iiTVInfo()
                vod.handleService()
       # elif mode == 203 or service == VOD_ONLINE_TABLE[203][1]:
       #        vod = ipla.IPLA()
       #        vod.handleService()
        elif mode == 204 or service == VOD_ONLINE_TABLE[204][1]:
                vod = iplex.IPLEX()
                vod.handleService()
        elif mode == 205 or service == VOD_ONLINE_TABLE[205][1]:
                vod = tvn.tvn()
                vod.handleService()
        elif mode == 206 or service == VOD_ONLINE_TABLE[206][1]:
                vod = tvp.tvp()
                vod.handleService()
        elif mode == 207 or service == VOD_ONLINE_TABLE[207][1]:
                vod = tvpvod.tvpvod()
                vod.handleService()
        elif mode == 208 or service == VOD_ONLINE_TABLE[208][1]:
                vod = serialnet.SerialNet()
                vod.handleService()
        elif mode == 209 or service == VOD_ONLINE_TABLE[209][1]:
                vod = bestplayer.BestPlayer()
                vod.handleService()
        elif mode == 210 or service == VOD_ONLINE_TABLE[210][1]:
                vod = kinopecetowiec.KinoPecetowiec()
                vod.handleService()
        elif mode == 211 or service == VOD_ONLINE_TABLE[211][1]:
                vod = maxvideo.Maxvideo()
                vod.handleService()
        elif mode == 212 or service == VOD_ONLINE_TABLE[212][1]:
                vod = kinomaniak.Kinomaniak()
                vod.handleService()
		
        elif mode == 4:
                self.LIST(ROZRYWKA_TABLE)
        elif mode == 400 or service == ROZRYWKA_TABLE[400][1]:
                vod = kabarety.Kabarety()
                vod.handleService()
        elif mode == 401 or service == ROZRYWKA_TABLE[401][1]:
                vod = teledyski.Teledyski()
                vod.handleService()
		
        elif mode == 300:
                vod = weebtv.WeebTV()
                vod.handleRecords()
        elif mode == 301:
                vod = wlacztv.WlaczTV()
                vod.handleRecords()              
        
	elif mode == 19:
                log.info('Zarządzanie nagrywaniem/ściąganiem')
                self.LIST(REC_DOWN_TABLE)
        elif mode == 20:
                log.info('Wyświetlam ustawienia')
                self.settings.showSettings()
	elif mode == 21:
		log.info('Service Info')
		si = serviceinfo.ServiceInfo()
		si.getWindow()
		

  def listsMenu(self, table, title):
    value = ''
    if len(table) > 0:
      d = xbmcgui.Dialog()
      choice = d.select(title, table)
      for i in range(len(table)):
        if choice == i:
          value = table[i]
    return value


  def listsTable(self, table):
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def CATEGORIES(self):

        self.addDir("Telewizja", 1, False, 'telewizja', False)
        self.addDir("Filmy, Seriale", 2, False, 'film', False)
        self.addDir("Rozrywka", 4, False, 'rozrywka', False)
        self.addDir('Zarządzanie nagrywaniem/ściąganiem', 19, False, 'nagrywanie', False)
        self.addDir('Informacje o serwisach', 21, True, 'info', False)
        self.addDir('Ustawienia', 20, True, 'ustawienia', False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def LIST(self, table = {}):
      valTab = []
      strTab = []
      for num, tab in table.items():
          strTab.append(num)
          strTab.append(tab[0])
	  strTab.append(tab[1])
          valTab.append(strTab)
          strTab = []
      valTab.sort(key = lambda x: x[1])      
      for i in range(len(valTab)):
          if valTab[i][2] == '': icon = False
          else: icon = valTab[i][2]
          self.addDir(valTab[i][1], valTab[i][0], False, icon, False)
      xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def addDir(self, name, mode, autoplay, icon, isPlayable = True):
    u=sys.argv[0] + "?mode=" + str(mode)
    if icon != False:
      icon = os.path.join(ptv.getAddonInfo('path'), "images/") + icon + '.png'
    else:
      icon = "DefaultVideoPlaylists.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)


init = PolishLiveTV()
init.showListOptions()

