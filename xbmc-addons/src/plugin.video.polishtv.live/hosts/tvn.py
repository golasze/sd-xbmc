# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re
import xbmcgui, xbmc, xbmcplugin

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

class tvn:
    mode = 0
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

    def addDir(self,name,id,mode,category,iconimage,videoUrl='',listsize=0):
        u = sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)
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
            "Duration": str(prop['time']/60),
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
            urlQuery = '&type=%s&id=%s&limit=50&page=1&sort=newest&m=%s' % (self.category, self.id,method)

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
        listsize = len(categories)
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
                    name = name + ", odcinek " + str(episodeNode.text)

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
                videoUrl = self.getVideoUrl(type,id)

            thumbnails = category.findall('thumbnail/row')
            iconUrl = ''

            if len(thumbnails) > 0:
                icon = thumbnails[0].find('url').text.encode('utf-8')
                iconUrl = self.mediaHost + self.mediaMainUrl + icon + '?quality=70&dstw=290&dsth=187&type=1'

            self.addDir(name,id,self.mode,type,iconUrl,videoUrl,listsize)
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def handleService(self):

        self.name = str(self.__moduleSettings__.paramName)
        self.title = str(self.__moduleSettings__.paramTitle)
        self.category = str(self.__moduleSettings__.paramCategory)
        self.mode = str(self.__moduleSettings__.paramMode)
        self.url = str(self.__moduleSettings__.paramURL)
        self.id = str(self.__moduleSettings__.getParam(self.__moduleSettings__.getParams(), 'id'))
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
        print self.contentHost+self.startUrl + urlQuery
        req = urllib2.Request(self.contentHost+self.startUrl + urlQuery)
        req.add_header('User-Agent', self.contentUserAgent)
        response = urllib2.urlopen(req)
        xmlDoc = ET.parse(response).getroot()
        videos = xmlDoc.findall(method + "/" + groupName + "/videos/main/video_content/row")
        videosCount = len(videos)
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
            print videoUrl
        else:
            videoUrl = ''
        return videoUrl

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


