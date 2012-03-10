# -*- coding: utf-8 -*-
import xbmc, xbmcgui, subprocess, os, time, sys, urllib, re
import xbmcplugin, xbmcaddon
#import switcher

  
__scriptname__ = "Bluray and 3D players"
__scriptID__      = "plugin.multimedia.players"
__author__ = "Plesken"
__url__ = "http://systems-design.pl"
__credits__ = ""
__addon__ = xbmcaddon.Addon(__scriptID__)

__language__ = __addon__.getLocalizedString
_ = sys.modules[ "__main__" ].__language__

# Shared resources
BASE_RESOURCE_PATH = os.path.join( __addon__.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import settings, pLog, xbmc3Dplayer

_log = pLog.pLog()

_log.info('Starting Player script') #@UndefinedVariable

TAB_PREFS = {'prog': 'None',
             'mediainfo': 'None',
             'file1': 'None',
             'file2': 'None',
             'input': 'None',
             'output': 'None',
             'audio': 'None',
             'audnum': 0,
             'subtitle': 'None',
             'subnum': 0,
             'subsize': 0,
             'subenc': 'None',
             'subcolor': 'None',
             'subparallax': 0,
             'switcher': 'false',
             'switcherexp': 'false'}


class StereoscopicInit:
    def __init__(self):
        _log.info('Starting') #@UndefinedVariable
        self.settings = settings.StereoscopicSettings()
        self.player = xbmc3Dplayer.StereoscopicPlayer()
        addon = xbmcaddon.Addon(__scriptID__)
        TAB_PREFS['prog'] = addon.getSetting('player_location')
        TAB_PREFS['mediainfo'] = addon.getSetting('mediainfo_location')
        #TAB_PREFS['file1'] = '"' + xbmc.getInfoLabel("ListItem.FileNameAndPath") + '"'
        TAB_PREFS['output'] = self.player.getOutputFormat(addon.getSetting('output_video'))
        #TAB_PREFS['audio'] = self.getLang()
        #TAB_PREFS['subtitle'] = self.getLang()
        TAB_PREFS['subsize'] = addon.getSetting('subtitle_size')
        TAB_PREFS['subenc'] = addon.getSetting('subtitle_coding')
        TAB_PREFS['subcolor'] =  addon.getSetting('subtitle_color')
        TAB_PREFS['subparallax'] = addon.getSetting('subtitle_parallax')
        TAB_PREFS['switcher'] = addon.getSetting('chooser')
        TAB_PREFS['switcherexp'] = addon.getSetting('chooser_exp')


    def handleListing(self):
        mode = self.settings.paramMode
        _log.info( 'mode: ' + str(mode))
        if mode == None:
            _log.info('Showing categories')
            self.CATEGORIES()
            _log.info('Showing categories done')
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif mode == 1:
            _log.info( 'Entering Play mode')
            d = xbmcgui.Dialog()
            fileSelect = d.browse(1, 'Select folder', 'video', '.mkv|.wmv|.avi|.mp4|.mp2|.m2v|.mpv|.mpg|.ts|.m2ts|.rmvb', False, False, '')
            _log.info('Open stream: ' + fileSelect)
            if fileSelect != '':
                TAB_PREFS['file1'] = '"' + fileSelect + '"'
                self.player.playStereo(TAB_PREFS)
        elif mode == 20:
            self.settings.showSettings()
        elif mode == 2:
            self.settings.initSettings()
        elif mode == 3:
            _log.info( 'Entering Manual Play mode')
            self.play3DUnknown()
  
  
    def CATEGORIES(self):
        # Filelocation
        #if self.settings.enableFile:
        self.addDir(_(50000),1, True, False)
        #self.addDir(_(50006),3, True, False)
        #self.addDir(_(50009),4, True, False)
        #self.addDir(_(50010),5, True, False)
        #self.addDir(_(50011),6, True, False)
        self.addDir(_(50001),20, True, False)
        self.addDir(_(50002),2, True, False)                     
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def addDir(self, name, mode, autoplay, isPlayable = True):
        u=sys.argv[0] + "?mode=" + str(mode)
        _log.info(u)
        icon = "DefaultVideoPlaylists.png"
        if autoplay:
            icon= "DefaultVideo.png"
        liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
        if autoplay and isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        _log.info(name)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)
    

try:
    os.remove('/tmp/is3D')
except:
    pass

mydisplay = StereoscopicInit()
mydisplay.handleListing()
