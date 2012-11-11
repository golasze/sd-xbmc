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

mainUrl = 'http://bestplayer.tv/'
mainUrl2 = 'http://bestplayer.tv/filmy/'
mainUrl3 = 'http://bestplayer.tv/top100/'
logoUrl = mainUrl + 'images/logo.png'
first = '-strona-1.html'

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

MENU_TAB = {1: "Lektor",
	    2: "Napisy",
	    3: "Premiery",
            4: "TOP", 
            5: "Data wydania",
            6: "Szukaj" }

class BestPlayer:
    def __init__(self):
        log.info('Loading BestPlayer')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()

    def listsMainMenu(self, table):
        for num, val in table.items():
            self.addDir('bestplayer', 'main-menu', val, '', '', '', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsCategoriesMenu2(self):
        link = self.cm.requestData(mainUrl2)     
        match = re.compile('<a href="(.+?)z-lektorem.html" title="Filmy(.+?)"><span class="float-left">(.+?)</span><span class="float-right"></span></a></li>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'submenu', '', match[i][2], '', mainUrl + match[i][0] + 'z-lektorem-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))    

    def listsCategoriesMenu3(self):
        link = self.cm.requestData(mainUrl2)
        match = re.compile('<a href="(.+?)z-napisami.html" title="Filmy.+?"><span class="float-left">(.+?)</span><span').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'submenu', '', match[i][1], '', mainUrl + match[i][0] + 'z-napisami-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsCategoriesMenu4(self):
        link = self.cm.requestData(mainUrl2)
        match = re.compile('<a href="(.+?)premiery.html" title="Filmy(.+?)"><span class="float-left">(.+?)</span><span class="float-right"></span></a></li>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'submenu', '', match[i][2], '', mainUrl + match[i][0] + 'premiery-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsCategoriesMenu5(self):
        link = self.cm.requestData(mainUrl2)
        match = re.compile('<a href="filmy/rok(.+?).html" title="(.+?)"><span class="float-left">(.+?)</span><span class="float-right"></span></a></li>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'submenu', '', match[i][1], '', mainUrl + 'filmy/rok' + match[i][0] + '-strona-1.html', logoUrl, True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 
     
    def getFilmTable(self,url):
        link = self.cm.requestData(url)
        tabURL = link.replace('</div>', '').replace('<div class="fr" style="width:475px; margin-right:10px; margin-top:10px">', '').replace('&amp;', '').replace('quot;', '').replace('&amp;quot;', '')
        match = re.compile('<a href="(.+?)" title=""><img src="(.+?)" width.+?/></a>\n.+?<div style.+?star.png" />\n.+?<div>Opini:.+?\n.+?\n.+?\n.+?<h2><a href=".+?">(.+?)</a></h2>\n.+?Kategorie:.+?</a></p>\n.+?\n.+?<div class="p5 film-dsc" >(.+?)\n.+?').findall(tabURL)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'playSelectedMovie', '', match[i][2], match[i][3], match[i][0], mainUrl + match[i][1], True, False)   
        match2 = re.compile('<li class="round "><a href="(.+?)" class="next"></a></li>').findall(link)
        if len(match2) > 0:
             nexturl = match2[0]
             self.addDir('bestplayer', 'submenu', '', 'Następna strona', '', mainUrl + nexturl, '', True, False)     
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getFilmTable2(self,url):
        link = self.cm.requestData(url)
        tabURL = link.replace('</div>', '').replace('&amp;', '').replace('quot;', '').replace('&amp;quot;', '')
        match = re.compile('<a class=".+?"  href="(.+?)" title=""><img src="(.+?)" height=.+?/></a>\n.+?<div class="trigger.+?".+?star.png" />\n.+?<div class="trigger.+?".+?\n.+?<div class="trigger.+?".+?\n.+?\n.+?<div class="fr".+?\n.+?<h2><a href=".+?">(.+?)</a></h2>\n.+?Kategorie.+?\n.+?\n.+?<div class=".+?" class="p5 film-dsc".+?">(.+?)\n.+?<a class="trigger.+?"').findall(tabURL)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'playSelectedMovie', '', match[i][2], match[i][3], match[i][0], mainUrl + match[i][1], True, False)       
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))    

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
          text = k.getText()
        return text

    def searchTab(self):
        text = self.searchInputText()
        searchUrl = mainUrl
        values = {'q': text}
        headers = { 'User-Agent' : HOST }
        data = urllib.urlencode(values)
        req = urllib2.Request(searchUrl, data, headers)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        tabURL = link.replace('</div>', '').replace('&amp;', '').replace('quot;', '').replace('&amp;quot;', '')
        match = re.compile('<div class="movie-cover fl">\n.+?<a href="(.+?)" title=""><img src="(.+?)" width="150" height="200" alt="okladka" /></a>\n.+?<div.+?png" />\n.+?<div>O.+?\n.+?\n.+?<div.+?px">\n.+?<h2><a.+?>(.+?)</a></h2>\n.+?Kat.+?</a></p>\n.+?\n.+?<div class="p5 film-dsc" >(.+?)\n.+?<div style="margin-top: 10px;">').findall(tabURL)
        if len(match) > 0:
            for i in range(len(match)):
             self.addDir('bestplayer', 'playSelectedMovie', '', match[i][2], match[i][3], match[i][0], mainUrl + match[i][1], True, False)   
        match2 = re.compile('<li class="round "><a href="(.+?)" class="next"></a></li>').findall(link)
        if len(match2) > 0:
             nexturl = match2[0]
             self.addDir('bestplayer', 'submenu', '', 'Następna strona', '', mainUrl + nexturl, '', True, False)     
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   

    def getVideoID(self,url):
        videoID = ''
        link = self.cm.requestData(url)
        match = re.compile('<iframe src="(.+?)" style="border:0px; width: 740px; height: 475px;" scrolling="no"></iframe>').findall(link)
        if len(match) > 0:
            videoID = match[0]
        return videoID

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
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Lektor':
            self.listsCategoriesMenu2()
        elif name == 'main-menu' and category == 'Napisy':
            self.listsCategoriesMenu3()
        elif name == 'main-menu' and category == "Premiery":
            self.listsCategoriesMenu4()
        elif name == 'main-menu' and category == "TOP":
            self.getFilmTable2(mainUrl3)    
        elif name == 'main-menu' and category == 'Data wydania':
            self.listsCategoriesMenu5()
        elif name == 'main-menu' and category == 'Szukaj':
            self.searchTab()  
        elif name == 'submenu':
            self.getFilmTable(page)

        if name == 'playSelectedMovie':
            nUrl = mainUrl + page
            linkVideo = ''
            ID = ''
            ID = self.getVideoID(nUrl)
            if ID != '':
                linkVideo = self.up.getVideoLink(ID)
                if linkVideo != False:
                    self.LOAD_AND_PLAY_VIDEO(linkVideo)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', 'Maxvideo - tymczasowo wyczerpałeś limit ilości uruchamianych seriali.', 'Zapraszamy za godzinę.')
