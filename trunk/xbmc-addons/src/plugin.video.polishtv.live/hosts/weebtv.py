# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys
import xbmcgui, xbmcplugin, xbmcaddon, xbmc

scriptID = sys.modules[ "__main__" ].scriptID

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
#sys.path.append( os.path.join( os.getcwd(), "../" ) )

import pLog, settings

log = pLog.pLog()

mainUrl = 'http://weeb.tv'

class WeebTV:
  def __init__(self):
    log.info('Loading WeebTV')
    self.settings = settings.TVSettings()


  def handle(self):
    channel = self.getChannelNamesAddDir()
    log.info(str(channel))


  def getChannels(self):
    outTab = []
    tabURL = []
    strTab = []
    urlChans = mainUrl + '/channels'
    openURL = urllib.urlopen(urlChans)
    readURL = openURL.read()
    openURL.close()
    tabURL = readURL.replace('\n', '').split('<')
    for line in tabURL:
      #log.info(line)
      #exprLink = re.match(r'^fieldset onclick="location.href=\'(.*?)\'">$', line, re.M|re.I)
      exprLink = re.match(r'^fieldset onclick="location.href=\'(.*?)\'".*$', line, re.M|re.I)
      exprName = re.match(r'^legend align="center" title=".*?">(.*?)$', line, re.M|re.I)
      #exprName2 = re.match(r'^.*?>(.*?).*$', line, re.M|re.I)
      exprIcon = re.match(r'^img src="(.*?)" alt=".*?" height=".*?" width=".*?" />$', line, re.M|re.I)
      if exprLink:
	strTab.append(exprLink.group(1))
      if exprName:
	strTab.append(exprName.group(1))
      if exprIcon:
	strTab.append(exprIcon.group(1))
	outTab.append(strTab)
      if '/fieldset' in line:
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


  def getChannelNamesAddDir(self):
    origTab = self.getChannels()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      iconimage = value[2]
      #log.info(str(name) + ', ' + str(mode) + ', ' + str(url) + ', ' + str(iconimage))
      #self.addDir(name, mode, True, False)
      self.addDir(name, iconimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    
  def getChannelURL(self, key):
    link = ''
    origTab = self.getChannels()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      if key in name:
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
    match = re.compile('<embed id="player_embed" type=".+?" src="(.+?)" flashvars="(.+?)" allowscriptaccess=".+?" allowfullscreen=".+?" quality=".+?"').findall(link)
    if len(match) > 0:
      #chan = split(';', str(match[0][1]))
      channel = str(match[0][1]).split('=')
      rtmp = 'rtmp://app.weeb.tv/live/'
      rtmp += ' swfUrl='  + urllib.unquote_plus(str(match[0][0]))
      rtmp += ' pageUrl=' + mainUrl + '/'
      #rtmp += ' tcUrl=' +  urllib.unquote_plus(str(match[0][1]))
      rtmp += ' playpath=' + channel[1]
      rtmp += ' swfVfy=true'
      rtmp += ' live=true'
      return rtmp
      
      
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


  def addDir(self, name, iconimage):
    #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    u=sys.argv[0]+"?name="+urllib.quote_plus(name)
    log.info(str(u))
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
    
    
  def get_params(self):
    param=[]
    paramstring=sys.argv[2]
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


  def LOAD_AND_PLAY_VIDEO(self, videoUrl):
        log.info('url: ' + videoUrl)
        ok=True
        if videoUrl == '':
                d = xbmcgui.Dialog()
                d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
                return False
        #try:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoUrl)
        #except:
        #    d = xbmcgui.Dialog()
        #    d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')        
        return ok
    

  def handleService(self):
    log.info('Wejście do TV komercyjnej')
    #tt = weebtv.WeebTV()
    #tt.handle()
    try:
      chn = self.listsMenu(self.getChannelNames(), "Wybór kanału")
    except:
      d = xbmcgui.Dialog()
      d.ok('Nie można pobrać kanałów.', 'Przyczyną może być tymczasowa awaria serwisu.', 'Spróbuj ponownie za jakiś czas')        
    if chn != '':
        link = self.getChannelURL(chn)
        if self.settings.WeebTVEnable == 'true':
          #log.info('podany login: ' + self.settings.WeebTVLogin)
          #log.info('podane hasło: ' + self.settings.WeebTVPassword)
          if self.login(self.settings.WeebTVLogin, self.settings.WeebTVPassword):
              #log.info('zalogowany')
              self.LOAD_AND_PLAY_VIDEO(self.videoLink(link))
          else:
              #log.info('bez logowania')
              self.LOAD_AND_PLAY_VIDEO(self.videoLink(link))


