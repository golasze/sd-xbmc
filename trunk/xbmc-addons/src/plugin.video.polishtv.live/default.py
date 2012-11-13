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

import pLog, settings, Parser
import weebtv, stations, tvp, tvn, iplex, tvpvod, ekinotv, iitvinfo, anyfiles, wlacztv, serialnet, bestplayer
#import ipla

log = pLog.pLog()


TV_ONLINE_TABLE = { 100: "Weeb TV [wyświetl kanały]",
                    #101: "Włącz TV [wyświetl kanały]",
                    102: "Stacje TV [strumienie]",
}

VOD_ONLINE_TABLE = {
                     200: "AnyFiles [różne filmy]",
                     201: "Ekino TV [filmy, seriale]",
                     202: "iiTV info [seriale]",
                     #203: "IPLA",
                     204: "IPLEX",
                     205: "TVN Player",
                     206: "TVP [info]",
                     207: "TVP VOD",
                     208: "SerialNet [seriale]",
                     209: "BestPlayer [filmy]",
}

REC_DOWN_TABLE = { 300: "Weeb TV",
                   #301: "Włącz TV",
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
        elif mode == 100 or service == 'weebtv':
                tv = weebtv.WeebTV()
                tv.handleService()
        #elif mode == 101 or service == 'wlacztv':
                #tv = wlacztv.WlaczTV()
                #tv.handleService()            
        elif mode == 102 or service == 'stations':
                tv = stations.StreamStations()
                tv.handleService()
        elif mode == 2:
                #log.info('Wejście do TV internetowej')
                self.LIST(VOD_ONLINE_TABLE)
        elif mode == 200 or service == 'anyfiles':
                vod = anyfiles.AnyFiles()
                vod.handleService()
        elif mode == 201 or service == 'ekinotv':
                vod = ekinotv.EkinoTV()
                vod.handleService()
        elif mode == 202 or service == 'iitvinfo':
                vod = iitvinfo.iiTVInfo()
                vod.handleService()
        #elif mode == 203 or service == 'ipla':
        #       vod = ipla.IPLA()
        #       vod.handleService()
        elif mode == 204 or service == 'iplex':
                vod = iplex.IPLEX()
                vod.handleService()
        elif mode == 205 or service == 'tvn':
                vod = tvn.tvn()
                vod.handleService()
        elif mode == 206 or service == 'tvp':
                vod = tvp.tvp()
                vod.handleService()
        elif mode == 207 or service == 'tvpvod':
                vod = tvpvod.tvpvod()
                vod.handleService()
        elif mode == 208 or service == 'serialnet':
                vod = serialnet.SerialNet()
                vod.handleService()
        elif mode == 209 or service == 'bestplayer':
                vod = bestplayer.BestPlayer()
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
        self.addDir('Zarządzanie nagrywaniem/ściąganiem', 19, False, False)
        self.addDir('Ustawienia', 20, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def LIST(self, table = {}):
        for num, val in table.items():
                self.addDir(val, num, False, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


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

