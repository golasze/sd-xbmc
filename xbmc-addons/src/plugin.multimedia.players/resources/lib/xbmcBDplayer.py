# -*- coding: utf-8 -*-
import subprocess
import string
import sys
import re
import os
import xbmc

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, connection

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


""" Old version on mplayer    
  def playerBluRay(self, appMovie, movie, audio):
    try:
      #numAudio = str(self.getAudioLanguage(mediaTab, audio))
      appRun = appMovie + ' br:// -bluray-device ' + movie
      _log.info('Starting BluRay command: ' + appRun)
      subprocess.call(appRun, shell=True)
    except OSError, e:
      #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
      return 1
      
      

  def mountISO(self, path):
    try:
      self.checkDir()
      _log.info('Check BluRay iso: ' + path)
      #if os.path.isfile('"' + path + '"'):
      _log.info('Mount BluRay iso: ' + path)
      appRun = 'sudo mount -t udf - o loop ' + path + ' /tmp/bd'
      subprocess.call(appRun, shell=True)
    except OSError, e:
      return 1



  def umountISO(self):
    try:
      appRun = 'sudo umount /tmp/bd'
      subprocess.call(appRun, shell=True)
    except OSError, e:
      return 1
      
     

  def checkDir(self):
    d = os.path.dirname('/tmp/bd')
    if not os.path.exists('/tmp/bd'):
      os.makedirs('/tmp/bd')



  def isISO(self, path):
    extensionISO = ('.iso')
    if filter(path.lower().endswith, extensionISO):
      return True
    else:
      return False
      


  def play(self, appMovie, movie, audio):
    if self.isISO(movie):
      self.mountISO(movie)
      pathMovie = '/tmp/bd'
    else:
      pathMovie = '"' + movie + '"'
      
    self.playerBluRay(appMovie, pathMovie, audio)
    
    if self.isISO(movie):
      self.umountISO()
"""