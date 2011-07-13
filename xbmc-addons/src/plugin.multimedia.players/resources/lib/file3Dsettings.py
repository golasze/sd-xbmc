# -*- coding: utf-8 -*-
import xbmcgui, xbmc
import sys, os, string
import pLog, xbmc3Dplayer, settings, connection

__scriptID__   = sys.modules[ "__main__" ].__scriptID__
_ = sys.modules[ "__main__" ].__language__
_log = pLog.pLog()


class File3DSettings:
  def __init__(self):
    #self.settings = settings.StereoscopicSettings()
    pass
  
  
  def browseUnknown(self):
    d = xbmcgui.Dialog()
    fileSelect = d.browse(1, 'Select folder', 'video', '.mkv|.wmv|.avi|.mp4|.mp2|.m2v|.mpv|.mpg|.ts|.m2ts|.rmvb', False, False, '')
    _log.info('Open stream: ' + fileSelect)
    #_log.info('Output FORMAT: ' + self.settings.outputVideo)
    videoInput = self.inputSettings()
    _log.info('Input FORMAT: ' + videoInput)
    self.playUnknown(videoInput, fileSelect)

  
  
  def playUnknown(self, videoInput, movie):
    Player = xbmc3Dplayer.StereoscopicPlayer()
    conn = connection.Connection()
    setting = settings.StereoscopicSettings()
    #check = Player.checkFile(self.settings.mediainfoLocation, movie)
    check = Player.checkFile(setting.mediainfoLocation, movie)
    pathMovie = conn.connection(movie)
    #Player.playStereoUnknown(self.settings.playerLocation, pathMovie, videoInput, self.settings.outputVideo, self.settings.audioLang. self.settings.subtitleLang, self.settings.subtitleSize, self.settings.subtitleCoding, self.settings.subtitleColor)
    Player.playStereoUnknown(setting.playerLocation, pathMovie, videoInput, setting.outputVideo, setting.audioLang, setting.subtitleLang, setting.subtitleSize, setting.subtitleCoding, setting.subtitleColor, setting.subtitleParallax)
    conn.exit(movie)


 
  def inputSettings(self):
    videoInput = '2D left'
    format = '2D mono|3D Over/Under|3D HALF Over/Under|3D Side-By-Side|3D HALF Side-By-Side|3D rows|3D Dual Stream'
    menu = format.split('|')
    size_menu = len(menu)
    dialog = xbmcgui.Dialog()
    choice = dialog.select(_(55020), menu)
    for i in range(size_menu):
      if choice == i:
	videoInput = menu[i]
    return videoInput

