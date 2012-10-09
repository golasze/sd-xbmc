# -*- coding: utf-8 -*-
import re, os, sys, cookielib
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID   = sys.modules[ "__main__" ].scriptID
t = sys.modules[ "__main__" ].language
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser

log = pLog.pLog()

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
mainUrl = "http://www.wlacz.tv"
mainChannels = mainUrl + "/kanaly"

COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "wlacztv.cookie" 

login = ptv.getSetting('wlacztv_login')
password = ptv.getSetting('wlacztv_pass')

cj = cookielib.LWPCookieJar()

class WlaczTV:
    def __init__(self):
        log.info("Loading wlacz.tv")
        self.parser = Parser.Parser()
        
    def requestData(self, url):
        if os.path.isfile(COOKIEFILE):
            cj.load(COOKIEFILE)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        data = response.read()
        response.close()    
        return data
    
    def checkDirCookie(self):
        if not os.path.isdir(ptv.getAddonInfo('path') + os.path.sep + "cookies"):
            os.mkdir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    
    def requestLoginData(self):
        if login == "" and password == "":
            d = xbmcgui.Dialog()
            d.ok(t(55603).encode("utf-8"), t(55604).encode("utf-8"), t(55605).encode("utf-8"))
            exit()
        else:
            url = mainUrl + "/user/login"
            headers = { 'User-Agent' : HOST }
            post = { 'email': login, 'password': password }
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            data = urllib.urlencode(post)
            req = urllib2.Request(url, data, headers)
            response = opener.open(req)
            link = response.read()
            response.close()
            self.checkDirCookie()
            cj.save(COOKIEFILE)
    
    def channelsList(self, url):
    	req = self.requestData(url)
    	match_icon = re.compile("<a href=\"/kanal/(.+?)\"><img src=\"(.+?)\" alt=\"\" /></a>").findall(req)
    	match = re.compile("<h5><i class=\"icon-picture\"></i> <a href=\"(.+?)\">(.+?)</a></a></h5>").findall(req)
    	if len(match) > 0 and len(match_icon) > 0:
    		for i in range(len(match)):
    			self.addChannel('wlacztv', match[i][1], mainUrl + match[i][0], mainUrl + match_icon[i][1])
    	  	xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def getChannelRTMPLink(self, url):
        req = self.requestData(url)
        match = re.compile("<param name=\"flashvars\" value=\"src=(.+?)&poster=(.+?)&streamType=live&autoPlay=true\"></param>").findall(req)
        if len(match) > 0:
            raw_rtmp_tab = match[0][0].split("?")
            split_rtmp_tab = raw_rtmp_tab[0].split("/")
            rtmp = raw_rtmp_tab[0]
            if split_rtmp_tab[len(split_rtmp_tab) - 1].endswith(".stream"):
                rtmp += " app=live?" + raw_rtmp_tab[1]
                rtmp += " pageUrl=" + url
                rtmp += " tcUrl=rtmp://" + split_rtmp_tab[len(split_rtmp_tab) - 3] + ":1935/live?" + raw_rtmp_tab[1]
                rtmp += " playpath=" + split_rtmp_tab[len(split_rtmp_tab) - 1]
            else:
                rtmp += " app=wlacztv?" + raw_rtmp_tab[1]
                rtmp += " pageUrl=" + url
                rtmp += " tcUrl=rtmp://" + split_rtmp_tab[len(split_rtmp_tab) - 3] + ":1935/live?" + raw_rtmp_tab[1]
                rtmp += " playpath=" + split_rtmp_tab[len(split_rtmp_tab) - 1] + "?" + raw_rtmp_tab[1]
            rtmp += " live=true"
            log.info("rtmp link: " + rtmp)
            return rtmp
    
    def addChannel(self, service, title, url, icon):
        u = "%s?service=%s&title=%s&url=%s&icon=%s" % (sys.argv[0], service, title, urllib.quote_plus(url), urllib.quote_plus(icon))
        liz = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage = icon)
        liz.setInfo(type="Video", infoLabels={ "Title": title, })
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
        

    def LOAD_AND_PLAY_VIDEO(self, videoUrl):
        ok=True
        if videoUrl == '':
            d = xbmcgui.Dialog()
            d.ok(t(55606).encode("utf-8"), t(55607).encode("utf-8"))
            return False
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl)
        except:
            d = xbmcgui.Dialog()
            d.ok(t(55608).encode("utf-8"), t(55609).encode("utf-8"))        
        return ok
		
    def handleService(self):
        params = self.parser.getParams()
        title = str(self.parser.getParam(params, "title"))
        url = str(self.parser.getParam(params, "url"))
        #log.info('title: ' + title)
        #log.info('url: ' + url)
        if title == 'None':
	 		self.requestLoginData()
	 		self.channelsList(mainChannels)
        elif title != '' and url != '':
            self.LOAD_AND_PLAY_VIDEO(self.getChannelRTMPLink(url))




