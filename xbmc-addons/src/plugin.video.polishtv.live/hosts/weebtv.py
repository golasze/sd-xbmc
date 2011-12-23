# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys
import xbmcgui, xbmcplugin, xbmcaddon, xbmc
import elementtree.ElementTree as ET
#from rtmpy.services import Application, NetConnection

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
#sys.path.append( os.path.join( os.getcwd(), "../" ) )

import pLog, settings

log = pLog.pLog()

mainUrl = 'http://weeb.tv'
playerUrl = mainUrl + '/setplayer'
HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

#IMAGE_TAB = {'TVP1': '1.png',
#             'TVP2': '2.png',
#             'TVN': 'tvn.png',
#             'TVN24': '24.png',
#             'TVN Turbo': 'tvnturbo.png',
#             'Canal+ HD': 'canal.png',
#             'Canal+ Film HD': 'cfilm.png',
#             '4fun.tv': '4fun.png',
#             'Cartoon Network': 'cn.png',
#             'EskaTV': 'eska.png',
#             'HBO HD': 'hbo.png',
#             'HBO 2 HD': 'hbo2.png',
#             'MTV': 'mtv.png',
#             'nFilm HD': 'nfilm.png',
#             'nSport HD': 'nsport.png',
#             'Discovery Science': 'science.png',
#             'VIVA POLSKA': 'viva.png'}

EXTRA_CHANNELS = [	
			['http://weeb.tv/channel/jedynka','TVP1','http://weeb.tv/static/ci/13.jpg', 'TVP1'],
			['http://weeb.tv/channel/dwójka', 'TVP2', 'http://weeb.tv/static/ci/6.jpg', 'TVP2'],
			['http://weeb.tv/channel/tvpolskahd', 'TVP HD', 'http://weeb.tv/static/ci/73.jpg', 'TVP HD'],
			['http://weeb.tv/channel/hbo-HBO', 'HBO HD', 'http://weeb.tv/static/ci/53.jpg', 'HBO HD'],
			['http://weeb.tv/channel/hbo-HBO2', 'HBO2 HD', 'http://weeb.tv/static/ci/56.jpg', 'HBO 2 HD'],
			['http://weeb.tv/channel/hbo-HBOCOMEDY', 'HBO Comedy HD', 'http://weeb.tv/static/ci/71.jpg', 'HBO Comedy HD'],
			['http://weeb.tv/channel/hbo-CINEMAX', 'Cinemax HD', 'http://weeb.tv/static/ci/58.jpg', 'Cinemax HD']
]

class WeebTV:
  def __init__(self):
    log.info('Loading WeebTV')
    self.settings = settings.TVSettings()


  def getImage(self, tvname):
      image = ''
      for name, img in IMAGE_TAB.items():
          if name.lower() == tvname.lower():
              image = os.path.join( ptv.getAddonInfo('path'), "images/" ) + img
      return image
  

  def getChannels(self):
      outTab = EXTRA_CHANNELS
      strTab = []
      urlChans = mainUrl + '/channels'
      openURL = urllib.urlopen(urlChans)
      readURL = openURL.read()
      openURL.close()
      match_opt = re.compile('<p style="font-size:14px;.+>(.*?)</a></p>(.*\n){6}.*<a href="(.*?)" title="(.*?)"><img src="(.*)" alt=".*?" height="100" width="100" /></a>').findall(readURL)
      if len(match_opt) > 0:
          for i in range(len(match_opt)):
              link = match_opt[i][2]
              title = match_opt[i][0]
              image = match_opt[i][4]
              desc = match_opt[i][3]
              #log.info(link + ', ' + image + ', ' + title)
              strTab.append(link)
              strTab.append(title)
              strTab.append(image)
              strTab.append(desc)
              outTab.append(strTab)
              strTab = []
      return outTab
      

  def getChannelNames(self):
    nameTab = []
    origTab = self.getChannels()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      nameTab.append(name)
    nameTab.sort()
    return nameTab


  def getChannelNamesAddLink(self):
      origTab = self.getChannels()
      origTab.sort(key=lambda x: x[1])
      for i in range(len(origTab)):
          value = origTab[i]
          url = value[0]
          name = value[1]
          iconimage = value[2]
          desc = value[3]
          self.addLink('weebtv', name, iconimage, url, desc, 'playSelectedMovie')
      xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    
  def getChannelURL(self, key):
      link = ''
      origTab = self.getChannels()
      for i in range(len(origTab)):
          value = origTab[i]
          name = value[1]
          if name == key:
              link = value[0]
              break
      return link
    

  def getChannelIcon(self, key):
    icon = ''
    origTab = self.getChannels()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      if key in name:
	icon = value[2]
	break
    return icon

  def getChannelByURL(self, url):
    icon = ''
    origTab = self.getChannels()
    for chan in origTab:
      if chan[0] == url:
        return chan
    return []


  def playConnection(self, url):
  	  username = 'username'
  	  password = 'password'
  	  if self.settings.WeebTVEnable == 'true':
  	  	  username = self.settings.WeebTVLogin
  	  	  password = self.settings.WeebTVPassword
  	  req = urllib2.Request(url)
  	  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  	  response = urllib2.urlopen(req)
  	  link = response.read()
  	  response.close()
  	  match_src = re.compile('<param name="movie" value="(.+?)" />').findall(link)
  	  match_chn = re.compile('<param name="flashvars" value="(.+?)" />').findall(link)
  	  bitrate = re.search('selected(.*\n){5}.*"programmeListTextRightQuality"[^<]+>([^<]+)<',link).groups()[1]
  	  if len(match_src) == 1 and len(match_chn) == 1:
  	  	  channel = str(match_chn[0]).split('=')
          tab = self.tableConnParams(playerUrl, '1', channel[1], username, password)
          rtmpLink = tab['rtmp']
          ticket = tab['ticket']
          time = tab['time']
          play = tab['play']
          if ticket == None:
              tabb = self.tableConnParams(playerUrl, '0', channel[1], username, password)
              ticket = tabb['ticket']
          if bitrate == 'MULTI' and self.settings.WeebHQ == 'true':
              playpath = play + 'HI'
          else:
              playpath = play
          rtmp = str(rtmpLink) + '/' + playpath
          rtmp += ' swfUrl='  + urllib.unquote_plus(str(match_src[0]))
          rtmp += ' weeb=' + str(ticket) + ';' + username + ';' + password
          rtmp += ' live=true'
          log.info(rtmp)
          self.LOAD_AND_PLAY_VIDEO(rtmp, self.getChannelByURL(url))                   
                

  def tableConnParams(self, playerUrl, numConn, channel, username, password):
      if username == '' and password == '':
          values = {'firstConnect': numConn, 'watchTime': '0', 'cid': channel, 'ip': 'Nan'}
      else:
          values = {'firstConnect': numConn, 'watchTime': '0', 'cid': channel, 'ip': 'Nan', 'username': username, 'password': password}
      headers = { 'User-Agent' : HOST }
      dataConn = urllib.urlencode(values)
      reqUrl = urllib2.Request(playerUrl, dataConn, headers)
      response = urllib2.urlopen(reqUrl)
      link = response.read()
      params = self.getParams(link)
      ticket = self.getParam(params, "73")
      time = self.getParam(params, "16")
      rtmpLink = self.getParam(params, "10")
      playPath = self.getParam(params, "11")
      data = {'rtmp': rtmpLink, 'ticket': ticket, 'time': time, 'play': playPath}
      return data     


  def addLink(self, service, name, iconimage, url, desc, play):
    #u=self.videoLink(url)
    params = self.settings.getParams()
    mode = self.settings.getParam(params, "mode")
    u=sys.argv[0] + "?service=" + service + "&url=" + url + '&page=' + play + '&mode=' + mode
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty("IsPlayable", "false")
    liz.setInfo( type="Video", infoLabels={ "Title": name,
                                           "Plot": desc,
                                           "Genre": "Telewizja online",
                                           "PlotOutline": desc } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)


  def listsMenu(self, table, title):
    value = ''
    if len(table) > 0:
      d = xbmcgui.Dialog()
      choice = d.select(title, table)
      for i in range(len(table)):
        #log.info(table[i])
        if choice == i:
            value = table[i]
    return value


  def listsTable(self, table):
    nTab = []
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def getParam(self, params, name):
        try:
            result = params[name]
            result = urllib.unquote_plus(result)
            return result
        except:
            return None 
        
        
  def getParams(self, paramstring):
        param=[]
        #xbmc.log('raw param string: ' + paramstring)
        if len(paramstring) >= 2:
            params = paramstring
            cleanedparams = params.replace('?','')
            if (params[len(params)-1] == '/'):
                params = params[0:len(params)-2]
            pairsofparams = cleanedparams.split('&')
            param = {}
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if (len(splitparams)) == 2:
                    param[splitparams[0]] = splitparams[1]
        return param


  def LOAD_AND_PLAY_VIDEO(self, videoUrl, chanInfo):
      ok=True
      if videoUrl == '':
          d = xbmcgui.Dialog()
          d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
          return False
      name = chanInfo[1]
      icon = chanInfo[2]
      liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
      liz.setInfo( type="Video", infoLabels={ "Title": name, } )
      try:
          xbmcPlayer = xbmc.Player()
          xbmcPlayer.play(videoUrl, liz)
      except:
          d = xbmcgui.Dialog()
          d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')        
      return ok
    

  def handleService(self):
    log.info('Wejście do TV komercyjnej')
    name = str(self.settings.paramName)
    play = str(self.settings.paramPage)
    url = str(self.settings.paramURL)
    chn = name.replace("+", " ")
    #log.info('b: '+chn + ', play: ' + play + ', url: ' + url + ', name: ' + name)
    if chn == 'None':
        try:
            self.getChannelNamesAddLink()
        except:
            d = xbmcgui.Dialog()
            d.ok('Nie można pobrać kanałów.', 'Przyczyną może być tymczasowa awaria serwisu.', 'Spróbuj ponownie za jakiś czas')
    if play == 'playSelectedMovie':
        self.playConnection(url)