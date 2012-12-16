# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re
import xbmcgui, xbmc, xbmcplugin, xbmcaddon

import elementtree.ElementTree as ET
from xml.dom.minidom import parseString
from time import strftime,strptime, localtime
from datetime import date
import traceback

import crypto.cipher.aes_cbc
import crypto.cipher.base
import binascii, time, os

try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.new

import pLog, settings, Parser, Navigation, pCommon, Errors

log = pLog.pLog()
HANDLE = int(sys.argv[1])

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

SERVICE = 'tvn'

qualities = [
            'HD',
            'Bardzo wysoka',
            'Wysoka',
            'Standard',
            'Średnia'
            'Niska',
            'Bardzo niska',
            ]

PAGE_LIMIT = ptv.getSetting('tvn_perpage')
platform = ptv.getSetting('tvn_platform')
quality = ptv.getSetting('tvn_quality')
quality_manual = ptv.getSetting('tvn_quality_manual')
#samsung_quality = __settings__.getSetting('tvn_samsung_quality')
dstpath = ptv.getSetting('default_dstpath')
dbg = ptv.getSetting('default_debug')


class tvn:
    mode = 0
    __settings__ = xbmcaddon.Addon(sys.modules[ "__main__" ].scriptID)
    __moduleSettings__ =  settings.TVSettings()
    contentHost = 'http://tvnplayer.pl'
    mediaHost = 'http://redir.atmcdn.pl'
    authKey = 'b4bc971840de63d105b3166403aa1bea'
    startUrl = '/api/?platform=Mobile&terminal=Android&format=xml&v=2.0&authKey=' + authKey
    contentUserAgent = 'Apache-HttpClient/UNAVAILABLE (java 1.4)'
    if platform == 'Samsung TV':
        contentHost = 'https://api.tvnplayer.pl'
        authKey = 'ba786b315508f0920eca1c34d65534cd'
        startUrl = '/api/?platform=ConnectedTV&terminal=Samsung&format=xml&v=2.0&authKey=' + authKey
        contentUserAgent = 'Mozilla/5.0 (SmartHub; SMART-TV; U; Linux/SmartTV; Maple2012) AppleWebKit/534.7 (KHTML, like Gecko) SmartTV Safari/534.7'
    mediaMainUrl = '/scale/o2/tvn/web-content/m/'
    mediaUserAgent = 'Dalvik/1.2.0 (Linux; U; Android 2.2.1; GT-I5700 Build/FRG83)'
    contentUser='atm'
    contentPass='atm_json'

    def __init__(self):
        log.info("Starting TVN Player")
        self.parser = Parser.Parser()
        self.navigation = Navigation.VideoNav()
        self.common = pCommon.common()
        self.exception = Errors.Exception()
        if quality_manual == 'true':
            ptv.setSetting('tvn_quality_temp', '')
        elif quality_manual == 'false':
            ptv.setSetting('tvn_quality_temp', quality)
        

    def addDir(self,name,id,mode,category,iconimage,videoUrl='',listsize=0,season=0):
        u = sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)
        if season > 0:
            u = u + "&season=" + str(season)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if category == 'episode':
            liz.setProperty("IsPlayable", "true")
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=videoUrl,listitem=liz,isFolder=False,totalItems=listsize)
        else:
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=listsize)
        return ok

    def addVideoLink(self,prop,url,iconimage,listsize=0):
        ok=True
        if not 'description' in prop:
            prop['description'] = ''
        if not 'time' in prop:
            prop['time'] = 0
        if not 'aired' in prop:
            prop['aired'] = ''
        if not 'overlay' in prop:
            prop['overlay'] = 0
        if not 'TVShowTitle' in prop:
            prop['TVShowTitle'] = ''
        if not 'episode' in prop:
            prop['episode'] = 0
                   
        liz=xbmcgui.ListItem(prop['title'], iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={
            "Title": prop['title'],
            "Plot": prop['description'],
            "Duration": str(prop['time']),
            "Premiered": prop['aired'],
            "Overlay": prop['overlay'],
            "TVShowTitle" : prop['TVShowTitle'],
            "Episode" : prop['episode']
        } )
        
        if dstpath != "None" or not dstpath:
            cm = self.navigation.addVideoContextMenuItems({ 'service': SERVICE, 'title': urllib.quote_plus(prop['title']), 'url': urllib.quote_plus(url), 'path': os.path.join(dstpath, SERVICE) })
            liz.addContextMenuItems(cm, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False,totalItems=listsize)
        return ok

    def listsCategories(self):
        if quality_manual == 'true':
            ptv.setSetting('tvn_quality_temp', '')
        elif quality_manual == 'false':
            ptv.setSetting('tvn_quality_temp', quality)
        if self.category != 'None' and self.id != 'None':
            method = 'getItems'
            groupName = 'items'
            page = 1+self.page
            urlQuery = '&type=%s&id=%s&limit=%s&page=%s&sort=newest&m=%s' % (self.category, self.id, str(PAGE_LIMIT), str(page), method)
            if self.season > 0:
                urlQuery = urlQuery + "&season=" + str(self.season)
            
        else:
            method = 'mainInfo'
            groupName = 'categories'
            urlQuery = '&m=' + method


        if dbg == 'true':
            log.info('TVN - listCategories() -> link: ' + self.contentHost + self.startUrl + urlQuery)
        #req = urllib2.Request(self.contentHost+self.startUrl + urlQuery)
        #req.add_header('User-Agent', self.contentUserAgent)
        #response = ''
        try:
            #response = urllib2.urlopen(req)
            response = self.common.getURLRequestData({ 'url': self.contentHost + self.startUrl + urlQuery, 'use_host': True, 'host': self.contentUserAgent, 'use_cookie': False, 'use_post': False, 'return_data': False })
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
        xmlDoc = ET.parse(response).getroot()
        categories = xmlDoc.findall(method + "/" + groupName + "/row")
        countItemNode = xmlDoc.find(method + "/count_items")
        showNextPage = False
        if ET.iselement(countItemNode):
            countItem = int(countItemNode.text)
            if countItem > int(PAGE_LIMIT)*(1+self.page):
                showNextPage = True
        
        listsize = len(categories)


        seasons = xmlDoc.find(method + "/seasons")
        showSeasons = False
        if ET.iselement(seasons) and self.season == 0:
            showSeasons = True
            listsize = listsize + seasons.__len__()
            numSeasons = seasons.__len__()
        else:
            numSeasons = 0

        hasVideo = False

        if self.season<>0 or (self.season==numSeasons):
            for category in categories:
                titleNode = category.find('name')
                if not ET.iselement(titleNode):
                    titleNode = category.find('title')

                if ET.iselement(titleNode):
                    name = titleNode.text.encode('utf-8')
                else:
                    name = 'brak'

                episodeNode = category.find('episode')
                if ET.iselement(episodeNode):
                    episodeNo = episodeNode.text
                    if episodeNo:
                        if episodeNode.text != "0":
                            name = name + ", odcinek " + str(episodeNode.text)
                seasonNode = category.find('season')
                if ET.iselement(seasonNode):
                    seasonNo = seasonNode.text
                    if seasonNo:
                        if seasonNo != "0":
                            name = name + ", sezon " + str(seasonNo)

                airDateNode = category.find('start_date')
                if ET.iselement(airDateNode):
                    airDateStr = airDateNode.text
                    if airDateStr:
                        airDate = strptime(airDateStr,"%Y-%m-%d %H:%M")
                        #if airDate <
                        now = localtime()
                        if airDate > now:
                            name = name + " (planowany)"
                            #print airDate.text

                type = category.find('type').text.encode('utf-8')
                id = category.find('id').text.encode('utf-8')
                videoUrl = ''
                if type == 'episode':
                    videoProp = self.getVideoUrl(type,id)
                    videoUrl = videoProp[0]

                iconUrl = self.getIconUrl(category)
            
                if videoUrl == "":
                    self.addDir(name,id,self.mode,type,iconUrl,videoUrl,listsize)
                else:
                    prop = {
                        'title': name,
                        'TVShowTitle' : name,
                        'aired' : airDate,
                        'episode' : 0,
                        'description': videoProp[2],
                        'time': int(videoProp[1])
                        }
                    if self.watched(videoUrl):
                        prop['overlay'] = 7

                    self.addVideoLink(prop,videoUrl,iconUrl,listsize)
                    hasVideo = True


        if showSeasons:
            for season in seasons:
                iconUrl = self.getIconUrl(season)
                self.addDir(season.find('name').text,self.id,self.mode,self.category,iconUrl,"",listsize,season.find('id').text)


        if showNextPage:
            self.addNextPage()
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        if hasVideo:
            xbmcplugin.setContent(int( sys.argv[ 1 ] ), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def handleService(self):
        params = self.parser.getParams()
        self.name = str(self.parser.getParam(params, "name"))
        self.title = str(self.parser.getParam(params, "title"))
        self.category = str(self.parser.getParam(params, "category"))
        self.url = str(self.parser.getParam(params, "url"))
        self.id = str(self.parser.getParam(params, "id"))
        self.mode = str(self.parser.getParam(params, "mode"))
        self.page = self.parser.getParam(params, "page")
        self.season = self.parser.getParam(params, "season")
        self.action = self.parser.getParam(params, "action")
        self.service = self.parser.getParam(params, "service")
        self.path = self.parser.getParam(params, "path")
        self.vtitle = self.parser.getParam(params, "vtitle")
        
        if not self.page:
            self.page = 0
        else:
            self.page = int(self.page)

        print ("page: " + str(self.page))
        if not self.season:
            self.season = 0
        else:
            self.season = int(self.season)

        print "name:" + self.name + ", title:" + self.title + ", category:" + self.category + ", mode:" + self.mode + ", id:" + self.id + ", season:" + str(self.season)

        if self.name == 'None':
            self.listsCategories()
        elif self.name != 'None' and self.category != '':
            self.listsCategories()
   
        if self.service == SERVICE and self.action == 'download' and self.url != '':
            self.common.checkDir(os.path.join(dstpath, SERVICE))
            if dbg == 'true':
                log.info('TVN - handleService -> Download path: ' + self.path)
                log.info('TVN - handleService -> Title: ' + urllib.unquote_plus(self.vtitle))
                log.info('TVN - handleService -> URL: ' + urllib.unquote_plus(self.url))
            import downloader
            dwnl = downloader.Downloader()
            dwnl.getFile({ 'title': urllib.unquote_plus(self.vtitle), 'url': urllib.unquote_plus(self.url), 'path': self.path })


    def getVideoUrl(self, category, id):
        method = 'getItem'
        groupName = 'item'
        urlQuery = '&type=%s&id=%s&limit=%s&page=1&sort=newest&m=%s' % (category, id, str(PAGE_LIMIT), method)
        #urlQuery = urlQuery + '&deviceScreenHeight=1080&deviceScreenWidth=1920'
        if dbg == 'true':
            log.info('TVN - getVideoUrl() -> link: ' + self.contentHost + self.startUrl + urlQuery)
        try:
            response = self.common.getURLRequestData({ 'url': self.contentHost + self.startUrl + urlQuery, 'use_host': True, 'host': self.contentUserAgent, 'use_cookie': False, 'use_post': False, 'return_data': False })
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
        #response = urllib2.urlopen(self.contentHost + self.startUrl + urlQuery)
        xmlDoc = ET.parse(response).getroot()
        runtime = xmlDoc.find(method + "/" + groupName + "/run_time")
        videoTime = 0
        #print ET.dump(runtime)
        if ET.iselement(runtime):
            videoTimeStr = runtime.text
            if  videoTimeStr:
                videoTimeElems = videoTimeStr.split(":")
                videoTime = int(videoTimeElems[0])*60*60+int(videoTimeElems[1])*60+int(videoTimeElems[2])
        plot = xmlDoc.find(method + "/" + groupName + "/lead")
        videoPlot = ""
        if ET.iselement(plot):
            videoPlot = plot.text
            if  videoPlot:
                videoPlot = plot.text.encode('utf-8')

        videos = xmlDoc.findall(method + "/" + groupName + "/videos/main/video_content/row")
        videoUrls = []
        strTab = []
        for video in videos:
            qualityName = video.find('profile_name').text.encode('utf-8')
            url = video.find('url').text
            strTab.append(qualityName)
            strTab.append(url)
            videoUrls.append(strTab)
            strTab = []
        rankSorted = sorted(videoUrls)
        if dbg == 'true':
            log.info('TVN - getVideoUrl -> video tab: ' + str(rankSorted))
        videoUrl = ''
        if len(rankSorted) > 0:
            quality_temp = ptv.getSetting('tvn_quality_temp')
            if platform == 'Mobile (Android)':
                videoUrl = self.generateToken(self.getUrlFromTab(rankSorted, quality_temp))
            elif platform == 'Samsung TV':
                tempVideoUrl = self.getUrlFromTab(rankSorted, quality_temp)
                try:
                    videoUrl = self.common.getURLRequestData({ 'url': tempVideoUrl, 'use_host': True, 'host': self.contentUserAgent, 'use_cookie': False, 'use_post': False, 'return_data': True })
                except Exception, exception:
                    traceback.print_exc()
                    self.exception.getError(str(exception))
                    exit()
                if dbg == 'true':
                    log.info('TVN - getVideoUrl() -> temporary videoUrl: ' + tempVideoUrl)
                    log.info('TVN - getVideoUrl() -> videoUrl: ' + videoUrl)
        return [videoUrl, videoTime, videoPlot]

    def generateToken(self, url):
        url = url.replace('http://redir.atmcdn.pl/http/','')
        SecretKey = 'AB9843DSAIUDHW87Y3874Q903409QEWA'
        iv = 'ab5ef983454a21bd'
        KeyStr = '0f12f35aa0c542e45926c43a39ee2a7b38ec2f26975c00a30e1292f7e137e120e5ae9d1cfe10dd682834e3754efc1733'
        salt = sha1()
        salt.update(os.urandom(16))
        salt = salt.hexdigest()[:32]

        tvncrypt = crypto.cipher.aes_cbc.AES_CBC(SecretKey, padding=crypto.cipher.base.noPadding(), keySize=32)
        key = tvncrypt.decrypt(binascii.unhexlify(KeyStr), iv=iv)[:32]

        expire = 3600000L + long(time.time()*1000) - 946684800000L

        unencryptedToken = "name=%s&expire=%s\0" % (url, expire)

        pkcs5_pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        pkcs5_unpad = lambda s : s[0:-ord(s[-1])]

        unencryptedToken = pkcs5_pad(unencryptedToken)

        tvncrypt = crypto.cipher.aes_cbc.AES_CBC(binascii.unhexlify(key), padding=crypto.cipher.base.noPadding(), keySize=16)
        encryptedToken = tvncrypt.encrypt(unencryptedToken, iv=binascii.unhexlify(salt))
        encryptedTokenHEX = binascii.hexlify(encryptedToken).upper()

        return "http://redir.atmcdn.pl/http/%s?salt=%s&token=%s" % (url, salt, encryptedTokenHEX)

    def watched(self, videoUrl):
        wasWatched = ''
        videoPath = videoUrl[0:1+videoUrl.rfind('/')]
    #    sql_data = "SELECT count(*) FROM files LEFT JOIN path ON files.idPath = path.idPath WHERE path.strPath = '" + videoPath + "' AND files.playCount > 0"
    #    xml_data = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % urllib.quote_plus( sql_data ), )
    #    wasWatched = re.findall( "<field>(.*?)</field>", xml_data)[0]
        if wasWatched == "1":
            return True
        else :
            return False

    def addNextPage(self):
        page = self.page
        if not page:
            page = 0
        u = sys.argv[0]+"?mode="+self.mode+"&name="+urllib.quote_plus(self.name)+"&category="+urllib.quote_plus(self.category)+"&page="+str(page+1)+"&url="+urllib.quote_plus(self.url)+"&id="+urllib.quote_plus(self.id)+"&season="+urllib.quote_plus(str(self.season))
        ok=True
        image = os.path.join( self.__settings__.getAddonInfo('path'), "images/" ) + "next.png"
        print u
        liz=xbmcgui.ListItem("Następna", iconImage="DefaultFolder.png", thumbnailImage=image)
        liz.setProperty( "Folder", "true" )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


    def getIconUrl(self, node):
        thumbnails = node.findall('thumbnail/row')
        iconUrl = ''
        if len(thumbnails) > 0:
            icon = thumbnails[0].find('url').text.encode('utf-8')
            if dbg == 'true':
                log.info('TVN - getIconUrl() -> url: ' + self.mediaHost + self.mediaMainUrl + icon + '?quality=70&dstw=290&dsth=187&type=1')
            iconUrl = self.mediaHost + self.mediaMainUrl + icon + '?quality=70&dstw=290&dsth=187&type=1'
        return iconUrl
    
    
    def getUrlFromTab(self, tab, key):
        out = ''  
        for key in qualities if key == 'Maksymalna' else [key]:
            for i in range(len(tab)):
                k = tab[i][0]
                v = tab[i][1]
                if key == k:
                    out = v
                    break
            if out != '':
                break      
        if out == '':
            tabmenu = []
            for i in range(len(tab)):
                tabmenu.append(tab[i][0])
            menu = xbmcgui.Dialog()
            item = menu.select("Wybór jakości", tabmenu)
            #print 'item: ' + str(tabmenu[item])
            nkey = ''
            for i in range(len(tabmenu)):
                if i == item:
                    nkey = tabmenu[i]
                    ptv.setSetting('tvn_quality_temp', str(tabmenu[i]))
                    break
            for i in range(len(tab)):
                k = tab[i][0]
                v = tab[i][1]
                if nkey == k:
                    out = v
                    break
        return out

        