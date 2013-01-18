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

log = pLog.pLog()

dbg = ptv.getSetting('default_debug')
dstpath = ptv.getSetting('default_dstpath')

SERVICE = 'iitvinfo'
mainUrl = 'http://iitv.info'
watchUrl = mainUrl + '/ogladaj/'
imageUrl = mainUrl + '/gfx/'

class iiTVInfo:
    def __init__(self):
        log.info('Loading ' + SERVICE)
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.navigation = Navigation.VideoNav()
	self.chars = pCommon.Chars()
	self.exception = Errors.Exception()


    def listsABCMenu(self, table):
        for i in range(len(table)):
            self.addDir(SERVICE, 'abc-menu', table[i], table[i], '', '', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        
    def getSerialsTable(self, letter):
        strTab = []
        outTab = []
        query_data = { 'url': mainUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<li class="serial_menu.+?" style="display:.+?"><a href="(.+?)">(.+?)</a>').findall(data)
        if len(match) > 0:
            addItem = False
            for i in range(len(match)):
                if not '<b>' in match[i][1]:
                    if (ord(letter[0]) < 65) and (ord(match[i][1][0]) < 65 or ord(match[i][1][0]) > 91): addItem = True
                    if (letter == match[i][1][0].upper()): addItem = True
                    if (addItem):
                        strTab.append(match[i][1])
                        strTab.append(match[i][0])
                        outTab.append(strTab)
                        strTab = []
                        addItem = False
        outTab.sort(key = lambda x: x[0])
        return outTab         
    
    
    def getImage(self,url):
        imageLink=imageUrl + url[1:-1] + '.jpg'     
        return imageLink
    
    
    def showSerialTitles(self, letter):
        tab = self.getSerialsTable(letter)
        if len(tab) > 0:
            for i in range(len(tab)):
                imageLink = self.getImage(tab[i][1])
                self.addDir(SERVICE, 'serial-title', tab[i][0], tab[i][0], tab[i][1], imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

    def showSeason(self, url, fname):
        imageLink = self.getImage(url)
        nUrl = mainUrl + url
        query_data = { 'url': nUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
        match = re.compile('<div class="serial_season">(.+?)</div>').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                if 'Sezon' in match[i]:
                    self.addDir(SERVICE, 'serial-season', fname, match[i], url, imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def showSerialParts(self, url, title, fname):
        imageLink = self.getImage(url)
        log.info("image: " + imageLink)
        nUrl = mainUrl + url
        tTab = title.split(' ')
        num = tTab[1]
        if float(num) < 10: num = '0' + num
        s = "s" + str(num)
        log.info("url:" + nUrl)
        log.info("season: " + s)
        query_data = { 'url': nUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()       
        match_parts = re.compile('<a href="(.+?)"><span class="release">(.+?)</span>(.+?)</a>').findall(data)
        if len(match_parts) > 0:
            for i in range(len(match_parts)):
                if s in match_parts[i][1]:
                    pTab = match_parts[i][1].split('e')
                    if (len(pTab)==2):
                        title = match_parts[i][1] + ' - ' + match_parts[i][2]
                        if match_parts[i][2] == '' or match_parts[i][2] == ' ':
                            title = match_parts[i][1]
                        nUrl = url + match_parts[i][0]
                        self.addDir(SERVICE, 'playSelectedMovie', fname, title, nUrl, imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[0])
        return out


    def getVideoID(self, url):
        videoID = ''
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit() 
        match = re.compile('<input type="hidden" name="(.+?)" value="(.+?)" />').findall(data)
        if len(match) > 0:
            og_ser = ''
            og_s = ''
            og_e = ''
            og_url = ''
            og_code = ''
            for i in range(len(match)):
                if match[i][0] == 'og_ser':
                    og_ser =  match[i][1]
                elif match[i][0] == 'og_sez':
                    og_s = match[i][1]
                elif match[i][0] == 'og_e':
                    og_e  = match[i][1]
                elif match[i][0] == 'og_url':
                    og_url = match[i][1]
                elif match[i][0] == 'og_coda':
                    og_code = match[i][1]
            post_data = {'og_ser': og_ser, 'og_sez': og_s, 'og_e': og_e, 'og_url': og_url, 'og_coda': og_code}
            query_data = {'url': watchUrl, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True}
            try:
                data = self.cm.getURLRequestData(query_data, post_data)
            except Exception, exception:
                traceback.print_exc()
                self.exception.getError(str(exception))
                exit()                       
            match_watch = re.compile('<div class="watch_link" id=".+?"> <a href="(.+?)" target="_blank">').findall(data)
            if len(match_watch) > 0:
                valTab = []
                strTab = []
                a = 1
                for i in range(len(match_watch)):
                    strTab.append(str(a) + ". " + self.up.getHostName(match_watch[i], True))
                    strTab.append(match_watch[i])
                    valTab.append(strTab)
                    strTab = []
                    a = a + 1
                log.info("lista: " + str(valTab))
                d = xbmcgui.Dialog()
                item = d.select("Wybór filmu", self.getItemTitles(valTab))
                if item != -1:
                    videoID = str(valTab[item][1])
                    log.info('mID: ' + videoID)
                    return videoID
        return False
        

    def addDir(self, service, name, category, title, page, iconimage, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(page)
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        if dstpath != "None" or not dstpath and name == 'playSelectedMovie':
	    if dbg == 'true':
	    	log.info(SERVICE + ' - addDir() -> title: ' + title)
		log.info(SERVICE + ' - addDir() -> url: ' + page)
		log.info(SERVICE + ' - addDir() -> dstpath: ' + os.path.join(dstpath, SERVICE))
	    cm = self.navigation.addVideoContextMenuItems({ 'service': SERVICE, 'title': urllib.quote_plus(self.chars.replaceChars(category + ' - ' + title)), 'url': urllib.quote_plus(page), 'path': os.path.join(dstpath, SERVICE) })
	    liz.addContextMenuItems(cm, replaceItems=False)
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
            d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')        
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
        
        if name == None:
            self.listsABCMenu(self.cm.makeABCList())
        if name == 'abc-menu':
            self.showSerialTitles(category)
        elif name == 'serial-title':
            self.showSeason(page, category)
        elif name == 'serial-season' and title != None and page != None:    
            self.showSerialParts(page, title, category)

        if name == 'playSelectedMovie':
            nUrl = mainUrl + page
            linkVideo = ''
            ID = ''
            ID = self.getVideoID(nUrl)
            #print str (ID)
            if (ID!=False):
                if ID != '':
                    linkVideo = self.up.getVideoLink(ID)
                    if linkVideo != False:
                        self.LOAD_AND_PLAY_VIDEO(linkVideo, title)
                else:
                    d = xbmcgui.Dialog()
                    d.ok('Brak linku', SERVICE + ' - tymczasowo wyczerpałeś limit ilości uruchamianych seriali.', 'Zapraszamy za godzinę.')

        if service == SERVICE and action == 'download' and url != '':
            self.cm.checkDir(os.path.join(dstpath, SERVICE))
	    if dbg == 'true':
		log.info(SERVICE + ' - handleService()[download][0] -> title: ' + urllib.unquote_plus(vtitle))
		log.info(SERVICE + ' - handleService()[download][0] -> url: ' + urllib.unquote_plus(url))
		log.info(SERVICE + ' - handleService()[download][0] -> path: ' + path)	
	    if urllib.unquote_plus(url).startswith('/'):
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
