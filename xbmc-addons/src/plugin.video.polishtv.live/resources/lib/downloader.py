# -*- coding: utf-8 -*-
import re, os, sys
import urllib, urllib2, re, sys
import xbmcaddon

import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()

scriptID   = sys.modules[ "__main__" ].scriptID
t = sys.modules[ "__main__" ].language
ptv = xbmcaddon.Addon(scriptID)


class Downloader:
    def __init__(self):
        pass
    
    def getFile(self, opts = {}):
        print 'AAAA tutaj: ' + opts['url']
        params = { 'url': opts['url'], 'download_path': opts['path'] }
        downloader.download(self.fileName(opts['title']), params)
        #downloader.download(self.fileName(opts['title']), params, async = False)
        
    def fileName(self, title):
        return "%s.mp4" % (title)