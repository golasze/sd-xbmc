# -*- coding: utf-8 -*-
import re, os, sys
import urllib, urllib2, re, sys
import xbmcaddon

import SimpleDownloader as downl
downloader = downl.SimpleDownloader()

scriptID   = sys.modules[ "__main__" ].scriptID
t = sys.modules[ "__main__" ].language
ptv = xbmcaddon.Addon(scriptID)

INVALID_CHARS = "\\/:*?\"<>|"

CHARS = [
    [ ' ', '_' ],
    [ ',', '-' ]
]

class Downloader:
    def __init__(self):
        pass
    
    def getFile(self, opts = {}):
        print 'AAAA tutaj: ' + self.fileName(opts['title'])
        title = self.fileName(opts['title'])
        params = { 'url': opts['url'], 'download_path': opts['path'] }
        downloader.download(title, params)
        #downloader.download(self.fileName(opts['title']), params, async = False)
        
    def fileName(self, title):
        filename = "%s-[%s].mp4" % (''.join(c for c in title if c not in INVALID_CHARS), 0)
        return self.replaceString(filename)
    
    def replaceString(self, string):
        out = string
        for i in range(len(CHARS)):
            out = string.replace(CHARS[i][0], CHARS[i][1])
            string = out
        return out