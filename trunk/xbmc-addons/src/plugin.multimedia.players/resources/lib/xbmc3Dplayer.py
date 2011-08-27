# -*- coding: utf-8 -*-

#import libraries
import subprocess
import string, urllib
import sys
import re
import os, stat
import pLog, connection

__scriptID__   = sys.modules[ "__main__" ].__scriptID__
_ = sys.modules[ "__main__" ].__language__

_log = pLog.pLog()


class StereoscopicPlayer:
  def __init__(self):
    _log.info('Starting') #@UndefinedVariable
    self.conn = connection.Connection()
    
    
  def player3D(self, appMovie, formStreamInput, formStreamOutput, movie, audio, subtitle, subSize, subCode, subColor, subParallax):
    try:
      #playerFile = open(os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer', 'w')
      numAudio = str(self.getAudioLanguage(mediaTab, audio))
      numSubtitle = str(self.getSubtitleLanguage(mediaTab, subtitle))
      lircfile = os.getenv("HOME") + '/.lircrc'
      opt = ''
      lircOpt = ''
      if formStreamOutput == 'even-odd-rows':
          opt = '-S'
      if os.path.isfile(lircfile):
          lircOpt = '--lirc-config=' + lircfile
      appRun = appMovie + ' --input=' + formStreamInput + ' ' + movie + ' --output=' + formStreamOutput + ' --audio=' + numAudio + ' --subtitle=' + numSubtitle + ' --subtitle-size=' + subSize + ' --subtitle-encoding=' + subCode + ' --subtitle-color=' + subColor + ' --subtitle-parallax=' + subParallax + ' ' + lircOpt + ' -f ' + opt + '  -n'
      #playerFile.write('#!/bin/sh\n')
      #playerFile.write(appRun)
      #playerFile.close()
      #os.chmod(os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer', stat.S_IRWXU)
      _log.info('Starting command: ' + appRun)
      subprocess.call(appRun, shell=True)
    except OSError, e:
      #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
      return 1


  def player3D2files(self, appMovie, formStreamOutput, movieL, movieR, audio, subtitle, subSize, subCode, subColor, subParallax):
    try:
      #playerFile = open(os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer', 'w')
      numAudio = str(self.getAudioLanguage(mediaTab, audio))
      numSubtitle = str(self.getSubtitleLanguage(mediaTab, subtitle))
      lircfile = os.getenv("HOME") + '/.lircrc'
      lircOpt = ''
      if os.path.isfile(lircfile):
	         lircOpt = '--lirc-config=' + lircfile      
      appRun = appMovie + ' --input=separate-left-right ' + movieL + ' ' + movieR + ' --output=' + formStreamOutput + ' --audio=' + numAudio + ' --subtitle=' + numSubtitle + ' --subtitle-size=' + subSize + ' --subtitle-encoding=' + subCode + ' --subtitle-color=' + subColor + ' --subtitle-parallax=' + subParallax + ' ' + lircOpt + ' -f  -n'
      #playerFile.write('#!/bin/sh\n')
      #playerFile.write(appRun)
      #playerFile.close()
      #os.chmod(os.getenv("HOME") + '/.xbmc/addons/plugin.multimedia.players/xbmc3Dplayer', stat.S_IRWXU)
      subprocess.call(appRun, shell=True)
    except OSError, e:
      #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
      return 1


  def mediaInfo(self, appMediaInfo, movie):
    try:
      tab = []
      if movie != '':
	appRun = appMediaInfo + ' -vo null -ao null -identify -frames 0 ' + movie 
	p = subprocess.Popen(appRun, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	while True:
	  line = p.stdout.readline()
	  if line == '':
	    break
	  #if line == '' and p.poll() != None:
	  #  break
	  if 'ID_' in line:
	    tab.append(line)
	  sys.stdout.flush()
      return tab
    except OSError, e:
      #ekg.printf(subprocess.sys.stderr, "Błąd wykonania:", e)
      return 1


  def getWidth(self, table):
    width = '0'
    for line in table:
      if "ID_VIDEO_WIDTH" in line:
	a = line.split("=")
	width = a[1]
	break
    return width
	
	
  def getHeight(self, table):
    height = '0'
    for line in table:
      if "ID_VIDEO_HEIGHT" in line:
	a = line.split("=")
	height = a[1]
	break
    return height

    
    
  def isLeftEye(self, movie):
    matchEye = re.match(r'^.*([Ll][Ee][Ff][Tt]).*$', movie, re.M|re.I)
    if matchEye:
      return True
    else:
      return False
      

  def isRightEye(self, movie):
    matchEye = re.match(r'^.*([Rr][Ii][Gg][Hh][Tt]).*$', movie, re.M|re.I)
    if matchEye:
      return True
    else:
      return False
      

  def movieDir(self, movie):
    outDir = ''
    tab = movie.split('/')
    if len(tab) > 0:
      ntab = len(tab) - 1
      for i in range(ntab):
	outDir += tab[i] + '/'
    outDir = outDir.replace('"', '')
    return outDir    
	

  def getEyeName(self, eye, movie):
    out = ''
    if self.conn.isHTTPConnect(movie):
      readTab = []
      http1 = ''
      http2 = ''
      httpPath = ''
      expr = re.match(r'^\"(http://.*?)(/.*)\"$', movie, re.M|re.I)
      if expr:
	http1 = expr.group(1)
	http2 = expr.group(2)
      fTab = http2.split('/')
      if len(fTab) > 1:
	p = len(fTab) - 1
	pp = ''
	for i in range(p):
	  if i == 0:
	    pp = '/' + str(fTab[i])
	  else:
	    pp = pp + str(fTab[i]) + '/'
	httpPath = http1 + pp
      else:
	httpPath = http1
      try:
	listHTTP = urllib.urlopen(httpPath)
	readHTML = listHTTP.read()
	listHTTP.close()
	readTab = readHTML.split('\n')
      except IOError, e:
	return 1
      if eye == 'left':
	for line in readTab:
	  expr = re.match(r'^.*<a href=\"(.*?[Ll][Ee][Ff][Tt].*?)\">.*?</a>.*$', line, re.M|re.I)
	  if expr:
	    out = '"' + httpPath + expr.group(1) + '"'
      elif eye == 'right':
	for line in readTab:
	  expr = re.match(r'^.*<a href=\"(.*?[Rr][Ii][Gg][Hh][Tt].*?)\">.*?</a>.*$', line, re.M|re.I)
	  if expr:
	    out = '"' + httpPath + expr.group(1) + '"'
    else:
      listTable = os.listdir(self.movieDir(movie))
      for fname in listTable:
	expr = ''
	if eye == 'left':
	  expr = re.match(r'^.*([Ll][Ee][Ff][Tt]).*$', fname, re.M|re.I)
	elif eye == 'right':
	  expr = re.match(r'^.*([Rr][Ii][Gg][Hh][Tt]).*$', fname, re.M|re.I)
	if expr:
	  if expr.group(1) in fname:
	    out = '"' + self.movieDir(movie) + fname + '"'      
    return str(out)

      
  def isStereo(self, table):
    videos = []
    for line in table:
      if 'ID_VIDEO_ID' in line:
	videos.append(line)
    if len(videos) > 1:
      return True


  def getEyeFirst(self, table):
      inputForm = 'separate-left-right'
      eye = []
      for line in table:
          if 'ID_VID_' in line:
              eye.append(line)
              if len(eye) > 1:
                  exprL = re.match(r'^.*([Ll][Ee][Ff][Tt]).*$', str(eye[0]), re.M|re.I)
                  exprR = re.match(r'^.*([Rr][Ii][Gg][Hh][Tt]).*$', str(eye[0]), re.M|re.I)
                  if exprL:
                      inputForm = 'separate-left-right'
                  #_log.info('Set separate: left-right')
                  elif exprR:
                      inputForm = 'separate-right-left'
              else:
                  inputForm = ''
      #_log.info('Set separate: right-left')
      return inputForm	


  def getAudioLanguage(self, table, lang):
    language = 1
    numLang = []
    for line in table:
      if 'ID_AUDIO_ID' in line:
	numLang.append(line)
    for i in range(len(numLang)):
      for line in table:
	if 'ID_AID_' + str(i) + '_LANG' in line:
	  lineTab = line.split('=')
	  llang = lineTab[1].split("\n")
	  #_log.info('Language: ' + line + ', ' + llang[0] + ', ' + str(lang.find(llang[0])))
	  if lang.rfind(llang[0]) == 0:
	    #_log.info('Language2: ' + line + ', ' + lineTab[1] + '=' + lang)
	    language = i + 1
    return language
  

  def getSubtitleLanguage(self, table, lang):
    language = 0
    numLang = []
    _log.info('lang: ' + lang)
    for line in table:
      if 'ID_SUBTITLE_ID' in line:
	numLang.append(line)
    for i in range(len(numLang)):
      for line in table:
	if 'ID_SID_' + str(i) + '_LANG' in line:
	  lineTab = line.split('=')
	  llang = lineTab[1].split("\n")
	  #_log.info('Language: ' + line + ', ' + llang[0] + ', ' + str(lang.find(llang[0])))
	  if lang.rfind(llang[0]) == 0:
	    #_log.info('Language2: ' + line + ', ' + lineTab[1] + '=' + lang)
	    language = i + 1
    return language


  def getOutputFormat(self, output):
    out = ''
    if output == '2D left':
      out = 'mono-left'
    elif output == '2D right':
      out = 'mono-right'
    elif output == '2D equalizer':
      out = 'equalizer'
    elif output == '3D equalizer':
      out = 'equalizer-3d'
    elif output == '3D OpenGL':
      out = 'stereo'
    elif output == '3D Over/Under':
      out = 'top-bottom'
    elif output == '3D HALF Over/Under':
      out = 'top-bottom-half'
    elif output == '3D Side-By-Side':
      out = 'left-right'
    elif output == '3D HALF Side-By-Side':
      out = 'left-right-half'
    elif output == '3D rows':
      out = 'even-odd-rows'
    elif output == '3D columns':
      out = 'even-odd-columns'
    elif output == '3D checkerboard':
      out = 'checkerboard'
    elif output == 'Red-Cyan mono':
      out = 'red-cyan-monochrome'
    elif output == 'Red-Cyan half color':
      out = 'red-cyan-half-color'
    elif output == 'Red-Cyan color':
      out = 'red-cyan-full-color'
    elif output == 'Red-Cyan dubois':
      out = 'red-cyan-dubois'
    elif output == 'Green-Magenta mono':
      out = 'green-magenta-monochrome'
    elif output == 'Green-Magenta half color':
      out = 'green-magenta-half-color'
    elif output == 'Green-Magenta color':
      out = 'green-magenta-full-color'
    elif output == 'Green-Magenta dubois':
      out = 'green-magenta-dubois'
    elif output == 'Amber-Blue mono':
      out = 'amber-blue-monochrome'
    elif output == 'Amber-Blue half color':
      out = 'amber-blue-half-color'
    elif output == 'Amber-Blue color':
      out = 'amber-blue-full-color'
    elif output == 'Amber-Blue dubois':
      out = 'amber-blue-dubois'
    elif output == 'HDMI pack':
      out = 'hdmi-frame-pack'
    elif output == 'Red-Green mono':
      out = 'red-green-monochrome'
    elif output == 'Red-Blue mono':
      out = 'red-blue-monochrome'
    return out



  def getInputFormat(self, inn):
    out = 'mono'
    if inn == '2D mono':
      out = 'mono'
    elif inn == '3D Over/Under':
      out = 'top-bottom'
    elif inn == '3D HALF Over/Under':
      out = 'top-bottom-half'
    elif inn == '3D Side-By-Side':
      out = 'left-right'
    elif inn == '3D HALF Side-By-Side':
      out = 'left-right-half'
    elif inn == '3D rows':
      out = 'even-odd-rows'
    elif inn == '3D Dual Stream':
      out = 'separate-left-right'
 

  
  def checkFile(self, appMediaInfo, pathMovie):
    inputVideo = ''
    pathMovie = '"' + pathMovie + '"'
    #start script
    _log.info('Prepare to play 3D movie')
    

    #load information of the movie
    _log.info('Generating informations of 3D movie: ' + pathMovie)
    
    global mediaTab
    mediaTab = self.mediaInfo(appMediaInfo, pathMovie)

    #width & height for side by side & over/under
    _log.info('Checking if movie is side-by-side or over/under')
    
    if float(self.getWidth(mediaTab)) > 0 and float(self.getHeight(mediaTab)) > 0:
      dimension = float(self.getWidth(mediaTab))/float(self.getHeight(mediaTab))
      if dimension >= 3:
	inputVideo = 'left-right'
      elif dimension < 1:
	inputVideo = 'top-bottom'
      

    #2 files [left, right] for 1 3D film
    if self.isRightEye(pathMovie) or self.isLeftEye(pathMovie):
      _log.info('Prepare to display movie from 2 files')
      
      if self.isLeftEye(pathMovie):
	#_log.info('Left eye')
	left = pathMovie
	right = self.getEyeName('right', pathMovie)
	#_log.info('Right eye: ' + str(right))
	inputVideo = 'separate-files;' + left + ';' + str(right)
      elif self.isRightEye(pathMovie):
	#_log.info('Right eye')
	left = self.getEyeName('left', pathMovie)
	right = pathMovie
	inputVideo = 'separate-files;' + str(left) + ';' + right

    #mkv dualstream
    if self.isStereo(mediaTab):
      inputVideo = 'internal-files;' + self.getEyeFirst(mediaTab)

    return inputVideo



  def playStereo(self, appMovie, formVideo, pathMovie, outputVideo, audio, subtitle, subSize, subCode, subColor, subParallax):
    outputForm = self.getOutputFormat(outputVideo)
    _log.info('Output video form is: ' + outputForm)
    
    #check connection and mount smb if exist
    _log.info('Checking connection to media stream')
    
    IN = '"' + pathMovie + '"'
    
    if formVideo == 'left-right':
      self.player3D(appMovie, 'left-right', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
    elif formVideo == 'top-bottom':
      self.player3D(appMovie, 'top-bottom', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
    elif 'separate-files;' in formVideo:
      tab = formVideo.split(";")
      left = tab[1]
      right = tab[2]
      self.player3D2files(appMovie, outputForm, left, right, audio, subtitle, subSize, subCode, subColor, subParallax)
    elif 'internal-files;' in formVideo:
      tab = formVideo.split(";")
      self.player3D(appMovie, tab[1], outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)

    
    
  def playStereoUnknown(self, appMovie, pathMovie, inputVideo, outputVideo, audio, subtitle, subSize, subCode, subColor, subParallax):
    #start script
    _log.info('Prepare to play 3D movie')
    
    outputForm = self.getOutputFormat(outputVideo)
    _log.info('Output video form is: ' + outputForm)
    
    #check connection and mount smb if exist
    _log.info('Checking connection to media stream')
    
    IN = '"' + pathMovie + '"'

    if inputVideo == '2D mono':
      self.player3D(appMovie, 'mono', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
      
    if inputVideo == '3D rows':
      self.player3D(appMovie, 'even-odd-rows', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)

    #width & height for side by side & over/under
    _log.info('if movie is sbs or over/under play unknown. Input: ' + inputVideo)
    if inputVideo == '3D Side-By-Side':
      self.player3D(appMovie, 'left-right', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
    elif inputVideo == '3D Over/Under':
      self.player3D(appMovie, 'top-bottom', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
      
    #side by side & over/under halfsbs
    _log.info('if movie is half sbs or half over/under play unknown. Input: ' + inputVideo)
    
    if inputVideo == '3D HALF Side-By-Side':
      self.player3D(appMovie, 'left-right-half', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
    elif inputVideo == '3D HALF Over/Under':
      player3D(appMovie, 'top-bottom-half', outputForm, IN, audio, subtitle)

    #mkv dualstream
    _log.info('if movie is dual stream play unknown. Input: ' + inputVideo)
    if inputVideo == '3D Dual Stream':
      self.player3D(appMovie, 'separate-left-right', outputForm, IN, audio, subtitle, subSize, subCode, subColor, subParallax)
