# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib
import os, time
import xbmcaddon, xbmcplugin, xbmcgui
import parser

scriptID = 'plugin.moje.polskieradio'
scriptname = "Moje Polskie Radio"
pradio = xbmcaddon.Addon(scriptID)



class MyPolishRadio:
    def showListOptions(self):
        p = parser.Parser()
        p.listChannels()


init = MyPolishRadio()
init.showListOptions()