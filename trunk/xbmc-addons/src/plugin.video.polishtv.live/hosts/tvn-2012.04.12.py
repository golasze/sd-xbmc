# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re
import xbmcgui, xbmc, xbmcplugin, xbmcaddon

import elementtree.ElementTree as ET
from xml.dom.minidom import parseString
from time import strftime,strptime, localtime
from datetime import date

import crypto.cipher.aes_cbc
import crypto.cipher.base
import binascii, time, os

try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.new

import pLog, settings

log = pLog.pLog()
HANDLE = int(sys.argv[1])
PAGE_LIMIT = 50

class tvn:
    mode = 0
    __settings__ = xbmcaddon.Addon(sys.modules[ "__main__" ].scriptID)
    __moduleSettings__ =  settings.TVSettings()
    contentHost = 'http://tvnplayer.pl'
    mediaHost = 'http://redir.atmcdn.pl'
    startUrl = '/api/?platform=Mobile&terminal=Android&format=xml'
    mediaMainUrl = '/scale/o2/tvn/web-content/m/'
    contentUserAgent = 'Apache-HttpClient/UNAVAILABLE (java 1.4)'
    mediaUserAgent = 'Dalvik/1.2.0 (Linux; U; Android 2.2.1; GT-I5700 Build/FRG83)'
    contentUser='atm'
    contentPass='atm_json'

    def __init__(self):
        log.info("Starting TVN Player")

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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False,totalItems=listsize)
        return ok

    def listsCategories(self):

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
        print self.contentHost+self.startUrl + urlQuery

        req = urllib2.Request(self.contentHost+self.startUrl + urlQuery)
        req.add_header('User-Agent', self.contentUserAgent)
        response = urllib2.urlopen(req)
        xmlDoc = ET.parse(response).getroot()
        categories = xmlDoc.findall(method + "/" + groupName + "/row")
        countItemNode = xmlDoc.find(method + "/count_items")
        showNextPage = False
        if ET.iselement(countItemNode):
            countItem = int(countItemNode.text)
            if countItem > PAGE_LIMIT*(1+self.page):
                showNextPage = True

        listsize = len(categories)


        seasons = xmlDoc.find(method + "/seasons")
        showSeasons = False
        if ET.iselement(seasons):
            showSeasons = True
            listsize = listsize + seasons.__len__()

        hasVideo = False

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
                print "1" #ET.dump(season)

        if showNextPage:
            self.addNextPage()
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        if hasVideo:
            xbmcplugin.setContent(int( sys.argv[ 1 ] ), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def handleService(self):

        self.name = str(self.__moduleSettings__.paramName)
        self.title = str(self.__moduleSettings__.paramTitle)
        self.category = str(self.__moduleSettings__.paramCategory)
        self.mode = str(self.__moduleSettings__.paramMode)
        self.url = str(self.__moduleSettings__.paramURL)
        self.id = str(self.__moduleSettings__.getParam(self.__moduleSettings__.getParams(), 'id'))
        self.page = self.__moduleSettings__.getParam(self.__moduleSettings__.getParams(), 'page')
        self.season = self.__moduleSettings__.getParam(self.__moduleSettings__.getParams(), 'season')
        if not self.page:
            self.page = 0
        else:
            self.page = int(self.page)

        if not self.season:
            self.season = 0
        else:
            self.season = int(self.season)

        print "name:" + self.name + ", title:" + self.title + ", category:" + self.category + ", mode:" + self.mode + ", id:" + self.id

        if self.name == 'None':
            self.listsCategories()
        elif self.name != 'None' and self.category != '':
            self.listsCategories()

    def getVideoUrl(self, category, id):
        method = 'getItem'
        groupName = 'item'
        urlQuery = '&type=%s&id=%s&limit=30&page=1&sort=newest&m=%s' % (category, id,method)
        urlQuery = urlQuery + '&deviceScreenHeight=1080&deviceScreenWidth=1920'
        #print self.contentHost+self.startUrl + urlQuery
        req = urllib2.Request(self.contentHost+self.startUrl + urlQuery)
        req.add_header('User-Agent', self.contentUserAgent)
        response = urllib2.urlopen(req)
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
            videoPlot = plot.text.encode('utf-8')

        videos = xmlDoc.findall(method + "/" + groupName + "/videos/main/video_content/row")
        videoUrls={}
        for video in videos:
            qualityName = video.find('profile_name').text
            url = video.find('url').text
            rank = 'z'
            if qualityName == 'Bardzo wysoka':
                rank = 'a'
            elif qualityName == 'Wysoka':
                rank = 'b'
            elif qualityName == 'Standard':
                rank = 'c'
            elif qualityName == 'Niska':
                rank = 'd'
            if rank != 'z':
                videoUrls[rank] = url
            else:
                print qualityName
        rankSorted =sorted(videoUrls)
        if len(rankSorted) > 0:
            videoUrl = videoUrls.get(rankSorted[0])
            videoUrl = self.generateToken(videoUrl)
            #print videoUrl
        else:
            videoUrl = ''
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
        videoPath = videoUrl[0:1+videoUrl.rfind('/')]
        sql_data = "SELECT count(*) FROM files LEFT JOIN path ON files.idPath = path.idPath WHERE path.strPath = '" + videoPath + "' AND files.playCount > 0"
        xml_data = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % urllib.quote_plus( sql_data ), )
        wasWatched = re.findall( "<field>(.*?)</field>", xml_data)[0]
        if wasWatched == "1":
            return True
        else :
            return False

    def addNextPage(self):
        page = self.page
        if not page:
            page = 0

        u = sys.argv[0]+"?mode="+self.mode+"&name="+urllib.quote_plus(self.name)+"&category="+urllib.quote_plus(self.category)+"&page="+str(page+1)+"&url="+urllib.quote_plus(self.url)+"&id="+urllib.quote_plus(self.id)
        ok=True
        image = os.path.join( self.__settings__.getAddonInfo('path'), "images/" ) + "next.png"

        liz=xbmcgui.ListItem("Następna", iconImage="DefaultFolder.png", thumbnailImage=image)
        liz.setProperty( "Folder", "true" )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

    def getIconUrl(self, node):
        thumbnails = node.findall('thumbnail/row')
        iconUrl = ''

        if len(thumbnails) > 0:
            icon = thumbnails[0].find('url').text.encode('utf-8')
            iconUrl = self.mediaHost + self.mediaMainUrl + icon + '?quality=70&dstw=290&dsth=187&type=1'

        return iconUrl