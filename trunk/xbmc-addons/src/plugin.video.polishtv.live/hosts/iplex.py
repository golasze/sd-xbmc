# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc


BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()

mainUrl = 'http://www.iplex.pl'


class IPLEX:
  def __init__(self):
    log.info('Starting IPLEX')
    

  #def getItems()