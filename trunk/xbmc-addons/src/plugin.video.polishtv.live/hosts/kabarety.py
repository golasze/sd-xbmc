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

import pLog, settings, Parser, urlparser, pCommon

log = pLog.pLog()

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
SERVICE = 'kabarety'
MAINURL = 'http://www.kabarety.odpoczywam.net/'
LOGOURL = 'http://www.kabarety.odpoczywam.net/img/logo.png'
IMGURL = 'http://i.ytimg.com/vi/'

NAJ_LINK = MAINURL + '/bestof/page:'
NOW_LINK = MAINURL + '/index/page:'

SERVICE_MENU_TABLE = {1: "Najnowsze",
		      2: "Najlepsze",
		      3: "Kategorie",
                      4: "Szukaj",
		      5: "Historia Wyszukiwania"
		      }

class Kabarety:
    def __init__(self):
        log.info('Loading ' + SERVICE)
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
	self.history = pCommon.history()


    def setTable(self):
	return SERVICE_MENU_TABLE


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.addDir(SERVICE, 'main-menu', val, '', '', '', LOGOURL, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getCategoryTab(self,url):   
        strTab = []
        valTab = []
        data = self.cm.requestData(url)
        match = re.compile('<a href="(.+?)">(.+?)</a><br>').findall(data)
        if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(value[0])
		strTab.append(value[1])	
		valTab.append(strTab)
		strTab = []
	    valTab.sort(key = lambda x: x[1])
        return valTab


    def listsCategoriesMenu(self,url,category):
        table = self.getCategoryTab(url)
        for i in range(len(table)):
	    value = table[i]
	    title = value[1]
	    if title > 0:
		self.addDir(SERVICE, value[0], category, title, '', '', '', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTab(self, url):
        strTab = []
        valTab = []
        data = self.cm.requestData(url)
        link = data.replace('\n', '')
	match = re.compile('<a class="video-mini" title="(.+?)" href=".+?">.+?<span class="duration".+?<img class="video-mini-img".+?src="http://i.ytimg.com/vi/(.+?)/0.jpg" />').findall(link)
        if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(value[0])
		strTab.append(value[1])	
		valTab.append(strTab)
		strTab = []
	match = re.compile('<span><a href=".+?" class="next shadow-main">&raquo;</a></span>').findall(data)
	if len(match) > 0:
            strTab.append('Następna strona')
            strTab.append('')
            valTab.append(strTab) 	    
        return valTab

   
    def getFilmTable(self, url, page, category, name):
        table = self.getFilmTab(url)
        for i in range(len(table)):
	    value = table[i]
	    title = value[0]
	    img = IMGURL + value[1] + '/0.jpg'
	    if value[0] != 'Następna strona':
		self.addDir(SERVICE, 'playSelectedMovie', '', title, '', value[1], img, True, False)
	    else:
		page = str(int(page) + 1)
		self.addDir(SERVICE, name, category, value[0], '', page, '', True, False) 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsHistory(self, table):
	for i in range(len(table)):
	    if table[i] <> '':
		self.addDir(SERVICE, table[i], 'history', table[i], 'None', LOGOURL, 'None', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchTable(self, table):
        for i in range(len(table)):
	    value = table[i]
	    title = value[0]
	    img = IMGURL + value[1] + '/0.jpg'
	    self.addDir(SERVICE, 'playSelectedMovie', '', title, '', value[1], img, True, False)
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
        data = self.cm.requestData(MAINURL + '/search?q=' + text)
        link = data.replace('\n', '')
	match = re.compile('<a class="video-mini" title="(.+?)" href=".+?">.+?<span class="duration".+?<img class="video-mini-img".+?src="http://i.ytimg.com/vi/(.+?)/0.jpg" />').findall(link)
        if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(value[0])
		strTab.append(value[1])	
		valTab.append(strTab)
		strTab = []
        return valTab



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
    
      
    def LOAD_AND_PLAY_VIDEO(self, videoId):
        ok=True
        if videoId == '':
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
            return False
        try:
            url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId
            xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
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

	log.info ('name: ' + str(name))
	log.info ('title: ' + str(title))
	log.info ('category: ' + str(category))
	log.info ('page: ' + str(page))

	if page=='': page = 1
		
        if name == None:
            self.listsMainMenu(SERVICE_MENU_TABLE)	
   
	elif category == self.setTable()[1]:
            name = 'nic'
	    self.getFilmTable(NOW_LINK + str(page), page, category, name)	    

	elif category == self.setTable()[2]:
            name = 'nic'
	    self.getFilmTable(NAJ_LINK + str(page), page, category, name)	

	elif category == self.setTable()[3]:
            categoryfix = category + 'fix'
	    self.listsCategoriesMenu(MAINURL, categoryfix)

	elif category == self.setTable()[4]:
	    text = self.searchInputText()
	    self.getSearchTable(self.searchTab(text))
	elif category == self.setTable()[5]:
	    t = self.history.loadHistoryFile(SERVICE)
	    self.listsHistory(t)
	if category == 'history' and name != 'playSelectedMovie':
	    self.getSearchTable(self.searchTab(name))	
	
	if category == 'Kategoriefix':
            url = name + '/page:' + str(page)
            self.getFilmTable(url, page, category, name)	    
	    	    
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(page)
      
