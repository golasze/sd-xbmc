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

import settings, pLog, xbmc3Dplayer, xbmcBDplayer, file3Dsettings, connection

_log = pLog.pLog()

_log.info('Starting Player script') #@UndefinedVariable


class StereoscopicInit:
  def __init__(self):
    _log.info('Starting') #@UndefinedVariable
    self.settings = settings.StereoscopicSettings()


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
        _log.info('Output FORMAT: ' + self.settings.outputVideo)
        mystarter = StereoscopicInit()
        mystarter.play3DMovie(self.settings.playerLocation, self.settings.mediainfoLocation, fileSelect, self.settings.outputVideo, self.settings.audioLang, self.settings.subtitleLang, self.settings.subtitleSize, self.settings.subtitleCoding, self.settings.subtitleColor, self.settings.subtitleParallax)
    elif mode == 20:
      self.settings.showSettings()
    elif mode == 2:
      self.settings.initSettings()
    elif mode == 3:
      _log.info( 'Entering Manual Play mode')
      self.play3DUnknown()
    elif mode == 4:
      self.playBluray(self.settings.blurayPlayer, mode)
    elif mode == 5:
      d = xbmcgui.Dialog()
      fileSelect = d.browse(1, 'Select folder', 'video', '.iso|.cue|.cdi|.mds|.ccd', False, False, '')
      self.playBluray(self.settings.blurayPlayer, mode, fileSelect)
    elif mode == 6:
      d = xbmcgui.Dialog()
      fileSelect = d.browse(1, 'Select folder', 'video', 'index.bdmv|.ifo', False, False, '')
      if "index.bdmv" in fileSelect:
	#fileSelect = fileSelect[:-15]
	self.playBluray(self.settings.blurayPlayer, mode, fileSelect)
      elif "video_ts.ifo" in fileSelect.lower():
	#fileSelect = fileSelect[:-12]
	_log.info('path dvd: ' + fileSelect)
	self.playBluray(self.settings.blurayPlayer, mode, fileSelect)



  def play3DMovie(self, appMovie, appMediaInfo, fileLocation, outVideoFormat, audio, subtitle, subSize, subCode, subColor, subParallax):
      try:
          if fileLocation != '':
              is3DFile = open('/tmp/is3D', 'w')
              is3DFile.write('true')
              is3DFile.close()
              xbmcPlayer = xbmc.Player()
              Player = xbmc3Dplayer.StereoscopicPlayer()
              conn = connection.Connection()
              pathMovie = conn.connection(fileLocation)
              check = Player.checkFile(appMediaInfo, pathMovie)
              _log.info('Input video: ' + check)
              if check == '':
                  Set = file3Dsettings.File3DSettings()
                  videoInput = Set.inputSettings()
                  if videoInput != '':
                      Set.playUnknown(videoInput, pathMovie)
              else:
                  Player.playStereo(appMovie, check, pathMovie, outVideoFormat, audio, subtitle, subSize, subCode, subColor, subParallax)
                  xbmcPlayer.play(pathMovie)
                  conn.exit(fileLocation)
              try:
                  os.remove('/tmp/is3D')
              except:
                  pass
      except IOError:
          pass
       
  
  
  def play3DUnknown(self):
      is3DFile = open('/tmp/is3D', 'w')
      is3DFile.write('true')
      is3DFile.close()
      Set = file3Dsettings.File3DSettings()
      Set.browseUnknown()
      try:
          os.remove('/tmp/is3D')
      except:
          pass
  
  
  
  def playBDiso(self, appMovie, fileLocation, audio):
    if fileLocation != '':
      bd = xbmcBDplayer.BluRay()
      conn = connection.Connection()
      pathMovie = conn.connection(fileLocation)
      bd.play(appMovie, pathMovie, audio)
      #conn.exit(fileLocation)    
  
  
  
  def playBluray(self, appMovie, mode, fileLocation = 'None'):
    _log.info('Prepare to play bluray')
    bd = xbmcBDplayer.BluRay()
    conn = connection.Connection()
    if mode == 4:
      bd.getIntBluRayDisc()
    elif mode == 5:
      pathMovie = conn.connection(fileLocation)
      bd.getIntBluRayFile(pathMovie)
    elif mode == 6:
      pathMovie = conn.connection(fileLocation)
      bd.getIntBluRayISO(pathMovie)

  
  
  def CATEGORIES(self):
    # Filelocation
    #if self.settings.enableFile:
    self.addDir(_(50000),1, True, False)
    self.addDir(_(50006),3, True, False)
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
