# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, string
import os, time
import xbmcaddon, xbmcplugin, xbmcgui, xbmc
import simplejson as json


scriptID = 'plugin.moje.polskieradio'
scriptname = "Moje Polskie Radio"
pradio = xbmcaddon.Addon(scriptID)

idKey = '20439fdf-be66-4852-9ded-1476873cfa22'
api_url = 'http://moje.polskieradio.pl/api/'
format = 'json'

channels_url = api_url + '?key=' + idKey + '&output=' + format
categories_url = api_url + 'categories/?key=' + idKey + '&output=' + format
swfUrl = 'http://moje.polskieradio.pl/_swf/player.swf'


class Parser:
    def listChannels(self):
        self.createRTMP(channels_url)
            

    def listCategories(self):
        raw_json = urllib.urlopen(categories_url)
        content_json = raw_json.read()
        result_object = json.loads(content_json)
        #xbmc.log(str(result_object))
        categoryTab = result_object["category"]
        for i in range(len(categoryTab)):
            id = categoryTab[i]["id"]
            name = categoryTab[i]["name"]
            self.addDir('categories', id, name, '')
        #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NAME)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def programyLink(self):
        self.addLink('Jedynka', 'http://moje.polskieradio.pl/_img/kanaly/pr1.jpg', 'mms://stream.polskieradio.pl/program1_wma10', '', '')
        self.addLink('Dwójka', 'http://moje.polskieradio.pl/_img/kanaly/pr2.jpg', 'mms://stream.polskieradio.pl/program2_wma10', '', '')
        self.addLink('Trójka', 'http://moje.polskieradio.pl/_img/kanaly/pr3.jpg', 'mms://stream.polskieradio.pl/program3_wma10', '', '')
        self.addLink('Czwórka', 'http://moje.polskieradio.pl/_img/kanaly/pr4.jpg', 'mms://stream.polskieradio.pl/program4_wma10', '', '')
        self.addLink('Zagranica', 'http://moje.polskieradio.pl/_img/kanaly/pr5.jpg', 'mms://stream.polskieradio.pl/program5_wma10', '', '')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
    def keyLink(self, key):
        url = channels_url + '&category=' + key
        self.createRTMP(url)


    def categoryLink(self, id):
        url = channels_url + '&subcategory=' + id
        self.createRTMP(url)


    def createRTMP(self, url):
        raw_json = urllib.urlopen(url)
        content_json = raw_json.read()
        result_object = json.loads(content_json)
        channelTab = result_object["channel"]
        for i in range(len(channelTab)):
            title = channelTab[i]["title"]
            desc = channelTab[i]["description"]
            image = channelTab[i]["image"]
            stream = channelTab[i]["streaming_uri"]
            category = channelTab[i]["category"]
            #pageUrl = channelTab[i]["link"]
            #rating = channelTab[i]["rating"]
            playPath = channelTab[i]["streaming_channel"]
            if title != '' and stream != '' and playPath != '':
                rtmpTab = stream.split(playPath)
                rtmp = rtmpTab[0]
                #rtmp += ' swfUrl=' + swfUrl
                #rtmp += ' pageUrl=' + pageUrl
                rtmp += ' playpath=' + playPath
                #rtmp += ' swfVfy=true'
                #rtmp += ' live=true'
                self.addLink(title, image, rtmp, desc, category)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        
                       
              
    def addLink(self, title, image, url, desc, category):
        u = url
        #xbmc.output(u)
        if image == '':
            thumbnailImage="DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=image)
        liz.setProperty("IsPlayable", "true")
        liz.setProperty("IsLive", "true")
        liz.setProperty('Album_Description', desc)
        liz.setInfo( type="Music", infoLabels={ 
                                               "Title": title,
                                               "Album": 'Moje Polskie Radio',
                                               "Artist": "Radio",
                                               "Genre": category,
                                               "Comment": desc } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False) 


    def addDir(self, name, id, title, icon):
        params = self.getParams()
        mode = self.getParam(params, "mode")
        u=sys.argv[0] + "?mode=" + str(mode) + "&id=" + str(id) + "&name=" + str(name)
        if icon == '':
            icon= "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        liz.setProperty("IsPlayable", "false")
        liz.setInfo( type="Music", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder=True)
            
  
    def getParam(self, params, name):
        try:
            result = params[name]
            result = urllib.unquote_plus(result)
            return result
        except:
            return None 
        
        
    def getParams(self):
        param=[]
        paramstring=sys.argv[2]
        xbmc.log('raw param string: ' + paramstring)
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param         