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

import pLog, settings, Parser, pCommon

log = pLog.pLog()

mainUrl = 'http://serialnet.pl'
watchUrl = mainUrl + '/ogladaj/'

version = ptv.getSetting('serialnet_wersja')

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

class SerialNet:
    def __init__(self):
        log.info('Loading SerialNet')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.cm = pCommon.common()
        
 
    def getSerialsTable(self):
        strTab = []
        outTab = []
        link = self.cm.requestData(mainUrl)
        #<li><a href="http://serialnet.pl/serial/1-1023/10-things-i-hate-about-you">10 Things I Hate About You <
        match = re.compile('<li><a href="http://serialnet.pl/serial/(.+?)">(.+?)<').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                strTab.append(match[i][1])
                strTab.append('http://serialnet.pl/serial/' + match[i][0])
                outTab.append(strTab)
                strTab = []
        outTab.sort(key = lambda x: x[0])
        return outTab        
    

    def getInfo(self,data):
        outTab = []       
        #<meta property="og:image" content="http://static.serialnet.pl/thumbs/zakochana-zlosnica.jpg"/>
        match = re.compile('<meta property="og:image" content="(.+?)"/>').findall(data)
        if len(match) > 0:
            imageLink = match[0]
        else:
            imageLink = ''
        outTab.append(imageLink)

        d = data.replace("<br/>","").replace("\n","")
        match = re.compile('<p><fb:like href=.+?</p><strong>(.+?)</strong></p></div>').findall(d)
        if len(match) > 0:
            desc = match[0]
        else:
            desc = ''
        outTab.append(desc)
        return outTab
    

    def showSerialTitles(self):
        tab = self.getSerialsTable()
        if len(tab) > 0:
            for i in range(len(tab)):
                self.addDir('serialnet', 'serial-title', 'None', tab[i][0], '', tab[i][1], '', True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

    def showSeason(self, url):  
        link = self.cm.requestData(url)       
        info = self.getInfo(link)
        #<h3>Sezon 1</h3></div>
        match = re.compile('<div style=".+?"><h3>(.+?)</h3></div>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                if 'Sezon' in match[i]:
                    self.addDir('serialnet', 'serial-season', 'None', match[i], info[1], url, info[0], True, False)
            #zmien view na "Media Info 2"
            xbmcplugin.setContent(int(sys.argv[1]),'tvshows')
            xbmc.executebuiltin("Container.SetViewMode(503)")
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def showSerialParts(self, url, title):
        link = self.cm.requestData(url)
        info = self.getInfo(link)
        tTab = title.split(' ')
        num = tTab[1]        
        s = "sezon-" + str(num)               
        #href="http://serialnet.pl/ogladaj/1-20/10-things-i-hate-about-you-sezon-1-odcinek-20"><b>Odcinek: 20 : Revolution</b>
                                                                                              #<b>Odcinek: 1</b>
        match = re.compile('href="(.+?)' + s + '(.+?)"><b>Odcinek:(.+?)</b>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                oTab = match[i][2].split(':')
                if len(oTab)==2:
                    episode = 'Odcinek ' + oTab[0] + ' - ' + oTab[1]
                else:
                    episode = 'Odcinek ' + oTab[0]
                self.addDir('serialnet', 'playSelectedMovie', 'None', episode, info[1], match[i][0] + s + match[i][1], info[0], True, False)
            #zmien view na "Media Info 2"
            xbmcplugin.setContent(int(sys.argv[1]),'tvshows')
            xbmc.executebuiltin("Container.SetViewMode(503)")    
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    def getVideoUrl(self, url):
        link = self.cm.requestData(url)       
        #<iframe id="framep" class="radi" src="http://serialnet.pl/play.php?t=1-18"
        match = re.compile('<iframe id="framep" class="radi" src="(.+?)"').findall(link)
        if len(match) > 0:
            nUrl = match[0]
            if version == 'false':
                d = xbmcgui.Dialog()
                item = d.select("Wybór wersji", ["Napisy","Bez lektora i napisow"])
                if item != '':
                    log.info(item)
                    if item == 0:
                        nUrl = match[0] + '&wersja=napisy'
                    if item == 1:
                        nUrl = match[0] + '&wersja=oryginalny'
                    
            link = self.cm.requestData(nUrl)    
            #log.info(link)
            #var flm = escape('http://50.7.220.66/folder/432ee8003a064ecc0eb46abfa59a044a_8555.mp4');
            match_watch = re.compile("var flm = escape\('(.+?)'\);").findall(link)
            if len(match_watch) > 0:
                videoUrl = match_watch[0]
            else:
                videoUrl = ''
            return videoUrl
        

    def addDir(self, service, name, category, title, plot, link, iconimage, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(link)
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
            self.showSerialTitles()
        elif name == 'serial-title':
            self.showSeason(page)
        elif name == 'serial-season' and title != None and page != None:    
            self.showSerialParts(page, title)
        if name == 'playSelectedMovie':
            log.info('video url: ' + page)
            videoUrl = self.getVideoUrl(page)
            print videoUrl
            if videoUrl != '':
                self.LOAD_AND_PLAY_VIDEO(videoUrl)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', 'SerialNet.pl - nie znaleziono linku')
