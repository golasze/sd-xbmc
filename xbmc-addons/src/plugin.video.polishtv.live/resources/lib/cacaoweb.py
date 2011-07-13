# -*- coding: utf-8 -*-
#megavideo, videobb
import subprocess
import string, urllib
import sys
import re
import os

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()


class CacaoWeb:
  def __init__(self):
    log.info('Starting cacaoweb')
    
    
  def runApp(self):
    try:
      appRun = os.getenv("HOME") + '/.xbmc/addons/plugin.video.polishtv.live/bin/cacaoweb.linux &'
      self.delTMPFiles()
      subprocess.call(appRun, shell=True)
    except OSError, e:
      return 1
      

  def delTMPFiles(self):
    tmpDir = os.getenv("HOME") + '/.cacaoweb'
    if os.path.isdir(tmpDir):
      for fileName in os.listdir(tmpDir):
	if fileName.endswith('.cacao'):
	  os.remove(tmpDir + '/' + fileName)