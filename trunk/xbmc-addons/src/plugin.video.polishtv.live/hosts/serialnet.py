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

import pLog, settings, Parser, common

log = pLog.pLog()

mainUrl = 'http://serialnet.pl'
imageUrl = 'http://static.serialnet.pl/thumbs/'
watchUrl = mainUrl + '/ogladaj/'

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

class SerialNet:
    def __init__(self):
        log.info('Loading SerialNet')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.cm = common.common()
        
 
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
    

    def getImage(self,url):
        #http://static.serialnet.pl/thumbs/swiat-wedlug-kiepskich.png
        #http://serialnet.pl/serial/2-759/swiat-wedlug-kiepskich
        uTab = url.split('/')
        imageLink=imageUrl + uTab[5] + '.jpg'
        return imageLink
    

    def showSerialTitles(self):
        tab = self.getSerialsTable()
        if len(tab) > 0:
            for i in range(len(tab)):
                imageLink = self.getImage(tab[i][1])
                self.addDir('serialnet', 'serial-title', 'None', tab[i][0], tab[i][1], imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

    def showSeason(self, url):  
        imageLink = self.getImage(url)
        link = self.cm.requestData(url)
        #<h3>Sezon 1</h3></div>
        match = re.compile('<div style=".+?"><h3>(.+?)</h3></div>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                if 'Sezon' in match[i]:
                    self.addDir('serialnet', 'serial-season', 'None', match[i], url, imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def showSerialParts(self, url, title):
        imageLink = self.getImage(url)
        tTab = title.split(' ')
        num = tTab[1]
        
        s = "sezon-" + str(num)        
        
        print s
        
        link = self.cm.requestData(url)
        #href="http://serialnet.pl/ogladaj/1-20/10-things-i-hate-about-you-sezon-1-odcinek-20"><b>Odcinek: 20 : Revolution</b>
                                                                                                #<b>Odcinek: 1</b>
        match = re.compile('href="(.+?)' + s + '(.+?)"><b>Odcinek:(.+?)</b>').findall(link)
        if len(match) > 0:
            print str(match)
            for i in range(len(match)):
                
                oTab = match[i][2].split(':')
                if len(oTab)==2:
                    episode = 'Odcinek ' + oTab[0] + ' - ' + oTab[1]
                else:
                    episode = 'Odcinek ' + oTab[0]
                self.addDir('serialnet', 'playSelectedMovie', 'None', episode, match[i][0] + s + match[i][1], imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    #done
    def getVideoUrl(self, url):
        videoUrl = ''
        link = self.cm.requestData(url)       
        #<iframe id="framep" class="radi" src="http://serialnet.pl/play.php?t=1-18"
        match = re.compile('<iframe id="framep" class="radi" src="(.+?)"').findall(link)
        if len(match) > 0:
            link = self.cm.requestData(match[0])    
            #log.info(link)
            #var flm = escape('http://50.7.220.66/folder/432ee8003a064ecc0eb46abfa59a044a_8555.mp4');
            match_watch = re.compile("var flm = escape\('(.+?)'\);").findall(link)
            if len(match_watch) > 0:
                videoUrl = match_watch[0]
            return videoUrl
        

    def addDir(self, service, name, category, title, link, iconimage, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(link)
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
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
