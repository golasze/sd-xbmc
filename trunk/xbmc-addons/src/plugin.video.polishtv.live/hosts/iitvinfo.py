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

import pLog, settings, Parser, urlparser

log = pLog.pLog()

mainUrl = 'http://iitv.info'
watchUrl = mainUrl + '/ogladaj/'
imageUrl = mainUrl + '/gfx/'

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

class iiTVInfo:
    def __init__(self):
        log.info('Loading iiTVinfo')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        
        
    def getSerialsTable(self):
        strTab = []
        outTab = []
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        
        #<li class="serial_menu no_promoted" style="display:none"><a href="/zakochana-zlosnica/">10 Things I Hate About You</a><br /><a class="sub_name" href="/zakochana-zlosnica/">Zakochana złośnica</a></li>
        #<li class="serial_menu no_promoted" style="display:none"><a href="/100-questions/">100 Questions</a></li>
        #<li class="serial_menu " style="display:block"><a href="/2-broke-girls/">2 Broke Girls</a><br /><a class="sub_name" href="/2-broke-girls/">Dwie spłukane dziewczyny</a></li>
        
        match = re.compile('<li class="serial_menu.+?" style="display:.+?"><a href="(.+?)">(.+?)</a>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                if not '<b>' in match[i][1]:
                    strTab.append(match[i][1])
                    strTab.append(match[i][0])
                    outTab.append(strTab)
                    strTab = []
        outTab.sort(key = lambda x: x[0])
        return outTab        
    
    
    def getImage(self,url):
        imageLink=imageUrl + url[1:-1] + '.jpg'     
        return imageLink
    
    
    def showSerialTitles(self):
        tab = self.getSerialsTable()
        if len(tab) > 0:
            for i in range(len(tab)):
                #log.info(tab[i][1])
                imageLink = self.getImage(tab[i][1])
                self.addDir('iitvinfo', 'serial-title', 'None', tab[i][0], tab[i][1], imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

    def showSeason(self, url):
        imageLink = self.getImage(url)
        nUrl = mainUrl + url
        #log.info(url)
        req = urllib2.Request(nUrl)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('<div class="serial_season">(.+?)</div>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                if 'Sezon' in match[i]:
                    self.addDir('iitvinfo', 'serial-season', 'None', match[i], url, imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def showSerialParts(self, url, title):
        imageLink = self.getImage(url)
        log.info("image: " + imageLink)
        nUrl = mainUrl + url
        tTab = title.split(' ')
        num = tTab[1]
        if float(num) < 10:
            num = '0' + num
        s = "s" + str(num)
        log.info("url:" + nUrl)
        log.info("season: " + s)
        req = urllib2.Request(nUrl)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()       
        match_parts = re.compile('<a href="(.+?)"><span class="release">(.+?)</span> (.+?)</a>').findall(link)
        if len(match_parts) > 0:
            for i in range(len(match_parts)):
                if s in match_parts[i][1]:
                    pTab = match_parts[i][1].split('e')
                    if (len(pTab)==2):
                        nUrl = url + match_parts[i][0]
                        self.addDir('iitvinfo', 'playSelectedMovie', 'None', match_parts[i][1] + ' - ' + match_parts[i][2], nUrl, imageLink, True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[0])
        return out


    def getVideoID(self, url):
        videoID = ''
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('<input type="hidden" name="(.+?)" value="(.+?)" />').findall(link)
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
            values = {'og_ser': og_ser, 'og_sez': og_s, 'og_e': og_e, 'og_url': og_url, 'og_coda': og_code}
            headers = { 'User-Agent' : HOST }
            data = urllib.urlencode(values)
            req = urllib2.Request(watchUrl, data, headers)
            response = urllib2.urlopen(req)
            link = response.read()
            response.close()
            #<div class="watch_link" id="l_60835"> <a href="http://video.anyfiles.pl/10+Things+I+Hate+About+You+S01E20+pl/Kino+i+TV/video/13068" target="_blank">http://video.anyfiles.pl/10+Things+I+Hate+About+You+S01E20+pl/Kino+i+TV/video/13068</a>
            #[0]link, [1]name
            match_watch = re.compile('<div class="watch_link" id=".+?"> <a href="(.+?)" target="_blank">http://(.+?)/.+?</a>').findall(link)
            if len(match_watch) > 0:
                valTab = []
                strTab = []
                a = 1
                for i in range(len(match_watch)):
                    strTab.append(str(a) + ". " + match_watch[i][1])
                    strTab.append(match_watch[i][0])
                    valTab.append(strTab)
                    strTab = []
                    a = a + 1
                log.info("lista: " + str(valTab))
                d = xbmcgui.Dialog()
                item = d.select("Wybór filmu", self.getItemTitles(valTab))
                if item != '':
                    videoID = str(valTab[item][1])
                    log.info('mID: ' + videoID)
                    return videoID
        return false
        

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
            nUrl = mainUrl + page
            linkVideo = ''
            ID = self.getVideoID(nUrl)
            if ID != '':
                #linkVideo = self.up.getHost(ID)
                linkVideo = self.up.getVideoLink(ID)
                if linkVideo != False:
                    self.LOAD_AND_PLAY_VIDEO(linkVideo)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', 'iiTV.info - tymczasowo wyczerpałeś limit ilości uruchamianych seriali.', 'Zapraszamy za godzinę.')
