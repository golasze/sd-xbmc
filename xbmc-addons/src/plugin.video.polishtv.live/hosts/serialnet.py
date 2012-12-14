# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar, binascii
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, pCommon

log = pLog.pLog()

SERVICE = 'serialnet'
mainUrl = 'http://serialnet.pl'
watchUrl = mainUrl + '/ogladaj/'

version = ptv.getSetting('serialnet_wersja')

class SerialNet:
    def __init__(self):
        log.info('Loading ' + SERVICE)
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.cm = pCommon.common()
               
        
    def listsABCMenu(self, table):
        for i in range(len(table)):
            self.addDir(SERVICE, 'abc-menu', table[i], table[i], '', '', '', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
    def getSerialsTable(self, letter):
        strTab = []
        outTab = []
        link = self.cm.requestData(mainUrl)
        match = re.compile('<li><a href="http://serialnet.pl/serial/(.+?)">(.+?)<').findall(link)
        if len(match) > 0:
            addItem = False
            for i in range(len(match)):
                if (ord(letter[0]) < 65) and (ord(match[i][1][0]) < 65 or ord(match[i][1][0]) > 91): addItem = True
                if (letter == match[i][1][0].upper()): addItem = True
                if (addItem):
                    strTab.append(match[i][1])
                    strTab.append('http://serialnet.pl/serial/' + match[i][0])
                    outTab.append(strTab)
                    strTab = []
                    addItem = False
        outTab.sort(key = lambda x: x[0])
        return outTab        
    

    def getInfo(self,data):
        outTab = []       
        match = re.compile('<meta property="og:image" content="(.+?)"/>').findall(data)
        if len(match) > 0: imageLink = match[0]
        else: imageLink = ''
        outTab.append(imageLink)
        d = data.replace("<br/>","").replace("\n","")
        match = re.compile('<p><fb:like href=.+?</p><strong>(.+?)</strong></p></div>').findall(d)
        if len(match) > 0: desc = match[0]
        else: desc = ''
        outTab.append(desc)
        return outTab
    

    def showSerialTitles(self, letter):
        tab = self.getSerialsTable(letter)
        if len(tab) > 0:
            for i in range(len(tab)):
                self.addDir(SERVICE, 'serial-title', 'None', tab[i][0], '', tab[i][1], '', True, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

    def showSeason(self, url):  
        link = self.cm.requestData(url)       
        info = self.getInfo(link)
        match = re.compile('<div style=".+?"><h3>(.+?)</h3></div>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                if 'Sezon' in match[i]:
                    self.addDir(SERVICE, 'serial-season', 'None', match[i], info[1], url, info[0], True, False)
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
        match = re.compile('href="(.+?)' + s + '(.+?)"><b>Odcinek:(.+?)</b>').findall(link)
        if len(match) > 0:
            for i in range(len(match)):
                oTab = match[i][2].split(':')
                if len(oTab)==2:
                    episode = 'Odcinek ' + oTab[0] + ' - ' + oTab[1]
                else:
                    episode = 'Odcinek ' + oTab[0]
                self.addDir(SERVICE, 'playSelectedMovie', 'None', episode, info[1], match[i][0] + s + match[i][1], info[0], True, False)
            #zmien view na "Media Info 2"
            xbmcplugin.setContent(int(sys.argv[1]),'tvshows')
            xbmc.executebuiltin("Container.SetViewMode(503)")    
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    def getVideoUrl(self, url):
        videoUrl = ''
        link = self.cm.requestData(url)       
        #<iframe id="framep" class="radi" src="http://serialnet.pl/play.php?t=1-18"
        match = re.compile('<iframe id="framep" class="radi" src="(.+?)"').findall(link)
        if len(match) > 0:
            nUrl = match[0]
            if version == 'false':
                d = xbmcgui.Dialog()
                item = d.select("Wybór wersji", ["Napisy","Bez lektora i napisów"])
                if item == -1: return videoUrl
                elif item == 0: nUrl = match[0] + '&wersja=napisy'
            log.info("wersja: " + nUrl)
            link = self.cm.requestData(nUrl)
            print "link: " + link
            match = re.search('eval\((.+?)\)\n',link)
            if match:
                js = 'eval(' + match.group(1) + ')'
                videoUrl = self.decodeJS(js)
                log.info("decoded link: " + videoUrl)
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
            d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')        
        return ok

    
    def handleService(self):
        params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        title = self.parser.getParam(params, "title")
        category = self.parser.getParam(params, "category")
        page = self.parser.getParam(params, "page")    
        
#       log.info ('name: ' + str(name))
#	log.info ('title: ' + str(title))
#	log.info ('category: ' + str(category))
#	log.info ('page: ' + str(page))
        
        #main menu
        if name == None:
            self.listsABCMenu(self.cm.makeABCList())
        #A-Z
        if name == 'abc-menu':
            self.showSerialTitles(category)   
        
        elif name == 'serial-title':
            self.showSeason(page)
        elif name == 'serial-season' and title != None and page != None:    
            self.showSerialParts(page, title)
        if name == 'playSelectedMovie':
            log.info('video url: ' + page)
            videoUrl = self.getVideoUrl(page)
            log.info('final link: ' + videoUrl)
            if videoUrl != '':
                self.LOAD_AND_PLAY_VIDEO(videoUrl, title)
            else:
                d = xbmcgui.Dialog()
                d.ok('Brak linku', 'SerialNet.pl - nie znaleziono linku')

           
    def int2base(self, x, base):
        digs = string.digits + string.lowercase + string.uppercase
        if x < 0: sign = -1
        elif x==0: return '0'
        else: sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(digs[x % base])
            x /= base
        if sign < 0:
            digits.append('-')
        digits.reverse()
        return ''.join(digits)


    def unpack(self, p, a, c, k, e=None, d=None):
        for i in xrange(c-1,-1,-1):
            if k[i]:
                p = re.sub('\\b'+self.int2base(i,a)+'\\b', k[i], p)
        return p


    def decodeJS(self, s):
        ret = ''
        if len(s) > 0:
            js = 'unpack' + s[s.find('}(')+1:-1]
            js = js.replace("unpack('",'''unpack("''').replace(");'",''');"''').replace("\\","/")
            js = js.replace("//","/").replace("/'","'")
            js = "self." + js

            match = re.compile("\('(.+?)'").findall(eval(js))
            if len(match) > 0:
                ret = base64.b64decode(binascii.unhexlify(match[0].replace("/x","")))
        return ret
