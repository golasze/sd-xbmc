# -*- coding: utf-8 -*-

import subprocess
import string
import sys
import re
import os
import pLog

__scriptID__   = sys.modules[ "__main__" ].__scriptID__
_ = sys.modules[ "__main__" ].__language__

_log = pLog.pLog()


class Connection:
  def __init__(self):
    _log.info('Starting connection')
    
    
  def isSMBConnect(self, path):
    line = path.replace('"', '')
    expr = re.match(r'^smb://.*$', line, re.M|re.I)
    if expr:
      return True
    else:
      return False
      

  def smbMount(self, path):
    try:
      line = path.replace('"', '')
      #expr = re.match(r'^smb://(.*):(.*)@(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)/(.*?)/(.*)$', line, re.M|re.I)
      expr1 = re.match(r'^smb://(.*?):(.*?)@(.*?)/(.*?)/(.*)$', line, re.M|re.I)
      expr2 = re.match(r'^smb://(.*?)/(.*?)/(.*)$', line, re.M|re.I)
      if expr1:
	user = expr1.group(1)
	passwd = expr1.group(2)
	host = expr1.group(3)
	share = expr1.group(4)
	path = expr1.group(5)
	appRun = 'sudo mount.cifs //' + host + '/' + share + ' /mnt -o rw,user=' + user + ',password=' + passwd + ',noperm'
	subprocess.call(appRun, shell=True)
      elif expr2:
	host = expr2.group(1)
	share = expr2.group(2)
	path = expr2.group(3)
	appRun = 'sudo mount.cifs //' + host + '/' + share + ' /mnt -o rw,noperm'
	subprocess.call(appRun, shell=True)
    except OSError, e:
      #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
      return 1



  def smbDir(self, path):
    outDir = ''
    line = path.replace('"', '')
    #expr = re.match(r'^smb://(.*):(.*)@(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)/(.*?)/(.*)$', line, re.M|re.I)
    expr1 = re.match(r'^smb://(.*?):(.*?)@(.*?)/(.*?)/(.*)$', line, re.M|re.I)
    expr2 = re.match(r'^smb://(.*?)/(.*?)/(.*)$', line, re.M|re.I)
    if expr1:
      npath = expr1.group(5)
      outDir = '/mnt/' + npath
    elif expr2:
      npath = expr2.group(3)
      outDir = '/mnt/' + npath
    return outDir
    
    

  def checkSMBPath(self, path):
    pathMovie = path
    f = open(os.getenv("HOME") + '/.xbmc/userdata/sources.xml', 'r').readlines()
    for line in f:
      expr1 = re.match(r'^.*?<path pathversion="1">smb://(.*?:.*?)@(.*?/.*?)</path>$', line, re.M|re.I)
      expr2 = re.match(r'^smb://(.*?/.*?)/(.*)$', path, re.M|re.I)
      if expr1 and expr2:
	ex = expr2.group(1) + '/'
	if expr1.group(2) == expr2.group(1):
	  pathMovie = 'smb://' + expr1.group(1) + '@' + expr1.group(2) + '/' + expr2.group(2)
	elif expr1.group(2) == ex:
	  pathMovie = 'smb://' + expr1.group(1) + '@' + expr1.group(2) + expr2.group(2)
    return pathMovie
    

  def isHTTPConnect(self, path):
    line = path.replace('"', '')
    expr = re.match(r'^http://.*$', line, re.M|re.I)
    if expr:
      return True
    else:
      return False


  def httpURL(self, path):
    out = path.replace('"', '')
    out = out.replace(' ', '%20')
    out = out.replace('[', '%5B')
    out = out.replace(']', '%5D')
    out = out.replace('@', '%40')
    out = out.replace('+', '%2B')
    return out          


  def connection(self, path):
    pathMovie = ''
    if self.isSMBConnect(path):
      listTable = os.listdir('/mnt')
      if len(listTable) > 0:
	self.smbUmount()
      link = self.checkSMBPath(path)
      self.smbMount(link)
      pathMovie = self.smbDir(link)
      _log.info('Mounted path: ' + pathMovie)
    elif self.isHTTPConnect(path):
      pathMovie = self.httpURL(path)
      _log.info('HTTP URL path: ' + pathMovie)
    else:
      pathMovie = path
    return pathMovie



  def smbUmount(self):
    try:
      appRun = 'sudo umount -lf /mnt'
      subprocess.call(appRun, shell=True)
    except OSError, e:
      #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
      return 1
      


  def exit(self, path):
    if self.isSMBConnect(path):
      self.smbUmount()
      