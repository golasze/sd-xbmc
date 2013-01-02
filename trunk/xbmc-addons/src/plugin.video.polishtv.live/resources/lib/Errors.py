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
    [ 'No JSON object could be decoded', t(55903).encode('utf-8'), t(55904).encode('utf-8') ],
    [ '\'NoneType\' object has no attribute', t(55900).encode('utf-8'), t(55905).encode('utf-8') ],
    [ 'global name', t(55900).encode('utf-8'), t(55906).encode('utf-8') ],
    [ 'cannot concatenate', t(55900).encode('utf-8'), t(55906).encode('utf-8') ],
    [ 'expected string or buffer', t(55900).encode('utf-8'), t(55906).encode('utf-8') ],
    [ 'Expecting property name:', t(55900).encode('utf-8'), t(55906).encode('utf-8') ],
    [ 'urlopen error timed out', t(55900).encode('utf-8'), t(55907).encode('utf-8') ],
    [ '[Errno 2]', t(55900).encode('utf-8'), t(55906).encode('utf-8') ],
    [ '[Errno 10035]', t(55900).encode('utf-8'), t(55906).encode('utf-8') ],
]

class Exception:
    def __init__(self):
        pass
    
    def getError(self, error):
        title = ''
        content = ''
        d = xbmcgui.Dialog()
        if dbg == 'true':
            log.info('Errors - getError()')
        for i in range(len(ERRORS)):
            log.info('Errors - getError()[for] ' + ERRORS[i][0] + ' = ' + error)
            #if error == ERRORS[i][0]:
            #    log.info('Errors - getError()[for] ' + ERRORS[i][0] + ' = ' + error)
            #    title = ERRORS[i][1]
            #    content = ERRORS[i][2]
            #    break
            if ERRORS[i][0] in error:
                log.info('Errors - getError()[for] ' + ERRORS[i][0] + ' = ' + error)
                title = ERRORS[i][1]
                content1 = ERRORS[i][2]
                content2 = error
                break
        d.ok(title, content1, content2)                     
