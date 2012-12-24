# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, urlparser, pCommon, Navigation, Errors, downloader
import maxvideo

log = pLog.pLog()

dbg = ptv.getSetting('default_debug')
dstpath = ptv.getSetting('default_dstpath')

SERVICE = 'bestplayer'
mainUrl = 'http://bestplayer.tv/'
mainUrl2 = mainUrl + 'filmy/'
TOP_LINK = mainUrl + 'top100/'
logoUrl = mainUrl + 'images/logo.png'
first = '-strona-1.html'

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

MENU_TAB = {1: "Lektor",
	    2: "Napisy",
	    3: "Premiery",
            4: "TOP", 
            5: "Data wydania",
            6: "Szukaj",
            7: "Historia Wyszukiwania"
            }


class BestPlayer:
    def __init__(self):
        log.info('Loading BestPlayer')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.history = pCommon.history()
	self.navigation = Navigation.VideoNav()
	self.chars = pCommon.Chars()
	self.exception = Errors.Exception()


    def setTable(self):
	return MENU_TAB


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.addDir(SERVICE, 'main-menu', val, '', '', '', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu2(self):
        query_data = { 'url': mainUrl2, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<a href="(.+?)z-lektorem.html" title="Filmy(.+?)"><span class="float-left">(.+?)</span><span class="float-right"></span></a></li>').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                self.addDir(SERVICE, 'submenu', '', match[i][2], '', mainUrl + match[i][0] + 'z-lektorem-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))    


    def listsCategoriesMenu3(self):
        query_data = { 'url': mainUrl2, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<a href="(.+?)z-napisami.html" title="Filmy.+?"><span class="float-left">(.+?)</span><span').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                self.addDir(SERVICE, 'submenu', '', match[i][1], '', mainUrl + match[i][0] + 'z-napisami-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu4(self):
        query_data = { 'url': mainUrl2, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<a href="(.+?)premiery.html" title="Filmy(.+?)"><span class="float-left">(.+?)</span><span class="float-right"></span></a></li>').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                self.addDir(SERVICE, 'submenu', '', match[i][2], '', mainUrl + match[i][0] + 'premiery-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu5(self):
        query_data = { 'url': mainUrl2, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<a href="filmy/rok(.+?).html" title="(.+?)"><span class="float-left">(.+?)</span><span class="float-right"></span></a></li>').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                self.addDir(SERVICE, 'submenu', '', match[i][1], '', mainUrl + 'filmy/rok' + match[i][0] + '-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 
     
     
    def getFilmTable(self,url):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        tabURL = data.replace('</div>', '').replace('<div class="fr" style="width:475px; margin-right:10px; margin-top:10px">', '').replace('&amp;', '').replace('quot;', '').replace('&amp;quot;', '')
        match = re.compile('<a href="(.+?)" title=""><img src="(.+?)" width.+?/></a>\n.+?<div style.+?star.png" />\n.+?<div>Opini:.+?\n.+?\n.+?\n.+?<h2><a href=".+?">(.+?)</a></h2>\n.+?Kategorie:.+?</a></p>\n.+?\n.+?<div class="p5 film-dsc" >(.+?)\n.+?').findall(tabURL)
        if len(match) > 0:
            for i in range(len(match)):
                #isPlayable needs to be set to False in order to play
                self.addDir(SERVICE, 'playSelectedMovie', '', match[i][2], match[i][3], match[i][0], mainUrl + match[i][1], False, False)   
        match2 = re.compile('<li class="round "><a href="(.+?)" class="next"></a></li>').findall(data)
        if len(match2) > 0:
            nexturl = match2[0]
            self.addDir(SERVICE, 'submenu', '', 'Następna strona', '', mainUrl + nexturl, '', True, False)     
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTable2(self,url):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        tabURL = data.replace('</div>', '').replace('&amp;', '').replace('quot;', '').replace('&amp;quot;', '')
        match = re.compile('<a class=".+?"  href="(.+?)" title=""><img src="(.+?)" height=.+?/></a>\n.+?<div class="trigger.+?".+?star.png" />\n.+?<div class="trigger.+?".+?\n.+?<div class="trigger.+?".+?\n.+?\n.+?<div class="fr".+?\n.+?<h2><a href=".+?">(.+?)</a></h2>\n.+?Kategorie.+?\n.+?\n.+?<div class=".+?" class="p5 film-dsc".+?">(.+?)\n.+?<a class="trigger.+?"').findall(tabURL)
        if len(match) > 0:
            for i in range(len(match)):
                #isPlayable needs to be set to False in order to play
                self.addDir(SERVICE, 'playSelectedMovie', '', match[i][2], match[i][3], match[i][0], mainUrl + match[i][1], False, False)       
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
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
		self.addDir(SERVICE, table[i], 'history', table[i], 'None', logoUrl, 'None', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def searchTab(self, url, text):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': True, 'return_data': True }
        try:
	    link = self.cm.getURLRequestData(query_data, {'q': text})
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        tabURL = link.replace('</div>', '').replace('&amp;', '').replace('quot;', '').replace('&amp;quot;', '')
        match = re.compile('<div class="movie-cover fl">\n.+?<a href="(.+?)" title=""><img src="(.+?)" width="150" height="200" alt="okladka" /></a>\n.+?<div.+?png" />\n.+?<div>O.+?\n.+?\n.+?<div.+?px">\n.+?<h2><a.+?>(.+?)</a></h2>\n.+?Kat.+?</a></p>\n.+?\n.+?<div class="p5 film-dsc" >(.+?)\n.+?<div style="margin-top: 10px;">').findall(tabURL)
        if len(match) > 0:
            for i in range(len(match)):
                self.addDir(SERVICE, 'playSelectedMovie', 'history', match[i][2], match[i][3], match[i][0], mainUrl + match[i][1], True, False)   
        match2 = re.compile('<li class="round "><a href="(.+?)" class="next"></a></li>').findall(link)
        if len(match2) > 0:
            nexturl = match2[0]
            self.addDir(SERVICE, 'submenu', '', 'Następna strona', '', mainUrl + nexturl, '', True, False)     
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   


    def getVideoID(self,url):
        videoID = ''
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': True, 'return_data': True }
        try:
	    link = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<iframe src="(.+?)" style="border:0px; width: 740px; height: 475px;" scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            videoID = match[0]
        return videoID


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
        if dstpath != "None" or not dstpath and name == 'playSelectedMovie':
	    if dbg == 'true':
		log.info(SERVICE + ' - addDir() -> title: ' + title)
		log.info(SERVICE + ' - addDir() -> url: ' + page)
		log.info(SERVICE + ' - addDir() -> dstpath: ' + os.path.join(dstpath, SERVICE))
	    cm = self.navigation.addVideoContextMenuItems({ 'service': SERVICE, 'title': urllib.quote_plus(self.chars.replaceChars(title)), 'url': urllib.quote_plus(page), 'path': os.path.join(dstpath, SERVICE) })
	    liz.addContextMenuItems(cm, replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
      
      
    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, player):
        ok=True
        if videoUrl == '':
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
            return False
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        
        if player=='maxvideo': xbmcPlayer = maxvideo.Player()
        else: xbmcPlayer = xbmc.Player()
            
        log.info("using player: " + player)
        try:
            xbmcPlayer.play(videoUrl, liz)
            #if player == 'default':
            #    while xbmcPlayer.is_active:
            #        xbmcPlayer.sleep(100)               
        except:
            d = xbmcgui.Dialog()
            d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')        
        return ok


    def handleService(self):
        params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        title = self.parser.getParam(params, "title")
        category = self.parser.getParam(params, "category")
        page = self.parser.getParam(params, "page")
        url = self.parser.getParam(params, "url")
        vtitle = self.parser.getParam(params, "vtitle")
        service = self.parser.getParam(params, "service")
        action = self.parser.getParam(params, "action")
        path = self.parser.getParam(params, "path")

        if dbg == 'true':
	    log.info ('name: ' + str(name))
	    log.info ('title: ' + str(title))
	    log.info ('category: ' + str(category))
	    log.info ('page: ' + str(page))
      
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif category == self.setTable()[1]:
            self.listsCategoriesMenu2()
        elif category == self.setTable()[2]:
            self.listsCategoriesMenu3()
        elif category == self.setTable()[3]:
            self.listsCategoriesMenu4()
        elif category == self.setTable()[4]:
            self.getFilmTable2(TOP_LINK)    
        elif category == self.setTable()[5]:
            self.listsCategoriesMenu5()
        elif category == self.setTable()[6]:
            text = self.searchInputText()
            self.searchTab(mainUrl, text)
        elif category == self.setTable()[7]:
	    t = self.history.loadHistoryFile(SERVICE)
	    self.listsHistory(t)
	if category == 'history' and name != 'playSelectedMovie':
	    self.searchTab(mainUrl, name)
        if name == 'submenu':
            self.getFilmTable(page)

        if name == 'playSelectedMovie':
            nUrl = mainUrl + page
            linkVideo = ''
            ID = self.getVideoID(nUrl)
            if ID != '':
                if 'maxvideo.pl' in ID: player = 'maxvideo'
                else: player = 'default'
                linkVideo = self.up.getVideoLink(ID)
                if linkVideo != False:
                    self.LOAD_AND_PLAY_VIDEO(linkVideo, title, player)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', 'Maxvideo - tymczasowo wyczerpałeś limit ilości uruchamianych seriali.', 'Zapraszamy za godzinę.')

        if service == SERVICE and action == 'download' and url != '':
            self.cm.checkDir(os.path.join(dstpath, SERVICE))
            if dbg == 'true':
		log.info(SERVICE + ' - handleService()[download][0] -> title: ' + urllib.unquote_plus(vtitle))
		log.info(SERVICE + ' - handleService()[download][0] -> url: ' + urllib.unquote_plus(url))
		log.info(SERVICE + ' - handleService()[download][0] -> path: ' + path)	
            if urllib.unquote_plus(url).startswith('film'):
		urlTempVideo = self.getVideoID(mainUrl + urllib.unquote_plus(url))
		linkVideo = self.up.getVideoLink(urlTempVideo)
		if dbg == 'true':
		    log.info(SERVICE + ' - handleService()[download][1] -> title: ' + urllib.unquote_plus(vtitle))
		    log.info(SERVICE + ' - handleService()[download][1] -> temp url: ' + urlTempVideo)
		    log.info(SERVICE + ' - handleService()[download][1] -> url: ' + linkVideo)							
		if linkVideo != False:
		    if dbg == 'true':
			log.info(SERVICE + ' - handleService()[download][2] -> title: ' + urllib.unquote_plus(vtitle))
			log.info(SERVICE + ' - handleService()[download][2] -> url: ' + linkVideo)
			log.info(SERVICE + ' - handleService()[download][2] -> path: ' + path)							
		    dwnl = downloader.Downloader()
		    dwnl.getFile({ 'title': urllib.unquote_plus(vtitle), 'url': linkVideo, 'path': path })
