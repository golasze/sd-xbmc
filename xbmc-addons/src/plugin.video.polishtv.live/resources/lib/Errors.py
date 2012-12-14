# -*- coding: utf-8 -*-
import os, string
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import pLog

scriptID   = sys.modules[ "__main__" ].scriptID
t = sys.modules[ "__main__" ].language
ptv = xbmcaddon.Addon(scriptID)

log = pLog.pLog()
dbg = ptv.getSetting('default_debug')

ERRORS = [
    [ 'HTTP Error 403: Forbidden', t(55900).encode('utf-8'), t(55901).encode('utf-8') ],
    [ 'urlopen error [Errno -2]', t(55900).encode('utf-8'), t(55902).encode('utf-8') ],
]

class Exception:
    def __init__(self):
        pass
    
    def getError(self, error):
        d = xbmcgui.Dialog()
        if dbg == 'true':
            log.info('Errors - getError()')
        for i in range(len(ERRORS)):
            log.info('Errors - getError()[for] ' + ERRORS[i][0] + ' = ' + error)
            if error == ERRORS[i][0]:
                log.info('Errors - getError()[for] ' + ERRORS[i][0] + ' = ' + error)
                d.ok(ERRORS[i][1], ERRORS[i][2])
                exit()
            elif ERRORS[i][0] in error:
                log.info('Errors - getError()[for] ' + ERRORS[i][0] + ' = ' + error)
                d.ok(ERRORS[i][1], ERRORS[i][2])
                exit()                     
