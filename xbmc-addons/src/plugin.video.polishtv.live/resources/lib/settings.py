# -*- coding: utf-8 -*-
import xbmcplugin, xbmcaddon, xbmcgui, xbmc
import sys, os, stat, re
import urllib
import pLog

scriptID = sys.modules[ "__main__" ].scriptID
log = pLog.pLog()


class TVSettings:
    def __init__(self):
        addon = xbmcaddon.Addon(scriptID)

    def showSettings(self):
        xbmcaddon.Addon(scriptID).openSettings(sys.argv[0])
        
    #def recStart(self):