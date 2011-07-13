# -*- coding: utf-8 -*-
import cookielib, os, string
import os, time
import urllib, urllib2, re, sys, math
import xbmcgui


BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, megavideo, cacaoweb

log = pLog.pLog()

mainUrl = 'http://www.justin.tv'


TV_TABLE = { 
1: 'TVN': 'rtmp://199.9.255.45/app swfUrl=http://www-cdn.justin.tv/widgets/live_site_player.r34305490c2b0abacd260523181fc486d496372ee.swf pageUrl=http://pl.justin.tv/akisla swfVfy=true live=true',
2: 'TVN HD': '' 
}