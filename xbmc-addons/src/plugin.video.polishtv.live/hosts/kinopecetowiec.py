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


playURL = 'http://www.putlocker.com/embed/'
playURL2 = 'http://nextvideo.pl/'
playURL3 = 'http://www.sockshare.com/'
playURL4 = 'http://video.anyfiles.pl/'
playURL5 = 'http://www.novamov.com/'
playURL6 = 'http://odsiebie.pl/'
playURL7 = 'http://www.nowvideo.eu/'

SERVICE_MENU_TABLE = {1: "Kategorie Filmowe",
		      2: "Najnowsze",
		      3: "Szukaj" }

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
        match = re.compile('<img  src="(.+?)" width="164" height="220" border="0" alt=""/></a></div>').findall(data)
        if len(match) > 0:
          img = match
        else:
          img = []
        match = re.compile('<div class=".+?"><a href="(.+?)" title="(.+?)"><span').findall(data)
        if len(match) > 0:
          for i in range(len(match)):
            value = match[i]
            strTab.append(img[i])
            strTab.append(value[0])
            strTab.append(value[1])	
            valTab.append(strTab)
            strTab = []
	  valTab.sort(key = lambda x: x[2])
        return valTab


    def listsCategoriesMenu(self,url):
        table = self.getCategoryTab(url)
        for i in range(len(table)):
          value = table[i]
          img = value[0]
          url = value[1]
          title = value[2]
          if title > 0:
             self.addDir(SERVICE, 'submenu', '', title, '', url, img, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTab(self,url):   
        strTab = []
        valTab = []
        data = self.cm.requestData(url)
        match = re.compile('<img src="(.+?)" width="150" height="180" border="0" id="rotate').findall(data)
        if len(match) > 0:
          img = match
        else:
          img = []
        match = re.compile('<div class=".+?"> <a href="(.+?)">(.+?)</a>').findall(data)
        if len(match) > 0:
          for i in range(len(match)):
            value = match[i]
            strTab.append(img[i])
            strTab.append(value[0])
            strTab.append(value[1])	
            valTab.append(strTab)
            strTab = []
        return valTab


    def getFilmTab2(self,url):   
        strTab = []
        valTab = []
        data = self.cm.requestData(url)
        match = re.compile('<img src="(.+?)" width="126"  height="160" id="rotate').findall(data)
        if len(match) > 0:
          img = match
        else:
          img = []
        match = re.compile('<div class="video-title"><a href="(.+?)" title="(.+?)">').findall(data)
        if len(match) > 0:
          for i in range(len(match)):
            value = match[i]
            strTab.append(img[i])
            strTab.append(value[0])
            strTab.append(value[1])	
            valTab.append(strTab)
            strTab = []
        return valTab
    
    
    def getFilmTable(self,url):
        table = self.getFilmTab(url)
        link = self.cm.requestData(url)
        for i in range(len(table)):
          value = table[i]
          imgtab = value[0]
          urltab = value[1]
          titletab = value[2]
          if titletab > 0:
             self.addDir(SERVICE, 'movies', '', titletab, '', urltab, imgtab, True, False)   
        match2 = re.compile('<a href="(.+?)">&raquo;</a> </div>').findall(link)
        if len(match2) > 0:
             nexturl = match2[0]
             self.addDir(SERVICE, 'submenu', '', 'Następna strona', '', nexturl, '', True, False) 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTable2(self,url):
        table = self.getFilmTab2(url)
        link = self.cm.requestData(url)
        for i in range(len(table)):
          value = table[i]
          imgtab2 = value[0]
          urltab2 = value[1]
          titletab2 = value[2]
          if titletab2 > 0:
             self.addDir(SERVICE, 'movies', '', titletab2, '', urltab2, imgtab2, True, False)   
        match2 = re.compile('class="pagingnav">.+?</span><a href="(.+?)">').findall(link)
        if len(match2) > 0:
             nexturl = match2[0]
             self.addDir(SERVICE, 'submenu3', 'Najnowsze', 'Następna strona', '', nexturl, '', True, False) 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchTable(self):
        table = self.searchTab()
        for i in range(len(table)):
          value = table[i]
          imgtab3 = value[0]
          urltab3 = value[1]
          titletab3 = value[2]
          if titletab3 > 0:
             self.addDir(SERVICE, 'movies', '', titletab3, '', urltab3, imgtab3, True, False)   
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getHostTable(self,url):
        link = self.cm.requestData(url)
        
	match = re.compile('<iframe src="http://www.putlocker.com/.+?/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'Putlocker', '', playURL + match[i], 'http://www.qooymirrors.com/image/cache/data/putlocker-228x228.jpg', True, False) 
        else:
            match = re.compile('http://www.putlocker.com/.+?/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'Putlocker', '', playURL + match[i], 'http://www.qooymirrors.com/image/cache/data/putlocker-228x228.jpg', True, False)
        
	match = re.compile('<iframe src="http://nextvideo.pl/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'Nextvideo', '', playURL2 + match[i], 'http://b.vimeocdn.com/ps/319/040/3190402_300.jpg', True, False)
        else:
            match = re.compile('http://nextvideo.pl/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'Nextvideo', '', playURL2 + match[i], 'http://b.vimeocdn.com/ps/319/040/3190402_300.jpg', True, False)
        
	match = re.compile('<iframe src="http://www.sockshare.com/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'Sockshare', '', playURL3 + match[i], 'http://www.qooymirrors.com/image/cache/data/sockshare-228x228.jpg', True, False)
        else:
            match = re.compile('http://www.sockshare.com/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'Sockshare', '', playURL3 + match[i], 'http://www.qooymirrors.com/image/cache/data/sockshare-228x228.jpg', True, False)
        
	match = re.compile('<iframe src="http://video.anyfiles.pl/(.+?)".+?scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'AnyFiles', '', playURL4 + match[i], 'http://anyfiles.pl/anyfiles2.jpg', True, False)
        else:
            match = re.compile('http://video.anyfiles.pl/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'AnyFiles', '', playURL4 + match[i], 'http://anyfiles.pl/anyfiles2.jpg', True, False)
        
	match = re.compile('<iframe src="http://www.novamov.com/(.+?)".+?scrolling="no"></iframe>').findall(link)       
	if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'Novamov', '', playURL5 + match[i], 'http://www.p2pon.com/wp-content/uploads/2012/10/novamov_trans_refl_glow_01-300x2251.png', True, False)
        else:
            match = re.compile('http://www.novamov.com/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'Novamov', '', playURL5 + match[i], 'http://www.p2pon.com/wp-content/uploads/2012/10/novamov_trans_refl_glow_01-300x2251.png', True, False)
        
	match = re.compile('<iframe src="http://odsiebie.pl/(.+?)".+?scrolling="no"></iframe>').findall(link)        
	if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'OdSiebie', '', playURL6 + match[i], 'http://www.polskiprogram.pl/wp-content/uploads/2010/12/odsiebie_pl-150x150.png', True, False)
        else:
            match = re.compile('http://odsiebie.pl/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'OdSiebie', '', playURL6 + match[i], 'http://www.polskiprogram.pl/wp-content/uploads/2010/12/odsiebie_pl-150x150.png', True, False)
        match = re.compile('<iframe src="http://www.nowvideo.eu/(.+?)".+?scrolling="no"></iframe>').findall(link)
        
	if len(match) > 0:
            for i in range(len(match)):
                     self.addDir(SERVICE, 'playSelectedMovie', '', 'Nowvideo', '', playURL7 + match[i], 'http://www.nowvideo.eu/images/logo.png', True, False)
        else:
            match = re.compile('http://www.nowvideo.eu/(.+?)\n').findall(link)
            if len(match) > 0:
                    for i in range(len(match)):
                         match[0]=re.sub('\r','',match[0])
                         self.addDir(SERVICE, 'playSelectedMovie', '', 'Nowvideo', '', playURL7 + match[i], 'http://www.nowvideo.eu/images/logo.png', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 
                

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


    def addDir(self, service, name, category, title, plot, link, iconimage, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(link)
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
	
	#print str(name)
	#print str(title)
	#print str(category)
	#print str (page)
	
        if name == None:
            self.listsMainMenu(SERVICE_MENU_TABLE)
        elif name == 'main-menu' and category == self.setTable()[1]:
            self.listsCategoriesMenu(MAINURL + '/categories')	    
        elif name == 'main-menu' and category == self.setTable()[2]:
	    self.getFilmTable2(MAINURL + '/videos')
        elif name == 'main-menu' and category == self.setTable()[3]:
	    self.getSearchTable()
	
	#nastepna strona
	elif category == 'Najnowsze' and title == 'Następna strona':
	    self.getFilmTable2(page)
	    
        elif name == 'submenu':
            self.getFilmTable(page)	    
	    
        elif name == 'movies':
            self.getHostTable(page)
	    
        if name == 'playSelectedMovie':
                linkVideo = self.up.getVideoLink(page)
                if linkVideo != False:
                    self.LOAD_AND_PLAY_VIDEO(linkVideo)
                else:
                    d = xbmcgui.Dialog()
                    d.ok('Brak linku', 'KinoPecetowiec - przepraszamy, chwilowa awaria.', 'Zapraszamy w innym terminie.')
