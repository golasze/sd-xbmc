# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import elementtree.ElementTree as ET
import hashlib

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings

log = pLog.pLog()

mainUrl = 'http://www.iplex.pl'
playerUrl = mainUrl + '/player_feed/'
sort_asc = '?o=rosnaco&f=tytul'
sort_desc = '?o=malejaco&f=tytul'

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

MENU_TAB = { 1: "Kategorie", 
            2: "Szukaj" }


class IPLEX:
    def __init__(self):
        log.info('Starting IPLEX')
        self.settings = settings.TVSettings()


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('iplex', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        openURL = urllib.urlopen(mainUrl)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<li><a href="/kategorie(.+?)">(.+?)</a></li>').findall(readURL)
        if len(match) > 0:
            for i in range(len(match)):
                url = mainUrl + '/kategorie' + match[i][0]
                self.add('iplex', 'categories-menu', match[i][1], 'None', 'None', url, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsItems(self, url):
        openURL = urllib.urlopen(url)
        readURL = openURL.read()
        readURL = readURL.replace('\n', '').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').split('class="movie"')
        openURL.close()
        if len(readURL) > 0:
            for i in range(len(readURL)):
                #<a class="cover" href="/filmy/trick,3400" title="Trick"> <img src="http://static.iplex.pl/1791/media/covers/0/3400.cover.jpg" alt="Trick" /> <span class="hover sprite"></span> </a> <a class="controls login favourite sprite" href="#" title="Dodaj do zapamiętanych">Dodaj do zapamiętanych</a> <a class="controls iplexplus sprite" href="/iplexplus/" title="iplex plus">iplex plus</a> <h1><a class="title" href="/filmy/trick,3400"> Trick</a></h1> <span class="duration">czas: 96 min.</span> <div class="rating-graph {'id': 3400, 'rating': 6.8, 'readOnly': true, 'type': 'vod'}"> <input type="radio" name="rating" value="1" title="strata czasu" /> <input type="radio" name="rating" value="2" title="bardzo zły" /> <input type="radio" name="rating" value="3" title="zły" /> <input type="radio" name="rating" value="4" title="nie polecam" /> <input type="radio" name="rating" value="5" title="ok" /> <input type="radio" name="rating" value="6" title="niezły" /> <input type="radio" name="rating" value="7" title="dobry" /> <input type="radio" name="rating" value="8" title="bardzo dobry" /> <input type="radio" name="rating" value="9" title="rewelacyjny" /> <input type="radio" name="rating" value="10" title="genialny!" /></div><span class="label rating-label"></span> <span class="duration">&nbsp;</span></div><div class="details sprite">     <span class="age">15<span class="plus">+</span></span> <span class="age iplexplus-contralogo sprite"></span> <img class="frame" src="http://static.iplex.pl/1791/media/covers/0/3400.details.frame.jpg" alt="" /> <span class="title">Trick</span> <span class="time"> <span class="label">czas:</span> <span class="value">96 min.</span> </span> <span class="country"> <span class="label">Kraj:</span> <span class="value">Polska</span> </span> <span class="year"> <span class="label">Rok produkcji:</span> <span class="value">2010</span> </span> <span class="genre"> <span class="label">Tagi:</span> <span class="value"><a href="/kanaly/tylko-polskie,17">Tylko polskie</a> / <a href="/kanaly/smieszne,19">Śmieszne</a> / <a href="/kolekcje/kino-polskie,27">Kino polskie</a> / <a href="/kategorie/akcja,34">Akcja</a> / <a href="/kategorie/komedia,46">Komedia</a> / <a href="/kategorie/kryminal,47">Kryminał</a></span> </span> <span class="rating"> <span class="label">Ocena:</span> <span class="value rating-desc">6.8</span> </span> <span class="votes"> <span class="label">Liczba głosów:</span> <span class="value">75</span> </span> <span class="description"> <span class="label">Opis:</span><br /> <span class="value">Filmowa opowieść o ucieczce z więzienia dwóch inteligentów odsiadujących wysokie wyroki: Marka Kowalewskiego – utalentowanego fałszerza studolarówek oraz jego starszego współtowarzysza z celi -„Profesora” Witka. Przypadkowo zamieszani w rządowe malwersacje przestępcy postanawiają zagrać va banque, a przy okazji wyrównać rachunki z przeszłości.</span> </span> </div> </div>
                match = re.compile('<a class="cover" href="(.+?)" title=".+?"> <img src="(.+?)" alt=".+?" /> <span class="hover sprite"></span> </a>.+?<h1><a class="title" href=".+?">(.+?)</a></h1>.+?<span class="title">(.+?)</span>.+?<span class="description"> <span class="label">Opis:</span><br /> <span class="value">(.+?)</span> </span> </div> </div>').findall(readURL[i])
                if len(match) > 0:
                    for a in range(len(match)):
                        log.info('url: ' + match[a][0])
                        if 'liczba odcinków:' in readURL[i]:
                            self.add('iplex', 'season-menu', 'None', match[a][3], match[a][1], match[a][0], match[a][4], 'None', True, False)
                        else:
                            self.add('iplex', 'playSelectedMovie', 'None', match[a][3], match[a][1], match[a][0], match[a][4], 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsItemsPage(self, url):
        self.getSizeItemsPerPage(url)
        if self.getSizeAllItems(url) > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(self.getSizeAllItems(url)) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('iplex', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


    def getMovieLinkFromXML(self, url):
        urlLink = 'None'
        log.info('url: ' + playerUrl + self.getMovieID(url) + '?sessionid=' + str(hashlib.md5(url).hexdigest()) + '&chlck=hhi7ep&r=1321745471310')
        urlXml = playerUrl + self.getMovieID(url) + '?sessionid=' + str(hashlib.md5(url).hexdigest()) + '&chlck=hhi7ep&r=1321745471310'
        elems = ET.parse(urllib.urlopen(urlXml)).getroot()
        mediaItems = elems.find("Media").findall("MediaItem")
        for mediaItem in mediaItems:
            media = mediaItem.attrib
            resID = media['id']
            if resID == 'M' + self.getMovieID(url):
                fileSets = mediaItem.findall("FileSet")
                for fileSet in fileSets:
                    resFiles = fileSet.findall("File")
                    if len(resFiles) > 1:
                        strTab = []
                        valTab = []
                        iid = 0
                        for resFile in resFiles:
                            file = resFile.attrib
                            bitrate = file['rate']
                            link = file['src']
                            #log.info('bitrate: ' + bitrate + ', link: ' + link)
                            strTab.append(str(iid))
                            strTab.append("Film z bitrate: " + bitrate + " kbps")
                            strTab.append(link)
                            valTab.append(strTab)
                            strTab = []
                            iid = iid + 1
                        d = xbmcgui.Dialog()
                        item = d.select("Wybierz jakość", self.getItemTitles(valTab))
                        if item != '':
                            urlLink = self.getItemURL(valTab, str(item))
                    else:
                        file = resFiles[0].attrib
                        urlLink = file['src']              
        return urlLink


    def getSizeAllItems(self, url):
        numItems = 0
        openURL = urllib.urlopen(url)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<h2>\((.+?) filmów\)</h2>').findall(readURL)
        if len(match) == 1:
            numItems = match[0]
        return numItems
    
    
    def getSizeItemsPerPage(self, url):
        numItemsPerPage = 0
        openURL = urllib.urlopen(url)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<div class="movie-(.+?)>').findall(readURL)
        if len(match) > 0:
            numItemsPerPage = len(match)
        return numItemsPerPage        

    def getMovieID(self, url):
        id = 0
        tabID = url.split(',')
        if len(tabID) > 0:
            id = tabID[1]
        return id


    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[1])
        return out

    def getItemURL(self, table, key):
        link = ''
        for i in range(len(table)):
            value = table[i]
            if key in value[0]:
                link = value[2]
                break
        return link


    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url)
        #log.info(str(u))
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
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
            d.ok('Błąd przy przetwarzaniu.', 'Najprawdopodobniej brak wsparcia vividas w ffmpeg.')        
        return ok


    def handleService(self):
        name = str(self.settings.paramName)
        category = str(self.settings.paramCategory)
        url = self.settings.paramURL
        log.info('url: ' + str(url))
        if name == 'None':
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Kategorie':
            self.listsCategoriesMenu()
        elif name == 'main-menu' and category == "Szukaj":
            self.searchInputText()
        elif name == 'categories-menu' and category != 'None':
            self.listsItemsPage(url)
        elif name == 'items-menu':
            self.listsItems(url)
            
        if name == 'playSelectedMovie':
            #self.getMovieLinkFromXML(url)
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url))
        
  