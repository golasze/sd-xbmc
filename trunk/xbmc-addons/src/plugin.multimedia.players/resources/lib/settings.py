# -*- coding: utf-8 -*-
import xbmcplugin, xbmcaddon, xbmcgui, xbmc
import sys, os, stat, re
import urllib
import pLog

__scriptID__   = sys.modules[ "__main__" ].__scriptID__
_ = sys.modules[ "__main__" ].__language__
_log = pLog.pLog()


class StereoscopicSettings:
    def __init__(self):
        addon = xbmcaddon.Addon(__scriptID__)
        self.log = pLog.pLog('settings')
        self.log.info('reading settings') #@UndefinedVariable

        params = self.getParams()
        self.paramUrl = self.getParam(params, 'url')
        self.paramName = self.getParam(params, "name")
        self.paramMode = self.getIntParam(params, "mode")
        self.playerLocation = addon.getSetting('player_location')
        self.mediainfoLocation = addon.getSetting('mediainfo_location')
        self.outputVideo = addon.getSetting('output_video')
        #self.audioLang = addon.getSetting('audio_language')
        self.audioLang = self.getLang()
        #self.subtitleLang = addon.getSetting('subtitle_language')
        self.subtitleLang = self.getLang()
        self.subtitleSize = addon.getSetting('subtitle_size')
        self.subtitleCoding = addon.getSetting('subtitle_coding')
        self.subtitleColor = addon.getSetting('subtitle_color')
        self.subtitleParallax = addon.getSetting('subtitle_parallax')
        self.autoPlay = addon.getSetting('autoplay_stereo')
        self.switcher = addon.getSetting('chooser')
        self.switcherExp = addon.getSetting('chooser_exp')


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
        _log.info('params: ' + str(sys.argv[2]))
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
        xbmcaddon.Addon(__scriptID__).openSettings(sys.argv[0])
    
  
    def initSettings(self):
        try:
              if self.switcher == 'true' and self.switcherExp == 'false':
                  file1 = os.getenv("HOME") + '/.xbmc/userdata/playercorefactory.xml'
                  file2 = os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/keymap.tmp'
                  file3 = os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/remote.tmp'
                  if os.path.isfile(file1):
                      os.remove(file1)
                  if os.path.isfile(file2):
                      tmpfile = open(file2, 'r').read()
                      outtext = tmpfile.replace('%arg0%', os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/switcher.py')
                      xmlfile = open(os.getenv("HOME") + '/.xbmc/userdata/keymaps/keymap.xml', 'w')
                      xmlfile.write(outtext)
                      xmlfile.close()
                  if os.path.isfile(file3):
                      tmpfile = open(file3, 'r').read()
                      outtext = tmpfile.replace('%arg1%', 'XBMC.RunScript(' + os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/switcher.py)')
                      xmlfile = open(os.getenv("HOME") + '/.xbmc/userdata/keymaps/remote.xml', 'w')
                      xmlfile.write(outtext)
                      xmlfile.close()
                  self.message(_(50007))
              elif self.switcher == 'false' and self.switcherExp == 'true':
                  file1 = os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/playercorefactory.tmp'
                  file2 = os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/keymap.tmp'
                  file3 = os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/remote.tmp'
                  if os.path.isfile(file1):
                      tmpfile = open(file1, 'r').read()
                      outtext = tmpfile.replace('%arg0%', os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer')
                      xmlfile = open(os.getenv("HOME") + '/.xbmc/userdata/playercorefactory.xml', 'w')
                      xmlfile.write(outtext)
                      xmlfile.close()
                  if os.path.isfile(file2):
                      tmpfile = open(file2, 'r').read()
                      outtext = tmpfile.replace('%arg0%', os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/switcher.py')
                      xmlfile = open(os.getenv("HOME") + '/.xbmc/userdata/keymaps/keymap.xml', 'w')
                      xmlfile.write(outtext)
                      xmlfile.close()
                  if os.path.isfile(file3):
                      tmpfile = open(file3, 'r').read()
                      outtext = tmpfile.replace('%arg1%', 'XBMC.RunScript(' + os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/switcher.py)')
                      xmlfile = open(os.getenv("HOME") + '/.xbmc/userdata/keymaps/remote.xml', 'w')
                      xmlfile.write(outtext)
                      xmlfile.close()
                  self.message(_(50007))
              elif self.switcher == 'false' and self.switcherExp == 'false':
                  player = os.getenv("HOME") + '/.xbmc/userdata/playercorefactory.xml'
                  keymap = os.getenv("HOME") + '/.xbmc/userdata/keymaps/keymap.xml'
                  remote = os.getenv("HOME") + '/.xbmc/userdata/keymaps/remote.xml'
                  os.remove(player)
                  os.remove(keymap)
                  os.remove(remote)
                  self.message(_(50004))
              elif self.switcher == 'true' and self.switcherExp == 'true':
                  self.message(_(50008))
        except:
            pass
      
      
    def message(self, messageText):
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMC 3D Player Info", messageText)
    
    
    def getLang(self):
        lang = 'english'
        fileConf = os.getenv("HOME") + '/.xbmc/userdata/guisettings.xml'
        if os.path.isfile(fileConf):
            tmpfile = open(fileConf, 'r').read()
            tabFile = tmpfile.split('\n')
            for line in tabFile:
                expr = re.match(r'^.*?<language>(.*?)</language>.*$', line, re.M|re.I)
                if expr:
                    ll = expr.group(1)
                    lang = ll.lower()
        return lang