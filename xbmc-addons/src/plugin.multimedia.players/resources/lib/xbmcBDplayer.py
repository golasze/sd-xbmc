# -*- coding: utf-8 -*-
import subprocess
import string
import sys
import re
import os
import xbmc
import pLog, connection

__scriptID__   = sys.modules[ "__main__" ].__scriptID__
_ = sys.modules[ "__main__" ].__language__

_log = pLog.pLog()


class BluRay:
  def __init__(self):
    _log.info('Starting play BluRay:')
    


  def getIntBluRayDisc(self):
    xbmc.executebuiltin('XBMC.PlayMedia()')



  def getIntBluRayFile(self, movie):
    xbmc.executebuiltin('XBMC.PlayMedia("' + movie + '")')
      


  def getIntBluRayISO(self, movie):
    self.checkDir()
    self.umountISO()
    self.mountISO('"' + movie + '"')
    xbmc.executebuiltin('XBMC.PlayMedia(/tmp/bd/BDMV/index.bdmv)')



  def mountISO(self, path):
    try:
      _log.info('Check BluRay iso: ' + path)
      #if os.path.isfile('"' + path + '"'):
      _log.info('Mount BluRay iso: ' + path)
      appRun = '/usr/bin/sudo /bin/mount -t udf -o loop ' + path + ' /tmp/bd'
      subprocess.call(appRun, shell=True)
    except OSError, e:
      return 1
      

  def umountISO(self):
    try:
      appRun = '/usr/bin/sudo /bin/umount /tmp/bd'
      subprocess.call(appRun, shell=True)
    except OSError, e:
      return 1
      

  def checkDir(self):
    d = os.path.dirname('/tmp/bd')
    if not os.path.exists('/tmp/bd'):
      os.makedirs('/tmp/bd')
