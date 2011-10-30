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
playerUrl = mainUrl + '/player.php'
HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

IMAGE_TAB = {'TVP1': '1.png',
             'TVP2': '2.png',
             'TVN': 'tvn.png',
             'TVN24': '24.png',
             'TVN Turbo': 'tvnturbo.png',
             'Canal+ HD': 'canal.png',
             'Canal+ Film HD': 'cfilm.png',
             '4fun.tv': '4fun.png',
             'Cartoon Network': 'cn.png',
             'EskaTV': 'eska.png',
             'HBO HD': 'hbo.png',
             'HBO 2 HD': 'hbo2.png',
             'MTV': 'mtv.png',
             'nFilm HD': 'nfilm.png',
             'nSport HD': 'nsport.png',
             'Discovery Science': 'science.png',
             'VIVA POLSKA': 'viva.png'}


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
      outTab = []
      strTab = []
      urlChans = mainUrl + '/channels'
      openURL = urllib.urlopen(urlChans)
      readURL = openURL.read()
      openURL.close()
      match_opt = re.compile('<p style="font-size:14px;font-weight:bold;margin-top:-8px;"><a href="(.*?)" title="(.*?)">(.*?)</a></p>').findall(readURL)
      if len(match_opt) > 0:
          for i in range(len(match_opt)):
              link = match_opt[i][0]
              link = link.replace('online', 'channel')
              title = match_opt[i][2]
              image = self.getImage(str(title))
              desc = match_opt[i][1]
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


  def videoLink(self, url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match_src = re.compile('<param name="movie" value="(.+?)" />').findall(link)
    match_chn = re.compile('<param name="flashvars" value="(.+?)" />').findall(link)
    #log.info('src: ' + str(len(match_src)) + ', chn: ' + str(len(match_chn)))
    if len(match_src) == 1 and len(match_chn) == 1:
        channel = str(match_chn[0]).split('=')
        #rtmp = 'rtmp://' + APP_HOST + '/live/' + channel[1] + '/'
        rtmp = 'rtmp://' + self.settings.WeebIP + '/live/' + channel[1] + '/'
        rtmp += ' swfUrl='  + urllib.unquote_plus(str(match_src[0]))
        rtmp += ' pageUrl=' + url
        #rtmp += ' tcUrl=rtmp://' + APP_HOST + '/live/' + channel[1]
        rtmp += ' tcUrl=rtmp://' + self.settings.WeebIP + '/live/' + channel[1]
        rtmp += ' playpath=live'
        rtmp += ' swfVfy=true'
        rtmp += ' live=true'
        #log.info(rtmp)
        return rtmp


  def playConnection(self, url, username, password):
      req = urllib2.Request(url)
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      match_src = re.compile('<param name="movie" value="(.+?)" />').findall(link)
      match_chn = re.compile('<param name="flashvars" value="(.+?)" />').findall(link)
      if len(match_src) == 1 and len(match_chn) == 1:
          channel = str(match_chn[0]).split('=')
          tab = self.tableConnParams(playerUrl, '1', channel[1], username, password)
          rtmpLink = tab['rtmp']
          ticket = tab['ticket']
          time = tab['time']
          if ticket == None:
              tabb = self.tableConnParams(playerUrl, '0', channel[1], username, password)
              ticket = tabb['ticket']
          rtmp = str(rtmpLink) + '/'
          rtmp += ' swfUrl='  + urllib.unquote_plus(str(match_src[0]))
          rtmp += ' pageUrl=' + url
          rtmp += ' tcUrl=' + str(rtmpLink)
          rtmp += ' weeb=' + str(ticket)
          rtmp += ' playpath=live'
          rtmp += ' swfVfy=true'
          rtmp += ' live=true'
          log.info(rtmp)
          #self.ticketSender(ticket, str(rtmpLink))
          self.LOAD_AND_PLAY_VIDEO(rtmp)                   
                

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
      ticket = self.getParam(params, "15")
      time = self.getParam(params, "16")
      rtmpLink = self.getParam(params, "10")
      data = {'rtmp': rtmpLink, 'ticket': ticket, 'time': time}
      return data     
              
      
  def login(self, user, password):
    loginUrl = mainUrl + '/account/login/after&go=home'
    try:
      cookiejar = cookielib.LWPCookieJar()
      cookiejar = urllib2.HTTPCookieProcessor(cookiejar) 
      opener = urllib2.build_opener(cookiejar)
      urllib2.install_opener(opener)
      values = {'username': user, 'userpassword': password, 'go': 'home', 'v1': '', 'v2': ''}
      headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' }
      data = urllib.urlencode(values)
      req = urllib2.Request(loginUrl, data, headers)
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      web = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
      match=re.compile('Nazwa użytkownika lub hasło są nie poprawne.').findall(web)
      if(len(match) > 0):
	d = xbmcgui.Dialog()
        d.ok('BŁĄD logowania', 'Podana nazwa użytkownika,', 'lub hasło jest niepoprawne.', 'Wpisz poprawnie te dane.')
        return False
      else:
	return True
    except:
      d = xbmcgui.Dialog()
      d.ok('BŁĄD logowania.', 'Upłynął czas limitu rządania', 'Spróbuj ponownie za jakiś czas.')
      return False


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


  def LOAD_AND_PLAY_VIDEO(self, videoUrl):
      ok=True
      if videoUrl == '':
          d = xbmcgui.Dialog()
          d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
          return False
      try:
          xbmcPlayer = xbmc.Player()
          xbmcPlayer.play(videoUrl)
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
    log.info('b: '+chn + ', play: ' + play + ', url: ' + url + ', name: ' + name)
    if chn == 'None':
        try:
            if self.settings.WeebTVEnable == 'true':
                log.info('zalogowany')
                self.getChannelNamesAddLink()
                #self.getChannels()
            else:
                log.info('bez logowania')
                self.getChannelNamesAddLink()
                #self.getChannels()
        except:
            d = xbmcgui.Dialog()
            d.ok('Nie można pobrać kanałów.', 'Przyczyną może być tymczasowa awaria serwisu.', 'Spróbuj ponownie za jakiś czas')
    if play == 'playSelectedMovie':
        log.info('Odtwarzam')
        self.playConnection(url, '', '')
              

