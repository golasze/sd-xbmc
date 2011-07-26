# -*- coding: utf-8 -*-
import xbmcplugin, xbmcaddon, xbmcgui, xbmc
import sys, os, stat, re
import urllib
import pLog

scriptID = sys.modules[ "__main__" ].scriptID
log = pLog.pLog()


class TVSettings:
  def __init__(self):
    addon = xbmcaddon.Addon(scriptID)
    self.log = pLog.pLog('settings')
    self.log.info('reading settings') 
    
    params = self.getParams()
    self.paramService = self.getParam(params, 'service')
    self.paramName = self.getParam(params, "name")
    self.paramTitle = self.getParam(params, "title")
    self.paramMode = self.getIntParam(params, "mode")
    self.paramCategory = self.getParam(params, "category")
    self.paramPage = self.getParam(params, "page")
    self.paramURL = self.getParam(params, "url")
    self.WeebTVLogin = addon.getSetting('weebtv_login')
    self.WeebTVPassword = addon.getSetting('weebtv_password')
    self.WeebTVEnable = addon.getSetting('weebtv_enable')
    self.MegaVideoLogin = addon.getSetting('megavideo_login')
    self.MegaVideoPassword = addon.getSetting('megavideo_password')
    self.MegaVideoEnable = addon.getSetting('megavideo_enable')
    self.MegaVideoUnlimit = addon.getSetting('megavideo_unlimit')


  def getParam(self, params, name):
    try:
      result = params[name]
      result = urllib.unquote_plus(result)
      return result
    except:
      return None

  def getIntParam (self, params, name):
    try:
      param = self.getParam(params, name)
      self.log.debug(name + ' = ' + param)
      return int(param)
    except:
      return None
    
  def getBoolParam (self, params, name):
    try:
      param = self.getParam(params,name)
      self.log.debug(name + ' = ' + param)
      return 'True' == param
    except:
      return None
    
  def getParams(self):
    param=[]
    paramstring=sys.argv[2]
    self.log.debug('raw param string: ' + paramstring)
    if len(paramstring)>=2:
      params=sys.argv[2]
      cleanedparams=params.replace('?','')
      if (params[len(params)-1]=='/'):
        params=params[0:len(params)-2]
      pairsofparams=cleanedparams.split('&')
      param={}
      for i in range(len(pairsofparams)):
        splitparams={}
        splitparams=pairsofparams[i].split('=')
        if (len(splitparams))==2:
          param[splitparams[0]]=splitparams[1]
    return param

  def showSettings(self):
    xbmcaddon.Addon(scriptID).openSettings(sys.argv[0])