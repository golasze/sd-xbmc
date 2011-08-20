# -*- coding: utf-8 -*-
import subprocess
import string, urllib
import sys
import re
import os, platform

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()


class CacaoWeb:
    def __init__(self):
        log.info('Starting cacaoweb')
    
    
    def runApp(self):
        try:
            appRun = ''
            if platform.system() == "Linux":
                appRun = '"' + os.getenv("HOME") + '/.xbmc/addons/plugin.video.polishtv.live/bin/cacaoweb.linux" &'
            elif platform.system() == "Windows":
                appRun = '"' + os.getenv("USERPROFILE") + '\\AppData\\Roaming\XBMC\\addons\\plugin.video.polishtv.live\\bin\\cacaoweb.exe"'
            if appRun != '':
                self.delTMPFiles()
                os.system(appRun)
        except OSError, e:
            return 1
      

    def delTMPFiles(self):
        tmpDir = ''
        if platform.system() == "Linux":
            tmpDir = '"' + os.getenv("HOME") + '/.cacaoweb"'
        elif platform.system() == "Windows":
            tmpDir = '"' + os.getenv("USERPROFILE") + '\\AppData\\Roaming\\cacaoweb"'
        if os.path.isdir(tmpDir):
            for fileName in os.listdir(tmpDir):
                if fileName.endswith('.cacao'):
                    os.remove(tmpDir + '/' + fileName)


    def process_num(self, process):
        return os.system('pidof %s |wc -w' % process)
    
    
    def stopApp(self):
        if platform.system() == "Linux":
            os.system("killall -9 cacaoweb.linux")
        elif platform.system() == "Windows":
            os.system("taskkill /F /PID cacaoweb.exe")