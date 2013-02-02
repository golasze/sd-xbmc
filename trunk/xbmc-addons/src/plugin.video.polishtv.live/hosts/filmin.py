# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re, socket, os
import xbmcgui, xbmc, xbmcplugin, xbmcaddon

import elementtree.ElementTree as ET
from xml.dom.minidom import parseString

import pLog, settings, Parser

log = pLog.pLog()

PAGE_MOVIES = 12


class filmin:
