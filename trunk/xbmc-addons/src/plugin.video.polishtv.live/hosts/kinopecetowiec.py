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
SERVICE = 'kinopecetowiec'
MAINURL = 'http://www.kino.pecetowiec.pl'
LOGOURL = MAINURL + '/images/logo-pecetowiec-filmy-online2.jpg'
IMGURL = MAINURL + '/chimg/'
NEW_LINK = MAINURL + '/videos/basic/mr/'

playURL = 'http://www.putlocker.com/embed/'
playURL2 = 'http://nextvideo.pl/'
playURL3 = 'http://www.sockshare.com/'
playURL4 = 'http://video.anyfiles.pl/'
playURL5 = 'http://www.novamov.com/'
playURL6 = 'http://odsiebie.pl/'
playURL7 = 'http://www.nowvideo.eu/'

SERVICE_MENU_TABLE = {1: "Kategorie Filmowe",
		      2: "Najnowsze",
		      3: "Szukaj",
		      }

class KinoPecetowiec:
    def __init__(self):
        log.info('Loading ' + SERVICE)
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()


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
        match = re.compile('<div class=".+?"><a href="http://www.kino.pecetowiec.pl/categories/(.+?)/.+?" title="(.+?)"><span').findall(data)
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
          title = value[1]
          if title > 0:
             self.addDir(SERVICE, 'category', value[0], title, '', '', img, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTab(self, url, category):
        strTab = []
        valTab = []
        data = self.cm.requestData(url)
	#Najnowsze
	if category == self.setTable()[2]:
	    match = re.compile('<div class="video-title"><a href="http://www.kino.pecetowiec.pl/video/(.+?)/(.+?)" title="(.+?)">').findall(data)
	else:
	#Kategorie
	    match = re.compile('<div class="channel-details-thumb-box-texts"> <a href="http://www.kino.pecetowiec.pl/video/(.+?)/(.+?)">(.+?)</a><br/>').findall(data)
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
	  if value[2] != 'Następna strona':
	    self.addDir(SERVICE, 'playSelectedMovie', '', value[2], '', value[1], value[0], True, False)
	  else:
	    page = str(int(page) + 1)
            self.addDir(SERVICE, 'category', category, value[2], '', page, '', True, False) 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchTable(self):
        table = self.searchTab()
        for i in range(len(table)):
          value = table[i]
#         movielink = value[1]
          self.addDir(SERVICE, 'playSelectedMovie', '', value[2], '', value[1], value[0], True, False)   
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def setLinkTable(self, host, url):
        strTab = []
	strTab.append(host)
	strTab.append(url)
	return strTab

    
    def getHostTable(self,url):
	valTab = []
        link = self.cm.requestData(url)
        
	match = re.compile('<iframe src="http://www.putlocker.com/.+?/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
		valTab.append(self.setLinkTable('putlocker', playURL + match[i]))
        else:
            match = re.compile('http://www.putlocker.com/.+?/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
		    valTab.append(self.setLinkTable('putlocker', playURL + match[i]))
        
	match = re.compile('<iframe src="http://nextvideo.pl/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
		valTab.append(self.setLinkTable('nextvideo', playURL2 + match[i]))
        else:
            match = re.compile('http://nextvideo.pl/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
		    match[0]=re.sub('\r','',match[0])
		    valTab.append(self.setLinkTable('nextvideo', playURL2 + match[i]))
        
	match = re.compile('<iframe src="http://www.sockshare.com/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
		valTab.append(self.setLinkTable('sockshare', playURL3 + match[i]))
        else:
            match = re.compile('http://www.sockshare.com/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
                    match[0]=re.sub('\r','',match[0])
		    valTab.append(self.setLinkTable('sockshare', playURL3 + match[i]))
        
	match = re.compile('<iframe src="http://video.anyfiles.pl/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
		valTab.append(self.setLinkTable('anyfiles', playURL4 + match[i]))
        else:
            match = re.compile('http://video.anyfiles.pl/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
                    match[0]=re.sub('\r','',match[0])
                    valTab.append(self.setLinkTable('anyfiles', playURL4 + match[i]))
        
	match = re.compile('<iframe src="http://www.novamov.com/(.+?)".+?scrolling="no"></iframe>').findall(link)       
	if len(match) > 0:
            for i in range(len(match)):
		valTab.append(self.setLinkTable('novamov', playURL5 + match[i]))
        else:
            match = re.compile('http://www.novamov.com/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
                    match[0]=re.sub('\r','',match[0])
		    valTab.append(self.setLinkTable('novamov', playURL5 + match[i]))
        
	match = re.compile('<iframe src="http://odsiebie.pl/(.+?)".+?scrolling="no"></iframe>').findall(link)        
	if len(match) > 0:
            for i in range(len(match)):
                valTab.append(self.setLinkTable('odsiebie', playURL6 + match[i]))
        else:
            match = re.compile('http://odsiebie.pl/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
                    match[0]=re.sub('\r','',match[0])
                    valTab.append(self.setLinkTable('odsiebie', playURL6 + match[i]))

        match = re.compile('<iframe src="http://www.nowvideo.eu/(.+?)".+?scrolling="no"></iframe>').findall(link)       
	if len(match) > 0:
            for i in range(len(match)):
                valTab.append(self.setLinkTable('nowvideo', playURL7 + match[i]))
        else:
            match = re.compile('http://www.nowvideo.eu/(.+?)\n').findall(link)
            if len(match) > 0:
                for i in range(len(match)):
		    match[0]=re.sub('\r','',match[0])
                    valTab.append(self.setLinkTable('nowvideo', playURL7 + match[i]))
        
	d = xbmcgui.Dialog()
        item = d.select("Wybór filmu", self.getItemTitles(valTab))
        if item != '':
	    videoID = str(valTab[item][1])
	    log.info('mID: ' + videoID)
            return videoID

	
    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[0])
        return out 
                

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
          text = k.getText()
        return text


    def searchTab(self):
        strTab = []
        valTab = []
        text = self.searchInputText()
        values = {'search_id': text}
        headers = { 'User-Agent' : HOST }
        data = urllib.urlencode(values)
        req = urllib2.Request(MAINURL + '/search/', data, headers)
        response = urllib2.urlopen(req)
        link = response.read()
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
	
	#main menu	
        if name == None:
            self.listsMainMenu(SERVICE_MENU_TABLE)	
	#kategorie filmowe    
	elif category == self.setTable()[1]:
	    self.listsCategoriesMenu(MAINURL + '/categories')	    
	#najnowsze
	elif category == self.setTable()[2]:
	    self.getFilmTable(NEW_LINK + str(page), category, page)	
	#szukaj
	elif category == self.setTable()[3]:
	    self.getSearchTable()
	#lista tytulow w kategorii    
	elif name == 'category':
	    url = MAINURL + '/categories/' + category + '/' + str(page) + '/'
	    self.getFilmTable(url, category, page)	    
	    	    
        if name == 'playSelectedMovie':
            url = self.getHostTable(page)
            linkVideo = self.up.getVideoLink(url)
            if linkVideo != False:
                self.LOAD_AND_PLAY_VIDEO(linkVideo)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', SERVICE + ' - przepraszamy, chwilowa awaria.', 'Zapraszamy w innym terminie.')
