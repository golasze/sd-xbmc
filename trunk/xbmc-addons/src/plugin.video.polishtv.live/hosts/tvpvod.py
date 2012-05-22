# -*- coding: utf-8 -*-

import pLog, Parser
import xbmcplugin, xbmcgui, xbmcaddon
import os, sys, urllib, urllib2, simplejson


log = pLog.pLog()
urlCategory = 'http://www.api.v3.tvp.pl/shared/listing.php?parent_id=%d&direct=false&count=%d&page=%d&filter=android_enabled=true&dump=json'
urlVideo = 'http://www.tvp.pl/pub/stat/videofileinfo?video_id=%d&mime_type=video/mp4'
urlImage = 'http://s.v3.tvp.pl/images/%s/%s/%s/uid_%s_width_%d_gs_0.jpg'

USER_AGENT = 'Apache-HttpClient/UNAVAILABLE (java 1.4)'
VOD_ID = 6442748
PAGE_MOVIES = 15

HANDLE = int(sys.argv[1])

class tvpvod:
    mode = 0
    __settings__ = xbmcaddon.Addon(sys.modules[ "__main__" ].scriptID)

    def __init__(self):
        log.info("Starting TVP.VOD")
        self.parser = Parser.Parser()

    def handleService(self):
        params = self.parser.getParams()
        self.name = str(self.parser.getParam(params, "name"))
        self.title = str(self.parser.getParam(params, "title"))
        self.category = str(self.parser.getParam(params, "category"))
        self.url = str(self.parser.getParam(params, "url"))
        self.mode = str(self.parser.getParam(params, "mode"))
        self.page = self.parser.getParam(params, "page")
        self.action = str(self.parser.getParam(params, "action"))
        self.videoid = str(self.parser.getParam(params, "videoid"))

        if not self.page:
            self.page = 1
        else:
            self.page = int(self.page)

        if self.action == 'None':
            log.info("List VOD")
            self.listsVOD()
        elif self.action == 'play_video' and self.videoid != '':
            log.info("Play video " + self.videoid)
            self.playVideo()

    def getListJson(self,id):
        url = urlCategory % (id, PAGE_MOVIES, self.page)
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', USER_AGENT)
            response = urllib2.urlopen(req)
            result = response.read()
            result = simplejson.loads(result)
            return result

        except urllib2.HTTPError, e:
            print "HTTP error " + e.code
        except urllib2.URLError, e:
            print "URL error " + e.reason
        except:
            print "Request to TVP API failed"
            return []
    def getVideoJson(self,id):
        url = urlVideo % (id)
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', USER_AGENT)
            response = urllib2.urlopen(req)
            result = response.read()
            result = simplejson.loads(result)
            return result

        except urllib2.HTTPError, e:
            print "HTTP error " + e.code
        except urllib2.URLError, e:
            print "URL error " + e.reason
        except:
            print "Request to TVP API failed"
            return []

    def listsVOD(self):
        result = self.getListJson(VOD_ID)
        items = result['items']
        totalCount = result['total_count']
        xbmcplugin.setContent(HANDLE, 'episodes')
        for item in items:
            prop = {
                'title' : item['title_root'].encode('utf-8'),
                'TVShowTitle': self.name,
                'episode': 0,
                'description': '',
                'time': 0,
                'aired': item['release_date_dt'].encode('utf-8'),
                'overlay' : 0,

            }

            if 'duration' in item and int(item['duration']):
                prop['time'] = int(item['duration'])/60
            if 'duration_min' in item and int(item['duration_min']):
                prop['time'] = int(item['duration_min'])
            if 'description_root' in item:
                prop['description'] = item['description_root'].encode('utf-8')

            iconUrl = ''
            if 'image' in item:
                iconFile = item['image'][0]['file_name'].encode('utf-8')
                iconWidth = item['image'][0]['width']
                iconUrl = urlImage %(iconFile[0],iconFile[1],iconFile[2],iconFile[:-4],iconWidth)

            self.addVideoLink(prop,str(item['_id']),iconUrl,len(items))

        if totalCount > self.page*PAGE_MOVIES:
            self.addNextPage()

        xbmcplugin.endOfDirectory(HANDLE)

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
            "Episode" : int(prop['episode'])
        } )

        u = sys.argv[0]+"?mode="+self.mode+"&name="+urllib.quote_plus(prop['title'])+"&category="+urllib.quote_plus(self.category)+"&page="+str(self.page)+"&action=play_video&videoid="+urllib.quote_plus(url)
        print u
        ok=xbmcplugin.addDirectoryItem(handle=HANDLE,url=u,listitem=liz,isFolder=False,totalItems=listsize)
        return ok

    def addNextPage(self):
        page = self.page
        if not page:
            page = 0

        u = sys.argv[0]+"?mode="+self.mode+"&name="+urllib.quote_plus(self.name)+"&category="+urllib.quote_plus(self.category)+"&page="+str(page+1)+"&url="+urllib.quote_plus(self.url)
        ok=True
        image = os.path.join( self.__settings__.getAddonInfo('path'), "images/" ) + "next.png"

        liz=xbmcgui.ListItem("Następna", iconImage="DefaultFolder.png", thumbnailImage=image)
        liz.setProperty( "Folder", "true" )
        ok=xbmcplugin.addDirectoryItem(handle=HANDLE,url=u,listitem=liz,isFolder=True)
        return ok

    def playVideo(self):
        videoId = int(self.videoid)
        videoTitle = self.name

        videoInfo = self.getVideoJson(videoId)
        url =  videoInfo['video_url']
        liz = xbmcgui.ListItem(label=videoTitle, path=url)
        liz.setInfo(type='Video', infoLabels={ "Title": videoTitle })
        xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=True, listitem=liz)

