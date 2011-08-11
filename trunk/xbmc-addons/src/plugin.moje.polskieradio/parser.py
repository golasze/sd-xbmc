# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib
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
swfUrl = 'http://moje.polskieradio.pl/_swf/player.swf'


class Parser:
    def listChannels(self):
        raw_json = urllib.urlopen(channels_url)
        content_json = raw_json.read()
        result_object = json.loads(content_json)
        channelTab = result_object["channel"]
        for i in range(len(channelTab)):
            title = channelTab[i]["title"]
            desc = channelTab[i]["description"]
            image = channelTab[i]["image"]
            stream = channelTab[i]["streaming_uri"]
            #pageUrl = channelTab[i]["link"]
            #rating = channelTab[i]["rating"]
            playPath = channelTab[i]["streaming_channel"]
            if title != '' and stream != '' and playPath != '':
                rtmpTab = stream.split(playPath)
                rtmp = rtmpTab[0]
                rtmp += ' swfUrl=' + swfUrl
                #rtmp += ' pageUrl=' + pageUrl
                rtmp += ' playpath=' + playPath
                rtmp += ' swfVfy=true'
                rtmp += ' live=true'
                self.addLink(title, image, rtmp)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

        
               
    def addLink(self, title, image, url):
        u = url
        #xbmc.output(u)
        if image == '':
            thumbnailImage="DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=image)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Music", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False) 
            
            