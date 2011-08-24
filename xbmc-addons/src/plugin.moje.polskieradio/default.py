# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib
import os, time
import xbmcaddon, xbmcplugin, xbmcgui
import parser

scriptID = 'plugin.moje.polskieradio'
scriptname = "Moje Polskie Radio"
pradio = xbmcaddon.Addon(scriptID)


MENU_MAIN = { 1: 'Programy',
             2: 'Słowo',
             3: 'Muzyka',
             4: 'Kategorie',
             5: 'Wszystkie kanały' }


class MyPolishRadio:
    def handleService(self):
        p = parser.Parser()
        params = p.getParams()
        if p.getParam(params, 'mode') == None or p.getParam(params, 'mode') == '':
            self.LIST(MENU_MAIN)
        elif p.getParam(params, 'mode') == '1' and p.getParam(params, 'name') == 'main':
            p.programyLink()
        elif p.getParam(params, 'mode') == '2' and p.getParam(params, 'name') == 'main':
            p.keyLink('slowo')
        elif p.getParam(params, 'mode') == '3' and p.getParam(params, 'name') == 'main':
            p.keyLink('muzyka')
        elif p.getParam(params, 'mode') == '4' and p.getParam(params, 'name') == 'main':
            p.listCategories()
        elif p.getParam(params, 'mode') == '4' and p.getParam(params, 'name') == 'categories':
            if p.getParam(params, 'id') != '':
                p.categoryLink(p.getParam(params, 'id'))
        elif p.getParam(params, 'mode') == '5' and p.getParam(params, 'name') == 'main':
            p.listChannels()


    def LIST(self, table = {}):
        for num, val in table.items():
            self.addDir('main', num, val, False, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def addDir(self, name, mode, title, autoplay, isPlayable = True):
        u=sys.argv[0] + "?mode=" + str(mode) + "&name=" + str(name)
        #xbmc.log('SCIEZKA: ' + u)
        icon = "DefaultVideoPlaylists.png"
        if autoplay:
            icon= "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage='')
        if autoplay and isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)


init = MyPolishRadio()
init.handleService()