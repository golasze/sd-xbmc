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
COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "ekinotv.cookie"
LOGOURL = ptv.getAddonInfo('path') + os.path.sep + "images" + os.path.sep + "ekinotv.png"
NEXTURL = ptv.getAddonInfo('path') + os.path.sep + "images" + os.path.sep + "next.png"

import pLog, settings, Parser, urlparser, pCommon, Navigation, Errors, downloader

log = pLog.pLog()
cj = cookielib.LWPCookieJar()

sortby = ptv.getSetting('ekinotv_sort')
sortorder = ptv.getSetting('ekinotv_sortorder')
quality = ptv.getSetting('ekinotv_quality')
username = ptv.getSetting('ekinotv_login')
password = ptv.getSetting('ekinotv_password')
dstpath = ptv.getSetting('default_dstpath')
dbg = ptv.getSetting('default_debug')

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
SERVICE = 'ekinotv'
MAINURL = 'http://www.ekino.tv/'
MAINURLSE = 'http://www.ekino.tv/seriale-online.html'
MAINURLSR = 'http://www.ekino.tv/szukaj-wszystko,'
POPULAR = ',wszystkie,wszystkie,1900-2013,.html?sort_field=odslony&sort_method=desc'

if username=='' or password=='':
    pr = ''
else:
    pr = '?premium&player=1'

SERVICE_MENU_TABLE =  {1: "Filmy [wg. gatunków]",
                       2: "Filmy [lektor]",
                       3: "Filmy [napisy]",
                       4: "Filmy [dubbing]",
                       5: "Filmy [polskie]",
                       6: "Filmy [najpopularniejsze]",
                       7: "Seriale",
                       8: "Wyszukaj",
                       9: "Historia Wyszukiwania"
                       }

class EkinoTV:
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
	self.dir = pCommon.common()
  
  
    def requestLoginData(self):
        if username=='' or password=='':
            xbmc.executebuiltin("XBMC.Notification(Niezalogowany, uzywam Player z limitami,2000)")
        else:
            url = MAINURL + "logowanie.html"
            self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
            query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': COOKIEFILE, 'use_post': True, 'return_data': True }
            postdata = { 'form_login_username': username, 'form_login_password': password }
            try:
                    data = self.cm.getURLRequestData(query_data, postdata)
            except Exception, exception:
                    traceback.print_exc()
                    self.exception.getError(str(exception))
                    exit()
            if self.isLoggedIn(data):
                xbmc.executebuiltin("XBMC.Notification(" + username + ", Zostales poprawnie zalogowany,2000)")
            else:
                xbmc.executebuiltin("XBMC.Notification(Blad logowania, uzywam Player z limitami,2000)")

    def isLoggedIn(self, data):
        lStr = 'href="premium.html">Premium'
        if lStr in data:
          return True
        else:
          return False


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
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        r = re.compile('<ul class="videosCategories">(.+?)<span>Wersja</span>', re.DOTALL).findall(data)    
        if len(r)>0:
          r2 = re.compile('<a href="(.+?).html">(.+?)</a>').findall(r[0])
          if len(r2)>0:
              for i in range(len(r2)):
                  value = r2[i]
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
		self.addDir(SERVICE, 'category', value[0], title, '', '', '', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))       


    def getFilmTab(self, url, category):
        strTab = []
        valTab = []
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
            data = self.cm.getURLRequestData(query_data)
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
        match = re.compile('class.+?src="(.+?)" alt=.+?/>.\n.+?class=.+?>.\n.+?<h2><a href="(.+?)">(.+?)</a></h2>').findall(data)
        if len(match) > 0:                
            for i in range(len(match)):
                value = match[i]
                strTab.append(value[0])
                strTab.append(value[1])
                strTab.append(value[2])
                valTab.append(strTab)
                strTab = []
	match = re.compile('<li class="active"><a href=".+?">.+?</a></li>.\n.+?<li>').findall(data)
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
	    title = value[2]
	    img = value[0].replace('_small', '')
	    if value[2] != 'Następna strona':
		self.addDir(SERVICE, 'playSelectedMovie', '', title, '', MAINURL + '/' + value[1] + pr, img, True, False)
	    else:
		page = str(int(page) + 1)
		self.addDir(SERVICE, 'category', category, value[2], '', page, NEXTURL, True, False) 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getAlfTab(self,url):   
        strTab = []
        valTab = []
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        r = re.compile('class="serialsmenu">(.+?)<div class="moviesWrap serialsList">', re.DOTALL).findall(data)    
        if len(r)>0:
          r2 = re.compile('<a href="(.+?).html"><span class="name">(.+?)</span><span').findall(r[0])
          if len(r2)>0:
              for i in range(len(r2)):
                  value = r2[i]
                  strTab.append(value[0])
                  strTab.append(value[1])
                  valTab.append(strTab)
                  strTab = []
              valTab.sort(key = lambda x: x[1])
        return valTab


    def listsSerialsMenu(self,url):
        table = self.getAlfTab(url)
        for i in range(len(table)):
	    value = table[i]
	    title = value[1]
	    if title > 0:
		self.addDir(SERVICE, 'serial', value[0], title, '', '', '', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getSerialTab(self, url):
        strTab = []
        valTab = []
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
            data = self.cm.getURLRequestData(query_data)
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
        match = re.compile('class="poster" src="(.+?)" alt=.+?/><span class=".+"?">.+?</span></div>.\n.+?<div class=".+?">.\n.+?<h2><a href="(.+?).html">(.+?)</a></h2>').findall(data)
        if len(match) > 0:                
            for i in range(len(match)):
                value = match[i]
                strTab.append(value[0])
                strTab.append(value[1])
                strTab.append(value[2])
                valTab.append(strTab)
                strTab = []
	match = re.compile('<li class="active"><a href=".+?add_date,desc.html">.+?</a></li>.\n.+?<li>').findall(data)
	if len(match) > 0:
            strTab.append('')
            strTab.append('')
            strTab.append('Następna strona')
            valTab.append(strTab) 	    
        return valTab

   
    def getSerialTable(self, url, category, page):
        table = self.getSerialTab(url)
        for i in range(len(table)):
	    value = table[i]
	    title = value[2]
	    img = value[0].replace('_small', '')
	    if value[2] != 'Następna strona':
		self.addDir(SERVICE, 'sezon', MAINURL + value[1], title, '', img, img, True, False)
	    else:
		page = str(int(page) + 1)
		self.addDir(SERVICE, 'serial', category, value[2], '', page, NEXTURL, True, False) 
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getSezonTable(self,url,category,img):
	query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        match = re.compile('<div class="h">Sezon(.+?)</div>').findall(data)
	if len(match) > 0:
            for i in range(len(match)):
                title = 'Sezon' + match[i]
                self.addDir(SERVICE, 'episode', category, title, '', img, img, True, False)
    	xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getPlayTable(self,url,category,title,img):   
        s = title.replace('Sezon ', '')
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
	link = data.replace(' ', '')
        r = re.compile('<div class="h">Sezon ' + s + '</div>(.+?)</ul>', re.DOTALL).findall(data)    
        if len(r)>0:
          r2 = re.compile('<a href="(.+?)epizod,(.+?).html">\r\n(.+?)</a>').findall(r[0])
          if len(r2)>0:
              for i in range(len(r2)):
                  t = 's' + s + 'e' + r2[i][1] + ' - ' + r2[i][2].replace('  ', '')
                  l = MAINURL + r2[i][0] + 'epizod,' + r2[i][1] + '.html' + pr
                  self.addDir(SERVICE, 'playSelectedMovie', '', t, '', l, img, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def setLinkTable(self, url, host):
        strTab = []
	strTab.append(url)
	strTab.append(host)
	return strTab

	
    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[1])
        return out 

    def getHostTable(self,url):
	linkVideo = ''
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': COOKIEFILE, 'use_post': False, 'return_data': True }
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        match = re.compile("""url: '(.+?)'""").findall(data)
	if len(match) > 0:
            linkVideo = match[0]
            log.info("final link: " + linkVideo)
            return linkVideo



    def getHostingTable(self,url):
	valTab = []
	videoID = ''
	query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
	link = data.replace('<div class="s-quality_mid"></div>', '').replace('<div class="s-quality_low"></div>', '').replace('<div class="s-quality_high"></div>', '')
	match = re.compile('<li class.+?><a href="(.+)player(.+?)">(.+?)</a></li>').findall(link) 
	if len(match) > 0:
            for i in range(len(match)):
                links = MAINURL + match[i][0] + 'player' + match[i][1]
                valTab.append(self.setLinkTable(links, match[i][2]))
            valTab.sort(key = lambda x: x[0])	
            d = xbmcgui.Dialog()
            item = d.select("Wybór hostingu", self.getItemTitles(valTab))
            print str(item)
            if item != -1:
                videoID = str(valTab[item][0])
                log.info('mID: ' + videoID)
            return videoID
        else:
            return False


    def getLinkTable(self,url):
	linkVideo = ''
	query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
		data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
		traceback.print_exc()
		self.exception.getError(str(exception))
		exit()
        match = re.compile('style="display:none;"><iframe src="(.+?)"').findall(data)
	if len(match) > 0:
            linkVideo = match[0]
            log.info("final link: " + linkVideo)
        return linkVideo

    def searchInputText(self, SER):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
	    text = k.getText()
	    self.history.addHistoryItem(SER, text)
        return text

    def getStype(self):
        stype = ''
        wybierz = ['Filmy','Seriale']
        d = xbmcgui.Dialog()
        item = d.select("Co chcesz znaleść?", wybierz)
        if item == 0:
            stype =  'filmy'
        elif item == 1:
            stype = 'seriale'
        return stype

    def listsHistory(self, table, ser):
	for i in range(len(table)):
	    if table[i] <> '':
		self.addDir(SERVICE, ser, 'history', table[i], 'None', 'None', 'None', True, False)
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
	if dstpath != "None" or not dstpath and name == 'playSelectedMovie':
		if dbg == 'true':
			log.info(SERVICE + ' - addDir() -> title: ' + title)
			log.info(SERVICE + ' - addDir() -> url: ' + page)
			log.info(SERVICE + ' - addDir() -> dstpath: ' + os.path.join(dstpath, SERVICE))
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
            d.ok(SERVICE + ' - przepraszamy', 'Darmowy player premium jest teraz niedostępny.', 'Spróbuj później lub kup konto premium.')        
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

	if str(page)=='None' or page=='': page = 0

	if sortby=='ocena':
          sSort = '?sort_field=ocena&sort_method='
        if sortby=='popularnosc':
          sSort = '?sort_field=odslony&sort_method='
        if sortby=='data dodania':
          sSort = '?sort_field=data-dodania&sort_method='
        if sortby=='tytul':
          sSort = '?sort_field=alfabetycznie&sort_method='
        if sortby=='data premiery':
          sSort = '?sort_field=data-premiery&sort_method='

	if quality=='wszystkie':
          sQua = 'wszystkie'
        if quality=='wysoka':
          sQua = 'wysoka-jakosc'
        if quality=='srednia':
          sQua = 'srednia-jakosc'
        if quality=='niska':
          sQua = 'niska-jakosc'
      
        if sortorder=='malejaco':
          sHow = 'desc'
        else:
          sHow = 'asc'


	#main menu	
	if name == None:
            self.requestLoginData()
	    self.listsMainMenu(SERVICE_MENU_TABLE)	
	#gatunki    
	elif category == self.setTable()[1]:
	    self.listsCategoriesMenu(MAINURL + 'kategorie.html', category)	    
	#lektor
	elif category == self.setTable()[2]:
            url = MAINURL + 'kategorie' + ',' + str(page) + ',lektor,' + sQua + ',1900-2013,.html' + sSort + sHow
	    self.getFilmTable(url, category, page)	
	#napisy 
	elif category == self.setTable()[3]:
            url = MAINURL + 'kategorie' + ',' + str(page) + ',napisy,' + sQua + ',1900-2013,.html' + sSort + sHow           
	    self.getFilmTable(url, category, page)
	#dubbing
	elif category == self.setTable()[4]:
            url = MAINURL + 'kategorie' + ',' + str(page) + ',dubbing,' + sQua + ',1900-2013,.html' + sSort + sHow           
	    self.getFilmTable(url, category, page)
	#PL
	elif category == self.setTable()[5]:
            url = MAINURL + 'kategorie' + ',' + str(page) + ',polskie,' + sQua + ',1900-2013,.html' + sSort + sHow            
	    self.getFilmTable(url, category, page)
	#najpopularniejsze
	elif category == self.setTable()[6]:
            url = MAINURL + 'kategorie' + ',' + str(page) + POPULAR
	    self.getFilmTable(url, category, page)		
	#seriale
	elif category == self.setTable()[7]:
	    self.listsSerialsMenu(MAINURLSE)		
	#wyszukaj   
	elif category == self.setTable()[8]:
            SERCH = self.getStype()
            text = self.searchInputText(SERVICE + SERCH)
            if  SERCH == 'filmy':
                url = MAINURLSR + text + ',filmy,' + str(page) + '.html'
                self.getFilmTable(url, category, page)
            else:
                url = MAINURLSR + text + ',seriale,' + str(page) + '.html'
                self.getSerialTable(url, category, page)
	#Historia Wyszukiwania
	elif category == self.setTable()[9]:
            SER = self.getStype()
	    t = self.history.loadHistoryFile(SERVICE + SER)
	    self.listsHistory(t, SER)
	if category == 'history' and name == 'filmy':
            url = MAINURLSR + title + ',filmy,' + str(page) + '.html'
            self.getFilmTable(url, category, page)
	if category == 'history' and name == 'seriale':
            url = MAINURLSR + title + ',seriale,' + str(page) + '.html'
            self.getSerialTable(url, category, page)
	
	#lista tytulow 
	if name == 'category':
            url = MAINURL + category + ',' + str(page) + ',wszystkie,wszystkie,1900-2013,.html' + sSort + sHow
            self.getFilmTable(url, category, page)

	#lista seriali
	if name == 'serial':
            url = MAINURL + category + ',' + str(page) + ',add_date,desc.html'
            self.getSerialTable(url, category, page)

	if name == 'sezon':
            url = category + '.html'
            self.getSezonTable(url, category, page)

	if name == 'episode':
            url = category + '.html'
            self.getPlayTable(url, category, title, page)
	    	    
        if name == 'playSelectedMovie':
            if username=='' or password=='':
                videoID = self.getHostingTable(page)
                if videoID != False:
                    linkVideo = self.up.getVideoLink(self.getLinkTable(videoID))
                else:
                    d = xbmcgui.Dialog()
                    d.ok(SERVICE + ' - przepraszamy', 'Ten materiał nie został jeszcze dodany', 'Zapraszamy w innym terminie.')
                    return False
            else: 
                linkVideo = self.getHostTable(page)
            if linkVideo != False:
                self.LOAD_AND_PLAY_VIDEO(linkVideo, title)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', SERVICE + ' - przepraszamy, chwilowa awaria.', 'Zapraszamy w innym terminie.')

        
        if service == SERVICE and action == 'download' and link != '':
                        self.dir.checkDir(os.path.join(dstpath, SERVICE))
			if dbg == 'true':
				log.info(SERVICE + ' - handleService()[download][0] -> title: ' + urllib.unquote_plus(vtitle))
				log.info(SERVICE + ' - handleService()[download][0] -> url: ' + urllib.unquote_plus(link))
				log.info(SERVICE + ' - handleService()[download][0] -> path: ' + path)	
			if urllib.unquote_plus(link).startswith('http://'):
                            if username=='' or password=='':
				urlTempVideo = self.getHostingTable(urllib.unquote_plus(link))
				linkVideo = self.up.getVideoLink(self.getLinkTable(urlTempVideo))
                                if dbg == 'true':
                                            log.info(SERVICE + ' - handleService()[download][1] -> title: ' + urllib.unquote_plus(vtitle))
                                            log.info(SERVICE + ' - handleService()[download][1] -> temp url: ' + urlTempVideo)
                                            log.info(SERVICE + ' - handleService()[download][1] -> url: ' + linkVideo)	
			    else:
                                linkVideo = self.getHostTable(urllib.unquote_plus(link))
                                if dbg == 'true':
                                            log.info(SERVICE + ' - handleService()[download][2] -> title: ' + urllib.unquote_plus(vtitle))
                                            log.info(SERVICE + ' - handleService()[download][2] -> url: ' + linkVideo)							
			    if linkVideo != False:
				    if dbg == 'true':
					    log.info(SERVICE + ' - handleService()[download][3] -> title: ' + urllib.unquote_plus(vtitle))
					    log.info(SERVICE + ' - handleService()[download][3] -> url: ' + linkVideo)
					    log.info(SERVICE + ' - handleService()[download][3] -> path: ' + path)							
				    dwnl = downloader.Downloader()
				    dwnl.getFile({ 'title': urllib.unquote_plus(vtitle), 'url': linkVideo, 'path': path })
