# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import elementtree.ElementTree as ET


scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings

log = pLog.pLog()

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

URL_IPLA = 'http://getmedia.redefine.pl'
IDENTITY = 'login=5zdl1ax9&ver=313&cuid=%2D11218210'
#IDENTITY = 'ver=162&login=common%5Fuser&cuid=%2D11033141'
#IDENTITY = { 'ver': '162', 'login': 'common%5Fuser', 'cuid': '%2D11033141' }
#LIVE = { 'passwdmd5': '', 'ver': '162', 'login': 'common_user', 'cuid': '-11033141' }

URL_CHANNELS = URL_IPLA + '/action/2.0/vod/list/'
URL_CATEGORIES = URL_IPLA + '/r/l_x_35_ipla/categories/list/?' + IDENTITY
#URL_CATEGORIES = URL_IPLA + '/r/cu_x_7_iplalight/categories/list/'
URL_LIVE = URL_IPLA + '/m/cu_pl_7_iplalight/live/reallive_channels/?passwdmd5=&' + IDENTITY
URL_MOVIE = URL_IPLA + '/action/2.0/vod/list/?' + IDENTITY + '&category='


MENU_TAB = { 1: "Na żywo;" + URL_LIVE,
            2: "Biblioteka;" + URL_CATEGORIES,
            3: "Filmy;http://getmedia.redefine.pl/r/x_x_7_iplalight/reco/viewing_media/" }


class IPLA:
    def __init__(self):
        self.settings = settings.TVSettings()              

    
    def listsMovieLive(self, url):
        elems = ET.parse(urllib.urlopen(url)).getroot()
        channels = elems.find("channels").findall("channel")
        for channel in channels:
            #log.info(channel.attrib)
            elchn = channel.attrib
            thumbnail = elchn['thumbnail_200px']
            title = elchn['title']
            #log.info(thumbnail)
            intros = channel.findall("intro")
            for intro in intros:
                links = intro.findall("srcreq")
                for link in links:
                    #log.info(link.attrib)
                    url = self.setLinkQuality(link.attrib)
                    self.addLink(title, thumbnail, url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))      


    def getMovieVODTab(self, id):
        strTab = []
        valTab = []
        outTab = []
        num = '0'
        nUrl = URL_MOVIE + id
        elems = ET.parse(urllib.urlopen(nUrl)).getroot()
        vods = elems.find("VoDs").findall("vod")
        for vod in vods:
            elv = vod.attrib
            title = elv['title']
            if 'Odcinek' in title:
                tab = title.split(' - ')
                part = tab[0]
                if len(tab) > 1:
                    part = tab[1]
                tabTitle = part.split('Odcinek ')
                if len(tabTitle) > 1:
                    num = tabTitle[1]
                    try :
                        if float(num) < 10:
                            num = '000' + num
                        elif float(num) < 100:
                            num = '00' + num
                        elif float(num) < 1000:
                            num = '0' + num
                    except:
                        num = '0'
            thumb = elv['thumbnail_big']
            desc = elv['descr']
            rating = elv['vote']
            duration = elv['dur']
            links = vod.findall("srcreq")
            for link in links:
                ell = link.attrib
                drm = ell['drmtype']
                if drm == '0':
                    format = ell['format']
                    quality = ell['quality']
                    bitrate = ell['bitrate']
                    url = ell['url']
                    strTab.append(title)
                    strTab.append(url)
                    strTab.append(thumb)
                    strTab.append(drm)
                    strTab.append(format)
                    strTab.append(quality)
                    strTab.append(bitrate)
                    if 'Odcinek' in title:
                        strTab.append(num)
                    else:
                        strTab.append(title)
                    strTab.append(desc)
                    strTab.append(duration)
                    valTab.append(strTab)
                    strTab = []
        valTab.sort(key = lambda x: x[6], reverse = True)
        seen = set()
        for i in range(len(valTab)):
            value = valTab[i]
            title = value[0]
            seen.add(title)
        for titleSeen in seen:
            for i in range(len(valTab)):
                value = valTab[i]
                title = value[0]
                if titleSeen == title:
                    outTab.append(value)
                    break     
        outTab.sort(key = lambda x: x[7])
        return outTab


    def listsMovieVOD(self, id):
        table = self.getMovieVODTab(id)
        for i in range(len(table)):
            value = table[i]
            title = value[0]
            url = value[1]
            thumb = value[2]
            desc = value[8]
            duration = value[9]
            self.addLink(title, thumb, url, desc, self.getMovieTime(duration))
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 
        

    def listsCategories(self, url):
        elems = ET.parse(urllib.urlopen(url)).getroot()
        cats = elems.findall("cat")
        for cat in cats:
               val = cat.attrib
               try:
                   pid = val['pid']
                   if pid == '0':
                       title = val['title']
                       id = val['id']
                       thumb = val['thumbnail_big']
                       self.add('ipla', id, 'main-categories', title, thumb, url, True, False)
               except:
                   pass
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   


    def listsTitles(self, url, idKey):
        elems = ET.parse(urllib.urlopen(url)).getroot()
        titles = elems.findall("cat")
        for title in titles:
               val = title.attrib 
               try:
                   pid = val['pid']
                   if pid == idKey:
                       title = val['title']
                       id = val['id']
                       thumb = val['thumbnail_big']
                       self.add('ipla', id, 'title-categories', title, thumb, url, True, False)
               except:
                   pass
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsSeasons(self, url, idKey):
        elems = ET.parse(urllib.urlopen(url)).getroot()
        seasons = elems.findall("cat")
        for season in seasons:
               val = season.attrib 
               try:
                   pid = val['pid']
                   if pid == idKey:
                       title = val['title']
                       id = val['id']
                       thumb = val['thumbnail_big']
                       self.add('ipla', id, 'movie-categories', title, thumb, url, True, False)
               except:
                   pass
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def check(self, url, idKey):
        out = 'false'
        elems = ET.parse(urllib.urlopen(url)).getroot()
        seasons = elems.findall("cat")
        for season in seasons:
               val = season.attrib 
               try:
                   pid = val['pid']
                   if pid == idKey:
                       out = 'true'
                       break
               except:
                   pass
        if out == 'true':
            return True
        elif out == 'false':
            return False
               

    def switcher(self, url, idKey):
        if self.check(url, idKey):
            self.listsSeasons(url, idKey)
        else:
            self.listsMovieVOD(idKey)

    
    def listsMenuTitle(self):
        for num, val in MENU_TAB.items():
            value = val.split(';')
            self.add('ipla', value[0], 'None', 'None', 'None', value[1], True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    

    def getMovieTime(self, seconds):
        h = '00'
        m = '00'
        s = '00'
        hour = int(int(seconds) / 3600)
        h = str(int(hour))
        if len(h) == 1:
            h = '0' + h
        minute = int((int(seconds) - int(hour * 3600)) / 60)
        m = str(minute)
        if len(m) == 1:
            m = '0' + m
        sec = int(int(seconds) - int(hour * 3600) - int(minute * 60))
        s = str(sec)
        if len(s) == 1:
            s = '0' + s
        time = h + ':' + m + ':' + s
        return time


        
    def add(self, service, name, category, title, iconimage, url, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url)
        #log.info(str(u))
        if name != 'None' and category == 'main-categories':
            name = title
        elif name != 'None' and category == 'title-categories':
            name = title
        elif name != 'None' and category == 'movie-categories':
            name = title
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)


    def addLink(self, title, iconimage, url, desc, duration):
        u= url
        #log.info(str(u))
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title,
                                               "Plot": desc,
                                               "Genre": "Film/Serial",
                                               "PlotOutline": desc,
                                               "Duration": duration } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
               
    def handleService(self):
        name = str(self.settings.paramName)
        title = str(self.settings.paramTitle)
        category = str(self.settings.paramCategory)
        url = str(self.settings.paramURL)
        name = name.replace("+", " ")
        title = title.replace("+", " ")
        category = category.replace("+", " ")
        url = url.replace("+", " ")
        #log.info('nazwa: ' + name)
        #log.info('cat: ' + category)
        #log.info('url: ' + url)
        #log.info('tytuł: ' + title)
        #if name == 'None':
        #    self.listsMenuTitle()
        
        #if name == 'Na żywo' and url != 'None':
        #    self.listsMovieLive(URL_LIVE)
        
        #if name == 'Biblioteka' and url != 'None':
        if name == 'None':
            self.listsCategories(URL_CATEGORIES)
        elif name != 'None' and url != 'None' and category == 'main-categories':
            #log.info('titles')
            self.listsTitles(url, name)
        elif name != 'None' and url != 'None' and category == 'title-categories':
            #self.listsSeasons(url, name)
            self.switcher(url, name)
        elif name != 'None' and url != 'None' and category == 'movie-categories':
            self.listsMovieVOD(name)
        
        #if name == 'Filmy' and url != 'None':
        #    self.listsMovieVOD(url)   