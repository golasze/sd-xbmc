# -*- coding: utf-8 -*-
import re, os, sys, cookielib
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID   = sys.modules[ "__main__" ].scriptID
t = sys.modules[ "__main__" ].language
ptv = xbmcaddon.Addon(scriptID)


class VideoNav:
    def __init__(self):
        pass
    
    def addVideoContextMenuItems(self, params={}):
        path = ""
        cm = []
        #cm.append((t(55800), "XBMC.RunPlugin(%s?service=%s&path=%s&action=play&url=%s&vtitle=%s)" % (sys.argv[0], params['service'], params['path'], params['url'], params['title'])))
        cm.append((t(55801), "XBMC.RunPlugin(%s?service=%s&path=%s&action=download&url=%s&vtitle=%s)" % (sys.argv[0], params['service'], params['path'], params['url'], params['title'])))
        cm.append((t(55804), "XBMC.Action(Info)",))
        return cm

class RecordNav:
    def __init__(self):
        pass
    
    def addVideoContextMenuItems(self, params={}):
        path = ""
        cm = []
        cm.append((t(55800), "XBMC.RunPlugin(%s?service=%s&path=%s&action=play&item=%s)" % (sys.argv[0], params['service'], params['path'], params['item'])))
        cm.append((t(55802), "XBMC.RunPlugin(%s?service=%s&path=%s&action=recording&url=%s)" % (sys.argv[0], params['service'], params['path'], params['item'])))
        cm.append((t(55803), "XBMC.RunPlugin(%s?service=%s&path=%s&action=timerecording&url=%s)" % (sys.argv[0], params['service'], params['path'], params['item'])))
        cm.append((t(55804), "XBMC.Action(Info)",))
        return cm          