# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re
import xbmcgui, xbmc, xbmcplugin

import elementtree.ElementTree as ET
from xml.dom.minidom import parseString

import pLog, settings

log = pLog.pLog()

class tvn:
    mode = 0
    __moduleSettings__ =  settings.TVSettings()

    def __init__(self):
        log.info("Starting TVP.INFO")


    def handleService(self):
        self.name = str(self.__moduleSettings__.paramName)
        self.title = str(self.__moduleSettings__.paramTitle)
        self.category = str(self.__moduleSettings__.paramCategory)
        self.mode = str(self.__moduleSettings__.paramMode)
        self.url = str(self.__moduleSettings__.paramURL)
