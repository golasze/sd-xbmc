# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re, os
import xbmcgui, xbmc, xbmcplugin, xbmcaddon
import simplejson as json
#import elementtree.ElementTree as ET

import traceback

import pLog, settings, Parser, Navigation, pCommon, Errors

log = pLog.pLog()
HANDLE = int(sys.argv[1])

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

SERVICE = 'hbogo'
userAgent = 'Apache-HttpClient/UNAVAILABLE (java 1.4)'

webUrl = 'http://www.hbogo.pl'
plapiUrl = 'http://plapi.hbogo.eu'
configUrl = plapiUrl + '/Player26.svc/Configuration/JSON/POL/TABL'
categoryPlayer = '/Player26.svc/Category/JSON/POL/'
mediaPlayer = '/Player26.svc/Media/JSON/POL/'
emptyMediaIdPlayer = '/00000000-0000-0000-0000-000000000000/TABL'

dstpath = ptv.getSetting('default_dstpath')
dbg = ptv.getSetting('default_debug')


class Movies:
    def __init__(self):
        self.common = pCommon.common()
        self.chars = pCommon.Chars()

    def enc(self, string):
        json_ustr = json.dumps(string, ensure_ascii=False)
        return json_ustr.encode('utf-8')
    
    def dec(self, json):
        string = self.enc('u\'' + json + '\'').replace("\"", "").replace("u'", "").replace("'", "")
        return string 
        
    def getStatus(self, url):
        status = True
        query_data = { 'url': url, 'use_host': True, 'host': userAgent, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
            response = self.common.getURLRequestData(query_data)
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
        if response.strip() != 'OK':
            status = False
        if dbg == 'true':
           log.info("HBOGO - getStatus() -> response: " + str(response.strip()))
           log.info("HBOGO - getStatus() -> status: " + str(status))
        return status
        
    def hbogoAPI(self, url, method = 'get', cookie = False, return_data = True):
        use_post = False
        if method == 'post':
            use_post = True
        query_data = { 'url': url, 'use_host': True, 'host': userAgent, 'use_cookie': cookie, 'use_post': use_post, 'return_data': return_data }
        try:
            response = self.common.getURLRequestData(query_data)
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
        json_data = json.loads(response)
        return json_data

    def listCategories(self, url):
        api = self.hbogoAPI(url)
        categories = api['Categories']
        for i in range(len(categories)):
            img = self.dec(categories[i]['NormalIconUrl'])
            title = self.dec(categories[i]['Name'])
            id = self.dec(categories[i]['Id'])
            n_url = plapiUrl + categoryPlayer + id + emptyMediaIdPlayer
            if dbg == 'true':
                log.info("HBOGO - listCategories() -> title: " + str(title))
                log.info("HBOGO - listCategories() -> img link: " + img)
                log.info("HBOGO - listCategories() -> url: " + n_url)
            self.addDir(SERVICE, 'categories', title, img, '', n_url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listContent(self, url):
        api = self.hbogoAPI(url)
        items = api['Collections'][0]['MediaItems']
        for i in range(len(items)):
            desc = self.dec(items[i]['Abstract'])
            img = self.dec(items[i]['ThumbnailUrl'])
            title = self.dec(items[i]['Name'])
            id = self.dec(items[i]['Id'])
            materialId = self.dec(items[i]['MaterialId'])
            materialItemId = self.dec(items[i]['MaterialItemId'])
            origTitle = self.dec(items[i]['OriginalName'])
            content = self.dec(items[i]['ContentType'])
            n_url = plapiUrl + mediaPlayer + id + '/' + materialId + '/' + materialItemId + '/TABL'
            if dbg == 'true':
                log.info("HBOGO - listSeasons() -> title: " + str(title))
                log.info("HBOGO - listSeasons() -> img link: " + img)
                log.info("HBOGO - listSeasons() -> url: " + n_url)
                log.info("HBOGO - listSeasons() -> content: " + content)
            if content == 'Season':
                self.addDir(SERVICE, 'season', title, img, desc, n_url)
            else:
                self.addDir(SERVICE, 'movie', title, img, desc, n_url)
            #self.addDir(SERVICE, 'series', '', '', '', '')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def addDir(self, service, type, title, img, desc, link):
        liz = xbmcgui.ListItem(title, iconImage = "DefaultFolder.png", thumbnailImage = img)
        liz.setProperty("IsPlayable", "false")
        liz.setInfo(type = "Video", infoLabels={ "Title": title,
                                                "Plot": desc })
                                                #"Studio": "WEEB.TV",
                                                #"Tagline": tags,
                                                #"Aired": user } )
        u = '%s?service=%s&type=%s&title=%s&icon=%s&url=%s' % (sys.argv[0], SERVICE, type, str(title), urllib.quote_plus(img), urllib.quote_plus(link))
        xbmcplugin.addDirectoryItem(HANDLE, url = u, listitem = liz, isFolder = True)


class HBOGO:
    def __init__(self):
        self.common = pCommon.common()
        self.chars = pCommon.Chars()
        self.movie = Movies()
        self.parser = Parser.Parser()
        
    def handleService(self):
        params = self.parser.getParams()
        title = str(self.parser.getParam(params, "title"))
        type = self.parser.getParam(params, "type")
        service = self.parser.getParam(params, "service")
        image = self.parser.getParam(params, "image")
        #url = urllib.unquote_plus(self.parser.getParam(params, "url"))
        url = self.parser.getParam(params, "url")
        #content = self.parser.getParam(params, "content")
        
        if dbg == 'true':
            log.info('HBOGO - handleService()[0] -> title: ' + str(title))
            log.info('HBOGO - handleService()[0] -> type: ' + str(type))
            log.info('HBOGO - handleService()[0] -> service: ' + str(service))
            log.info('HBOGO - handleService()[0] -> image: ' + str(image))
            log.info('HBOGO - handleService()[0] -> url: ' + str(url))
            log.info('HBOGO - handleService()[0] -> content: ' + str(content))
        
        if self.movie.getStatus(webUrl + '/servicestatus.aspx'):
            if dbg == 'true':
                log.info("HBOGO - handleService()[0] -> getStatus is TRUE")
            if title == 'None':
                self.movie.listCategories(configUrl)
            elif title != 'None' and url.startswith("http://") and type == 'categories':
                self.movie.listContent(url)
            elif title != 'None' and url.startswith("http://") and type == 'seasons':
                self.movie.listMovies(url)