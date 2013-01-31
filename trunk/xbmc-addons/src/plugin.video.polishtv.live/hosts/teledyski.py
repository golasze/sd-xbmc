# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import traceback

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, pCommon, Errors, Navigation


log = pLog.pLog()

dbg = ptv.getSetting('default_debug')
dstpath = ptv.getSetting('default_dstpath')

SERVICE = 'teledyski'
logoUrl = 'http://www.teledyskihd.pl/img/logo.jpg'
nextUrl = ptv.getAddonInfo('path') + os.path.sep + "images" + os.path.sep + "next.png"

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

MENU_TAB = {1: "Kategorie",
            2: "Najnowsze",
            3: "TOP",
            4: "Wyszukaj",
            5: "Historia Wyszukiwania"
            }



class Teledyski:
    def __init__(self):
        log.info('Loading Teledyski')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.cm = pCommon.common()
	self.exception = Errors.Exception()
	self.navigation = Navigation.VideoNav()
	self.history = pCommon.history()


    def setTable(self):
	return MENU_TAB


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.addDir(SERVICE, 'main-menu', val, '', '', '', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu2(self):
        url = 'http://www.teledyskihd.pl/'
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<li class=""><a href="(.+?)-videos-.+?-date.html">(.+?)</a></li>').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                title = match[i][1].replace('&amp;', '&')
                self.addDir(SERVICE, 'submenu', match[i][0], title, '', '', logoUrl, True, False)        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getFilmTable(self,url,category,page):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<div class=.+?>(.+?)</div>.\n.+?<div class=.+?>(.+?)</div>.\n.+?<div class=.+?><img src="http://.+?com/vi/(.+?)/0.jpg"').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                img = 'http://i.ytimg.com/vi/' + match[i][2] + '/0.jpg'
                title = match[i][1] + ' - ' + match[i][0] 
                self.addDir(SERVICE, 'playSelectedMovie', '', title, '', match[i][2], img, False, False)   
        match2 = re.compile('<a href="(.+?)">następne &raquo;</a></div>').findall(data)
        if len(match2) > 0:
            page = str(int(page) + 1)
            self.addDir(SERVICE, 'submenu', category, 'Następna strona', '', page, nextUrl, True, False)     
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getFilmTable1(self,url,category,page):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<div class=.+?><a title="(.+?)" href=".+?"> (.+?)</a></div>.\n.+?<div class.+?</a></div>.\n.+?<div class="datai">.\n.+?<a title=.+?><img src="http://.+?com/vi/(.+?)/0.jpg"').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                img = 'http://i.ytimg.com/vi/' + match[i][2] + '/0.jpg'
                title = match[i][1] + ' - ' + match[i][0]
                self.addDir(SERVICE, 'playSelectedMovie', '', title, '', match[i][2], img, False, False)   
        match2 = re.compile('<a href="(.+?)">następne &raquo;</a></div>').findall(data)
        if len(match2) > 0:
            page = str(int(page) + 1)
            self.addDir(SERVICE, '', category, 'Następna strona', '', page, nextUrl, True, False)     
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getFilmTable2(self,url):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<div class=.+?><a title="(.+?)" href=".+?">.+?.(.+?)</a></div>.\n.+?<div class.+?</a></div>.\n.+?<div class="datai">.\n.+?<a title=.+?><img src="http://.+?com/vi/(.+?)/0.jpg"').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                img = 'http://i.ytimg.com/vi/' + match[i][2] + '/0.jpg'
                title = match[i][1].replace('. ', '') + ' - ' + match[i][0]
                self.addDir(SERVICE, 'playSelectedMovie', '', title, '', match[i][2], img, False, False)       
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getFilmSearch(self,url):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<div class=.+?>(.+?)</div></a>.\n.+?<div class=.+?>(.+?)</div>.\n.+?<div class=.+?><img src="http://.+?com/vi/(.+?)/0.jpg"').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                img = 'http://i.ytimg.com/vi/' + match[i][2] + '/0.jpg'
                title = match[i][1] + ' - ' + match[i][0]
                self.addDir(SERVICE, 'playSelectedMovie', '', title, '', match[i][2], img, False, False)       
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
	    text = k.getText()
	    self.history.addHistoryItem(SERVICE, text)
        return text

    def listsHistory(self, table):
	for i in range(len(table)):
	    if table[i] <> '':
		self.addDir(SERVICE, 'teledyski', 'history', table[i], 'None', 'None', 'None', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def addDir(self, service, name, category, title, plot, page, iconimage, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(page)
        if name == 'main-menu':
            title = category
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title, "Plot": plot } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
      
      
    def LOAD_AND_PLAY_VIDEO(self, page):
        ok=True
        videoUrl = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + page
        if videoUrl == '':
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
            return False
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl)
        except:
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')        
        return videoUrl


    def handleService(self):
        params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        title = self.parser.getParam(params, "title")
        category = self.parser.getParam(params, "category")
        page = self.parser.getParam(params, "page")
        service = self.parser.getParam(params, "service")


        if dbg == 'true':
	    log.info ('name: ' + str(name))
	    log.info ('title: ' + str(title))
	    log.info ('category: ' + str(category))
	    log.info ('page: ' + str(page))

	if str(page)=='None' or page=='': page = 1
      
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif category == self.setTable()[1]:
            self.listsCategoriesMenu2()
        elif category == self.setTable()[2]:
            url = 'http://www.teledyskihd.pl/newvideos.html?&page=' + str(page)
            self.getFilmTable1(url, category, page)
        elif category == self.setTable()[3]:
            url = 'http://www.teledyskihd.pl/topvideos.html'
            self.getFilmTable2(url)
	elif category == self.setTable()[4]:
            text = self.searchInputText()
            url = 'http://www.teledyskihd.pl/search.php?keywords=' + text + '&btn.x=0&btn.y=0'
            self.getFilmSearch(url)
        elif category == self.setTable()[5]:
	    t = self.history.loadHistoryFile(SERVICE)
	    self.listsHistory(t)           
	if category == 'history' and name == 'teledyski':
            url = 'http://www.teledyskihd.pl/search.php?keywords=' + title + '&btn.x=0&btn.y=0'
            self.getFilmSearch(url)
            
        if name == 'submenu':
            url = category + '-videos-' + str(page) + '-date.html'
            self.getFilmTable(url, category, page)


        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(page)

