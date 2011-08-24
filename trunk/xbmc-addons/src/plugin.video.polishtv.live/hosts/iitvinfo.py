# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, megavideo, cacaoweb, settings

log = pLog.pLog()

mainUrl = 'http://iitv.info'
watchUrl = mainUrl + '/ogladaj/'

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
MEGAVIDEO_MOVIE_URL = 'http://www.megavideo.com/v/'
STREAM_MEGALINK = 'http://127.0.0.1:4001/megavideo/megavideo.caml?videoid='
STREAM_OBBLINK = 'http://127.0.0.1:4001/videobb/videobb.caml?videoid='


class iiTVInfo:
    def __init__(self):
        self.settings = settings.TVSettings()
        
        
    def getSerialsTable(self):
        strTab = []
        outTab = []
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match_norm = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a></li>').findall(link)
        match_new = re.compile('<li> <span class="newi"><img src=".+?"></span><a href="(.+?)" title=".+?">(.+?)</a></li>').findall(link)
        if len(match_norm) > 0 or len(match_new) > 0:
            for i in range(len(match_norm)):
                if not '<b>' in match_norm[i][1]:
                    strTab.append(match_norm[i][1])
                    strTab.append(match_norm[i][0])
                    outTab.append(strTab)
                    strTab = []
            for i in range(len(match_new)):
                if not '<b>' in match_new[i][1]:
                    strTab.append(match_new[i][1])
                    strTab.append(match_new[i][0])
                    outTab.append(strTab)
                    strTab = []
        outTab.sort(key = lambda x: x[0])
        return outTab        
    
    
    def showSerialTitles(self):
        tab = self.getSerialsTable()
        if len(tab) > 0:
            for i in range(len(tab)):
                self.addDir('iitvinfo', 'serial-title', 'None', tab[i][0], tab[i][1], '', True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

    def showSeason(self, link):
        url = mainUrl + link
        #log.info(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('<h3>(.+?)</h3>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                if 'Sezon' in match[i]:
                    self.addDir('iitvinfo', 'serial-season', 'None', match[i], url, '', True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def showSerialParts(self, url, title):
        tTab = title.split(' ')
        num = tTab[1]
        if float(num) > 10:
            num = '0' + num
        #log.info(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match_parts = re.compile('&nbsp; (.+?) <a class="serlink" href="(.+?)">(.+?)</a>.+?<br />').findall(link)
        if len(match_parts) > 0:
            for i in range(len(match_parts)):
                pTab = match_parts[i][0].split('e')
                nTab = pTab[0].split('s')
                if num in nTab[1]:
                    self.addDir('iitvinfo', 'playSelectedMovie', 'None', match_parts[i][0] + ' - ' + match_parts[i][2], match_parts[i][1], '', True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[0])
        return out


    def getTabID(self, table, key):
        id = ''
        for i in range(len(table)):
            value = table[i]
            if key in value[0]:
                id = value[1]
                break
        return id


    def getID(self, opt0, opt1):
        identity = ''
        if 'megavideo.com' in opt0:
            lTab = opt1.split('v=')
            identity = lTab[1] + ':megavideo'
        elif 'videobb.com' in opt0:
            lTab = opt1.split('video/')
            identity = lTab[1] + ':videobb'
        #log.info(identity)
        return identity


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
                elif match[i][0] == 'og_s':
                    og_s = match[i][1]
                elif match[i][0] == 'og_e':
                    og_e  = match[i][1]
                elif match[i][0] == 'og_url':
                    og_url = match[i][1]
                elif match[i][0] == 'og_code':
                    og_code = match[i][1] 
            values = {'og_ser': og_ser, 'og_s': og_s, 'og_e': og_e, 'og_url': og_url, 'og_code': og_code}
            headers = { 'User-Agent' : HOST }
            data = urllib.urlencode(values)
            req = urllib2.Request(watchUrl, data, headers)
            response = urllib2.urlopen(req)
            link = response.read()
            #log.info(link)
            response.close()
            match_watch = re.compile('<div align="left" style="text-align: left; font-size: 13px;"> <b>(.+?)<a href=".+?" target="_blank">(.+?)</a></b></div>').findall(link)
            if len(match_watch) == 1:
                videoID = self.getID(match_watch[0][0], match_watch[0][1])
            elif len(match_watch) > 1:
                valTab = []
                strTab = []
                a = 1
                for i in range(len(match_watch)):
                    if 'megavideo' in match_watch[i][0] or 'videobb' in match_watch[i][0]:
                        idd = self.getID(match_watch[i][0], match_watch[i][1])
                        iddTab = idd.split(':')
                        strTab.append('Film ' + str(a) + '. link z ' + iddTab[1])
                        strTab.append(idd)
                        valTab.append(strTab)
                        strTab = []
                        a = a + 1
                #log.info(str(valTab))
                d = xbmcgui.Dialog()
                item = d.select("Wybór filmu", self.getItemTitles(valTab))
                if item != '':
                    item = item + 1
                    videoID = self.getTabID(valTab, str(item))                              
        #log.info('mID: ' + videoID)
        return videoID
        

    
    def addDir(self, service, name, category, title, link, iconimage, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(link)
        #log.info(str(u))
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
    

    #def addLink(self, title, url):
    #    u = url
    #    log.info(str(u))
    #    liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage="DefaultVideo.png")
    #    liz.setProperty("IsPlayable", "true")
    #    liz.setInfo( type="Video", infoLabels={ "Title": title } )
    #    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    

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
        name = str(self.settings.paramName)
        title = str(self.settings.paramTitle)
        category = str(self.settings.paramCategory)
        page = str(self.settings.paramPage)
        
        if name == 'None':
            self.showSerialTitles()
        elif name == 'serial-title':
            self.showSeason(page)
        elif name == 'serial-season' and title != 'None' and page != 'None':
            self.showSerialParts(page, title)
        
        if name == 'playSelectedMovie':
            linkVideo = ''
            ID = self.getVideoID(mainUrl + page)
            tabID = ID.split(':')
            if ID != '':
                if tabID[1] == 'megavideo':
                    if self.settings.MegaVideoUnlimit == 'true':
                        linkVideo = STREAM_MEGALINK + tabID[0]
                        cw = cacaoweb.CacaoWeb()
                        cw.stopApp()
                        cw.runApp()              
                    elif self.settings.MegaVideoUnlimit == 'false':
                        mega = megavideo
                        linkVideo = mega.Megavideo(MEGAVIDEO_MOVIE_URL + tabID[0])
                elif tabID[1] == 'videobb':
                    linkVideo = STREAM_OBBLINK + tabID[0]
                    cw = cacaoweb.CacaoWeb()
                    cw.stopApp()
                    cw.runApp()                     
                    
                if linkVideo.startswith('http://'):
                    self.LOAD_AND_PLAY_VIDEO(linkVideo)
                    #if tabID[1] == 'megavideo' and self.settings.MegaVideoUnlimit == 'true':
                    #    cw = cacaoweb.CacaoWeb()
                    #    cw.stopApp()
                    #if tabID[1] == 'videobb':
                    #    cw = cacaoweb.CacaoWeb()
                    #    cw.stopApp()
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku MegaVideo.', 'iiTV.info - tymczasowo wyczerpałeś limit ilości uruchamianych seriali.', 'Zapraszamy za godzinę.')