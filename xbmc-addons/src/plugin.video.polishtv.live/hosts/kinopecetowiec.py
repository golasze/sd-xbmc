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

import pLog, settings, Parser, urlparser, pCommon, Navigation, Errors

log = pLog.pLog()

dbg = ptv.getSetting('default_debug')
dstpath = ptv.getSetting('default_dstpath')

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
SERVICE = 'kinopecetowiec'
MAINURL = 'http://www.kino.pecetowiec.pl'
LOGOURL = 'http://pecetowiec.pl/images/blackevo4-space/logo.png'
IMGURL = MAINURL + '/chimg/'

NEW_LINK = MAINURL + '/videos/basic/mr/'
POP_LINK = MAINURL + '/videos/basic/mv/'
COM_LINK = MAINURL + '/videos/basic/md/'
FAV_LINK = MAINURL + '/videos/basic/tf/'
SCR_LINK = MAINURL + '/videos/basic/tr/'
PRC_LINK = MAINURL + '/videos/basic/rf/'
RDM_LINK = MAINURL + '/videos/basic/rd/'

SERVICE_MENU_TABLE = {1: "Kategorie Filmowe",
		      2: "Najnowsze",
		      3: "Najczęściej Oglądane",
		      4: "Najczęściej Komentowane",
		      5: "Ulubione",
		      6: "Najwyżej Ocenione",
		      7: "Wyróżnione",
		      8: "Losowe",
		      
		      10: "Szukaj",
		      11: "Historia Wyszukiwania"
		      }

class KinoPecetowiec:
    def __init__(self):
        log.info('Loading ' + SERVICE)
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
	self.history = pCommon.history()
	self.navigation = Navigation.VideoNav()
	self.chars = pCommon.Chars()
	self.exception = Errors.Exception()


    def setTable(self):
	return SERVICE_MENU_TABLE


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.addDir(SERVICE, 'main-menu', val, '', '', '', LOGOURL, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getCategoryTab(self,url):   
        strTab = []
        valTab = []
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	#data = self.cm.requestData(url)
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        match = re.compile('<div class=".+?"><a href="http://www.kino.pecetowiec.pl/categories/(.+?)/(.+?)" title=".+?"><span').findall(data)
        if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(value[0])
		strTab.append(value[1])	
		valTab.append(strTab)
		strTab = []
	    valTab.sort(key = lambda x: x[1])
        return valTab


    def listsCategoriesMenu(self,url):
        table = self.getCategoryTab(url)
        for i in range(len(table)):
	    value = table[i]
	    img = IMGURL + value[0] + '.jpg'
	    title = value[1].replace('-', ' ')
	    if title > 0:
		self.addDir(SERVICE, 'category', value[0], title, '', '', img, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTab(self, url, category):
        strTab = []
        valTab = []
        data = self.cm.requestData(url)
	#Kategorie
	if category.isdigit()==True:
	    match = re.compile('<div class="channel-details-thumb-box-texts"> <a href="http://www.kino.pecetowiec.pl/video/(.+?)/(.+?)">(.+?)</a><br/>').findall(data)
	else:
	#Najnowsze, Najczescie Ogladane
	    match = re.compile('<div class="video-title"><a href="http://www.kino.pecetowiec.pl/video/(.+?)/(.+?)" title="(.+?)">').findall(data)
        if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(MAINURL + '/thumb/1_' + value[0] +'.jpg')
		strTab.append(MAINURL + '/video/' + value[0] + '/' + value[1])
		strTab.append(value[2])	
		valTab.append(strTab)
		strTab = []
	#pagination
	match = re.compile('<a href="(.+?)">&raquo;</a>').findall(data)
	if len(match) > 0:
            strTab.append('')
            strTab.append('')
            strTab.append('Następna strona')	
            valTab.append(strTab) 	    
        return valTab

   
    def getFilmTable(self, url, category, page):
        table = self.getFilmTab(url, category)
        for i in range(len(table)):
	    value = table[i]
	    title = value[2].replace("&#039;", "'").replace('&amp;', '&')
	    if value[2] != 'Następna strona':
		self.addDir(SERVICE, 'playSelectedMovie', '', title, '', value[1], value[0], True, False)
	    else:
		page = str(int(page) + 1)
		self.addDir(SERVICE, 'category', category, value[2], '', page, '', True, False) 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def setLinkTable(self, host, url):
        strTab = []
	strTab.append(host)
	strTab.append(url)
	return strTab

	
    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
           # title = value[0].replace('www', '').replace('com', '').replace('.', '').replace('pl', '').replace('eu', '')
            out.append(value[0])
        return out 

    def listsHistory(self, table):
#	print str(table)
	for i in range(len(table)):
#	    print str(table[i])
	    if table[i] <> '':
		self.addDir(SERVICE, table[i], 'history', table[i], 'None', LOGOURL, 'None', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchTable(self, table):
        #table = self.searchTab()
        for i in range(len(table)):
	    value = table[i]
	    title = value[2].replace("&#039;", "'").replace('&amp;', '&')
	    self.addDir(SERVICE, 'playSelectedMovie', 'history', title, '', value[1], value[0], True, False)   
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
	    text = k.getText()
	    self.history.addHistoryItem(SERVICE, text)
        return text


    def searchTab(self, text):
        strTab = []
        valTab = []
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': True, 'return_data': True }
        values = {'search_id': text}
	try:
		link = self.cm.getURLRequestData(query_data, values)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        match = re.compile('<img src="(.+?)" width="126"  height="160" id="rotate').findall(link)
        if len(match) > 0:
          img = match
        else:
          img = []
        match = re.compile('<div class="video-title"><a href="(.+?)" title="(.+?)">').findall(link)
        if len(match) > 0:
          for i in range(len(match)):
            value = match[i]
            strTab.append(img[i])
            strTab.append(value[0])
            strTab.append(value[1])	
            valTab.append(strTab)
            strTab = []
        return valTab


    def getHostTable(self,url):
	valTab = []
        #link = self.cm.requestData(url)
	query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
		link = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        data = link.replace('putlocker.com/file', 'putlocker.com/embed'). replace('http://sockshare.com', 'http://www.sockshare.com')
	match = re.compile('<div id="videoplayer">(.+?)</div>', re.DOTALL).findall(data)
	if len(match) > 0:
	    match2 = re.compile('http://(.+?)["\\r]').findall(match[0])
	    if len(match2) > 0:
		for i in range(len(match2)):
		    match2[i] = 'http://' + match2[i]
		    valTab.append(self.setLinkTable(self.up.getHostName(match2[i], True), match2[i]))
	    valTab.sort(key = lambda x: x[0])
	
	d = xbmcgui.Dialog()
        item = d.select("Wybór filmu", self.getItemTitles(valTab))
        if item != '':
	    videoID = str(valTab[item][1])
	    log.info('mID: ' + videoID)
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
			log.info('KINOPECETOWIEC - addDir() -> title: ' + title)
			log.info('KINOPECETOWIEC - addDir() -> url: ' + page)
			log.info('KINOPECETOWIEC - addDir() -> dstpath: ' + os.path.join(dstpath, SERVICE))
		cm = self.navigation.addVideoContextMenuItems({ 'service': SERVICE, 'title': urllib.quote_plus(self.chars.replaceChars(title)), 'url': urllib.quote_plus(page), 'path': os.path.join(dstpath, SERVICE) })
		liz.addContextMenuItems(cm, replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
    
      
    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title):
        ok=True
        if videoUrl == '':
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
            return False
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl, liz)
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
        icon = self.parser.getParam(params, "icon")
        link = self.parser.getParam(params, "url")
        vtitle = self.parser.getParam(params, "vtitle")
        service = self.parser.getParam(params, "service")
        action = self.parser.getParam(params, "action")
        path = self.parser.getParam(params, "path")

	if dbg == 'true':
		log.info ('name: ' + str(name))
		log.info ('title: ' + str(title))
		log.info ('category: ' + str(category))
		log.info ('page: ' + str(page))

	if page=='': page = 1
	
	#main menu	
	if name == None:
		self.listsMainMenu(SERVICE_MENU_TABLE)	
	#kategorie filmowe    
	elif category == self.setTable()[1]:
	    self.listsCategoriesMenu(MAINURL + '/categories')	    
	#najnowsze
	elif category == self.setTable()[2]:
	    self.getFilmTable(NEW_LINK + str(page), category, page)	
	#najczesciej ogladane
	elif category == self.setTable()[3]:
	    self.getFilmTable(POP_LINK + str(page), category, page)	
	#najczesciej komentowane
	elif category == self.setTable()[4]:
	    self.getFilmTable(COM_LINK + str(page), category, page)		
	#ulubione
	elif category == self.setTable()[5]:
	    self.getFilmTable(FAV_LINK + str(page), category, page)		
	#najwyzej ocenione
	elif category == self.setTable()[6]:
	    self.getFilmTable(SCR_LINK + str(page), category, page)	
	#wyroznione
	elif category == self.setTable()[7]:
	    self.getFilmTable(PRC_LINK + str(page), category, page)	
	#losowe
	elif category == self.setTable()[8]:
	    self.getFilmTable(RDM_LINK + str(page), category, page)

	#szukaj
	elif category == self.setTable()[10]:
	    text = self.searchInputText()
	    self.getSearchTable(self.searchTab(text))
	#Historia Wyszukiwania
	elif category == self.setTable()[11]:
	    t = self.history.loadHistoryFile(SERVICE)
#	    print str(t)
	    self.listsHistory(t)
	if category == 'history' and name != 'playSelectedMovie':
	    self.getSearchTable(self.searchTab(name))	
	
	#lista tytulow w kategorii
	if category > 0:
            if category.isdigit()==True:
                pagefix = title.replace(' ', '-')
                url = MAINURL + '/categories/' + category + '/' + str(page) + '/' + pagefix
                self.getFilmTable(url, category, page)	    
	    	    
        if name == 'playSelectedMovie':
            url = self.getHostTable(page)
            linkVideo = self.up.getVideoLink(url)
            if linkVideo != False:
                self.LOAD_AND_PLAY_VIDEO(linkVideo, title)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', SERVICE + ' - przepraszamy, chwilowa awaria.', 'Zapraszamy w innym terminie.')
        
        if service == SERVICE and action == 'download' and link != '':
			if dbg == 'true':
				log.info('KINOPECETOWIEC - handleService()[download][0] -> title: ' + urllib.unquote_plus(vtitle))
				log.info('KINOPECETOWIEC - handleService()[download][0] -> url: ' + urllib.unquote_plus(link))
				log.info('KINOPECETOWIEC - handleService()[download][0] -> path: ' + path)	
			if urllib.unquote_plus(link).startswith('http://'):
				urlTempVideo = self.getHostTable(urllib.unquote_plus(link))
				linkVideo = self.up.getVideoLink(urlTempVideo)
				if dbg == 'true':
					log.info('KINOPECETOWIEC - handleService()[download][1] -> title: ' + urllib.unquote_plus(vtitle))
					log.info('KINOPECETOWIEC - handleService()[download][1] -> temp url: ' + urlTempVideo)
					log.info('KINOPECETOWIEC - handleService()[download][1] -> url: ' + linkVideo)							
				if linkVideo != False:
					if dbg == 'true':
						log.info('KINOPECETOWIEC - handleService()[download][2] -> title: ' + urllib.unquote_plus(vtitle))
						log.info('KINOPECETOWIEC - handleService()[download][2] -> url: ' + linkVideo)
						log.info('KINOPECETOWIEC - handleService()[download][2] -> path: ' + path)							
					import downloader
					dwnl = downloader.Downloader()
					dwnl.getFile({ 'title': urllib.unquote_plus(vtitle), 'url': linkVideo, 'path': path })