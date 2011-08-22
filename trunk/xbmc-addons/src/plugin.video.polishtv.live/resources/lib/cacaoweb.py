# -*- coding: utf-8 -*-
import subprocess
import string, urllib
import sys
import re
import os
import xbmcaddon

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()


class CacaoWeb:
    def __init__(self):
        log.info('Starting cacaoweb')
    
    
    def runApp(self):
        try:
            appRun = ''
            if os.uname()[0] == "Linux":
                appRun = '"' + os.getenv("HOME") + '/.xbmc/addons/plugin.video.polishtv.live/bin/cacaoweb.linux" &'
            elif os.uname()[0] == "Windows":
                appRun = '"' + os.getenv("USERPROFILE") + '\\AppData\\Roaming\\XBMC\\addons\\plugin.video.polishtv.live\\bin\\cacaoweb.exe"'
            log.info('ODPALAM: ' + appRun)
            if appRun != '':
                self.delTMPFiles()
                os.system(appRun)
        except OSError, e:
            return 1
      

    def delTMPFiles(self):
        tmpDir = ''
        if os.uname()[0] == "Linux":
            tmpDir = '"' + os.getenv("HOME") + '/.cacaoweb"'
        elif os.uname()[0] == "Windows":
            tmpDir = '"' + os.getenv("USERPROFILE") + '\\AppData\\Roaming\\cacaoweb"'
        if os.path.isdir(tmpDir):
            for fileName in os.listdir(tmpDir):
                if fileName.endswith('.cacao'):
                    os.remove(tmpDir + '/' + fileName)


    def process_num(self, process):
        return os.system('pidof %s |wc -w' % process)
    
    
    def stopApp(self):
        if os.uname()[0] == "Linux":
            os.system("killall -9 cacaoweb.linux")
        elif os.uname()[0] == "Windows":
            os.system("taskkill /F /PID cacaoweb.exe")