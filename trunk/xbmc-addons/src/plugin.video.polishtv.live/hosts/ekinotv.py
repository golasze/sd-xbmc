# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "ekinotv.cookie"

import pLog, settings, Parser, urlparser

log = pLog.pLog()
cj = cookielib.LWPCookieJar()

mainUrl = 'http://www.ekino.tv'


sortby = ptv.getSetting('ekinotv_sort')
sortorder = ptv.getSetting('ekinotv_sortorder')
username = ptv.getSetting('ekinotv_login')
password = ptv.getSetting('ekinotv_password')


EKINO_MENU_TABLE = {
  1: "Filmy [wg. gatunków]",
  2: "Filmy [lektor]",
  3: "Filmy [napisy]",
  4: "Filmy [najpopularniejsze]",
  5: "Seriale",
  6: "Wyszukaj"
  }


HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
PAGE_MOVIES = 10
DUB_LINK = mainUrl + '/tag,lektor,1.html'
SUB_LINK = mainUrl + '/tag,napisy,1.html'


class EkinoTV:
  def __init__(self):
    log.info('Loading EkinoTV')
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()
    self.up = urlparser.urlparser()
  
  
  def postData(self, url, postval = {}):
    headers = { 'User-Agent' : HOST }
    data = urllib.urlencode(postval)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    return data
  
   
  def requestData(self, url):
    if os.path.isfile(COOKIEFILE):
      cj.load(COOKIEFILE)
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    response = opener.open(req)
    data = response.read()
    response.close()    
    return data
  
  
  def checkDirCookie(self):
    if not os.path.isdir(ptv.getAddonInfo('path') + os.path.sep + "cookies"):
      os.mkdir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
  
  
  def requestLoginData(self):
    if username=='' or password=='':
      xbmc.executebuiltin("XBMC.Notification(Niezalogowany, uzywam Player z limitami,2000)")
    else:
      url = mainUrl + "/logowanie.html?login=1"
      headers = { 'User-Agent' : HOST }
      post = { 'username': username, 'password': password }
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      data = urllib.urlencode(post)
      req = urllib2.Request(url, data, headers)
      response = opener.open(req)
      link = response.read()
      response.close()
      self.checkDirCookie()
      cj.save(COOKIEFILE)
      if self.isLoggedIn(link):
	xbmc.executebuiltin("XBMC.Notification(" + username + ", Zostales poprawnie zalogowany,2000)")
      else:
	xbmc.executebuiltin("XBMC.Notification(Blad logowania, uzywam Player z limitami,2000)")


  def isLoggedIn(self, data):
    #<div class="span-7 medium lh200 last">Zalogowany jako: <b>
    if 'Zalogowany jako:' in data:
      return True
    else:
      return False
    
  def setTable(self):
    return EKINO_MENU_TABLE


  def setDubLink(self):
    return DUB_LINK


  def setSubLink(self):
    return SUB_LINK


  def getMenuTable(self):
    nTab = []
    for num, val in EKINO_MENU_TABLE.items():
      nTab.append(val)
    return nTab
    
  
  def getCategories(self):
    valTab = []
    strTab = []
    url = mainUrl + '/kategorie.html'
    link = self.requestData(url)
    tabURL = link.replace(' ', '').split('\n')
    for line in tabURL:
      r = re.compile('<ahref="(' + mainUrl + '/filmy,.+?)"title=".+?"><divclass="columnspan-4">(.+?)<span>\((.+?)\)</span></div></a>').findall(line)    
      if len(r)>0:
	strTab.append(r[0][0])
	strTab.append(r[0][1])
	strTab.append(r[0][2])
	valTab.append(strTab)
      if '/span' in line:
	strTab = []
    return valTab 
  
  
  def getCategoryName(self):
    nameTab = []
    origTab = self.getCategories()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      nameTab.append(name)
    nameTab.sort()
    return nameTab
    
    
  def getCategoryURL(self, key):
    link = ''
    origTab = self.getCategories()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      if key in name:
	link = value[0]
	break
    return link
    
 
  def videoMetadata(self, title = "", plot = ""):
    plot = plot.replace("<br />","").replace("<br/>","").replace("<br>","").replace("&quot;","\"") 
    details = {'title' : title,
	       'plot'  : plot}
    return details
  

  def getMovieTab(self, url):
    if sortby=='ocena':
      sSort = 'p'
    if sortby=='popularnosc':
      sSort = 'o'
    if sortby=='data dodania':
      sSort = 'd'
    if sortby=='tytul':
      sSort = 't'
      
    if sortorder=='malejaco':
      sHow = 'desc'
    else:
      sHow = 'asc'
    nextPage=''
     
    strTab = []
    valTab = []
    values = {'sSort': sSort, 'sHow': sHow}
    
    link = self.postData(url, values)
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      expr1 = re.match(r'^.+?<img class="link_img" src="(.+?)" title="(.+?)" .+ />', line, re.M|re.I)
      expr2 = re.match(r'^<p>(.+?)<a href="(.+?)" title=".+?">.+?</a></p>$', line, re.M|re.I)
      expr3 = re.match(r'^<li style="display:inline;" class="next"><a href="(.+?)" title=".+?" >.+?</a></li>$', line, re.M|re.I)
      if expr1:
	title = expr1.group(2)
	strTab.append(expr1.group(1))
	strTab.append(expr1.group(2))
      if expr2:
	plot = expr2.group(1)
	metadata = [title,plot]
	strTab.append(metadata)
	strTab.append(expr2.group(2))
	valTab.append(strTab)
      if expr3:
	nextPage = expr3.group(1)
      if '<div class="column span-15 movie_container">' in line:
	strTab = []
    if nextPage:
      valTab.append(['','nastepna','',nextPage]) 
    return valTab


  def getMoviesPopTab(self):
    url = mainUrl + '/kategorie.html'
    return self.getMovieTab(url)


  def getMovieURL(self, table, key):
    link = ''
    for i in range(len(table)):
      value = table[i]
      name = value[1]
      if key in name:
	link = value[3]
	break
    return link


  def getSerialsTab(self):
    valTab = []
    strTab = []
    url = mainUrl + '/seriale-online.html'
    link = self.requestData(url)
    tabURL = link.replace('\t', '').replace('<sup class=\'red\'>new!</sup>', '').split('</li>')
    for line in tabURL:
      expr = re.match(r'.+?<a class=".+?" href="(.+?)" title=".+?">(.+?)</a>', line, re.M|re.I)
      if expr:
	strTab.append(expr.group(2).replace('&nbsp;', ''))
	strTab.append(expr.group(1))
	valTab.append(strTab)
	strTab = []
    return valTab
    

  def getSerialNamesTab(self, table):
    nameTab = []
    for i in range(len(table)):
      value = table[i]
      name = value[0]
      nameTab.append(name.replace('&nbsp;', ''))
    return nameTab 
    
  
  def getSerialNames(self):
    return self.getSerialNamesTab(self.getSerialsTab())
    

  def getSerialInfoTab(self, url):
    strTab = []
    link = self.requestData(url)
    tabURL = link.replace('\t', '').split('</div>')
    for line in tabURL:
      expr1 = re.match(r'.+?<div class="content" style="text-align:center">.+?<img src="(.+?)" alt="(.+?)"/>', line.replace('\n', ''), re.M|re.I)
      expr2 = re.match(r'.+?<div class="content">.+?<center><img src=".+?" title=".+?" style="max-width:450px;"></center>.+?<p class="truncate200">(.+?)</p>', line.replace('\n', ''), re.M|re.I)
      if expr1:
	strTab.append(expr1.group(2))
	strTab.append(expr1.group(1))
      if expr2:
	strTab.append(expr2.group(1).replace('\t' , '').replace('  ', ''))
    return strTab    


  def getSerialsFullTab(self):
    strTab = []
    valTab = []
    table = self.getSerialsTab()
    for i in range(len(table)):
      value = table[i]
      url = value[1]
      title = value[0]
      img = ''
      plot = ''
      tab = self.getSerialInfoTab(url)
      for i in range(len(tab)):
  	value = tab[i]
  	img = value[0]
  	plot = value[1]
      strTab.append(img)
      strTab.append(title)
      strTab.append(plot)
      strTab.append(url)
      valTab.append(strTab)
      strTab = []
    return valTab


  def getSeasonsTab(self, url):
    strTab = []
    link = self.requestData(url)
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      expr = re.match(r'.+?<div class="header"><h2>(.+?)</h2></div>$', line, re.M|re.I)
      if expr:
	if 'Sezon ' in expr.group(1):
	  strTab.append(expr.group(1))
    return strTab    


  def getPartsTab(self, url):
    valTab = []
    strTab = []
    link = self.requestData(url)
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      expr = re.match(r'.+?<li>(.+)<a href="(.+?)" title="(.+?) Odcinek\:.+?">(.+?)</a></li>$', line, re.M|re.I)
      expr_bak = re.match(r'.+?<li>(.+)<a href="(.+?)" title="(.+?) Odcinek\:.+?">(.+?)</a>.+?</li>$', line, re.M|re.I)
      if expr:
	if expr.group(2).startswith('http://'):
	  strTab.append(expr.group(1).replace('\t' , '').replace('  ', ''))
	  strTab.append(expr.group(2))
	  strTab.append(expr.group(3))
	  strTab.append(expr.group(4))
	  valTab.append(strTab)
	  strTab = []
      elif expr_bak:
	if expr_bak.group(2).startswith('http://'):
	  strTab.append(expr_bak.group(1).replace('\t' , '').replace('  ', ''))
	  strTab.append(expr_bak.group(2))
	  strTab.append(expr_bak.group(3))
	  strTab.append(expr_bak.group(4))
	  valTab.append(strTab)
	  strTab = []
    return valTab
    

  def getSerialURL(self, title):
    url = ''
    origTab = self.getSerialsTab()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[0]
      if title == name:
	url = value[1]
    return url
    
    
  def getSeasonPartsTitle(self, key, title):
    s = key.split(' ')
    titles = []
    table = self.getPartsTab(self.getSerialURL(title))
    for i in range(len(table)):
      value = table[i]
      part = value[0]
      name = value[3]
      season = value[2]
      if s[1] in season:
	titles.append(part + ' ' + name)
    return titles
    
    
  def getPartURL(self, key, title):
    url = ''
    table = self.getPartsTab(self.getSerialURL(title))
    for i in range(len(table)):
      value = table[i]
      name = value[3]
      if name in key:
	url = value[1]
	break
    return url


  def getItemTitles(self, table):
    out = []
    for i in range(len(table)):
      value = table[i]
      out.append(value[0])
    return out


  def getItemURL(self, table, key):
    link = ''
    for i in range(len(table)):
      value = table[i]
      if key in value[0]:
	link = value[1]
	break
    return link


  def getMovieURLFalse(self, url):
    fl = 'None'
    link = self.requestData(url)
    if self.isLoggedIn(link):
      #showVideo('http://www.ekino.tv/gcp,115451,v.html', $('#7e40699b1694f9d5e248289731904d47'));
      match = re.compile("showVideo\('(.+?)'").findall(link)
    else:
      match = re.compile('<div class="placeholder" style=".+?" onclick="(.+?)"><img src="http://static.ekino.tv/static/img/player_kliknij.jpg" alt="player" /></div>').findall(link)
    if len(match) == 1:
      if self.isLoggedIn(link):
	fl = match[0]
      else:
	fLink = match[0].split('\'')
	fl = str(fLink[1])
    elif len(match) > 1:
      valTab = []
      strTab = []
      for i in range(len(match)):
	a = i + 1
	strTab.append('Film ' + str(a))
	if self.isLoggedIn(link):
	  strTab.append(match[i])
	else:  
	  fLink = match[i].split('\'')
	  strTab.append(fLink[1])
	valTab.append(strTab)
	strTab = []
      d = xbmcgui.Dialog()
      item = d.select("Wybór filmu", self.getItemTitles(valTab))
      if item != '':
	item = item + 1
	fl = self.getItemURL(valTab, str(item))
    else:
      d = xbmcgui.Dialog()
      d.ok('Brak linku do filmu', 'Przepraszamy, ale w tej chwili nie możemy wyświetlić', 'Ci pełnej wersji tego filmu.')
      fl = 'None'
    print fl
    return fl


  def videoMovieLink(self, url):
    nUrl = ''
    link = self.getMovieURLFalse(url)
    if link != 'None':
      data = self.requestData(link)
      if "provider: 'lighttpd'" in data:
	match = re.compile("clip: {\n.+?url: '(.+?)'").findall(data)
	if len(match)==1:
	  nUrl = match[0]
      else:	
	match = re.compile('<iframe src="(.+?)".+?width').findall(link)
	if len(match) > 0:
	  nUrl = self.up.getVideoLink(match[0])
    if nUrl == '':
      d = xbmcgui.Dialog()
      d.ok('Player Limit','Wyczerpany limit czasowy oglądania','Spróbuj ponownie za jakiś czas')
    return nUrl		  

    
  def searchInputText(self):
    text = None
    k = xbmc.Keyboard()
    k.doModal()
    if (k.isConfirmed()):
      text = k.getText()
    return text


  def searchTab(self, text):
    strTab = []
    valTab = []
    searchUrl = mainUrl + '/szukaj.html'
    values = {'q': text}
    headers = { 'User-Agent' : HOST }
    data = urllib.urlencode(values)
    req = urllib2.Request(searchUrl, data, headers)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    tabURL = link.replace('\n', '').split('<p class="separator_h_5">')
    for line in tabURL:
      expr = re.match(r'^.+?<img class="link_img" src="(.+?)" title=".+?" alt=".+?" /></a>.+?</div>.+?<p class="h2"><a href=".+?" title=">.+?">(.+?)</a></p>.+?<p>(.+?)<a href="(.+?)" title=".+?">.+?</a></p>', line, re.M|re.I)
      if expr:
	title = expr.group(2)
	plot = expr.group(3)
	strTab.append(expr.group(1))
	strTab.append(expr.group(2))
	strTab.append([title,plot])
	strTab.append(expr.group(4))
	valTab.append(strTab)
	strTab = []
    return valTab

    
  def isNumeric(self,s):
    try:
      float(s)
      return True
    except ValueError:
      return False


  def listsAddLinkMovie(self, table):
    for i in range(len(table)):
      value = table[i]
      title = value[1]
      iconimage = value[0]
      if title!='nastepna':
	dict = self.videoMetadata(value[2][0],value[2][1])
	self.add('ekinotv', 'playSelectedMovie', 'movie', 'None', title, iconimage, dict, True, False)
      else:
	expr1 = value[3].split(',')
	category = expr1[1]
	if category=='lektor' or category=='napisy':
	  expr2 = expr1[2].split('.')
	else:
	  expr2 = expr1[3].split('.')
	page = expr2[0]    
	self.add('ekinotv', title, category, page, 'None', 'None', self.videoMetadata(), True, False)
    #zmien view na "Media Info 2"
    xbmcplugin.setContent(int(sys.argv[1]),'movies')
    xbmc.executebuiltin("Container.SetViewMode(503)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def listsAddLinkSerial(self, table, category):
    for i in range(len(table)):
      title = table[i]
      self.add('ekinotv', 'playSelectedMovie', 'serial', category, title, '', self.videoMetadata(), True, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def listsAddDirMenu(self, table, name, category, page):
    for i in range(len(table)):
      if name == 'None':
	self.add('ekinotv', table[i], 'None', 'None', 'None', 'None', self.videoMetadata(), True, False)
      elif category == 'None' and name != 'None':
	self.add('ekinotv', name, table[i], 'None', 'None', 'None', self.videoMetadata(), True, False)
      elif name != 'None' and category != 'None' and page == 'None':
	self.add('ekinotv', name, category, table[i], 'None', 'None', self.videoMetadata(), True, False)
      elif name != 'None' and category != 'None' and page != 'None':
	self.add('ekinotv', name, category, page, table[i], 'None', self.videoMetadata(), True, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def add(self, service, name, category, page, title, iconimage, metadata, folder = True, isPlayable = True):
    u=sys.argv[0] + "?service=" + service + "&name=" + urllib.quote_plus(name) + "&category=" + urllib.quote_plus(category) + "&page=" + urllib.quote_plus(page) + "&title=" + urllib.quote_plus(title)
    if name == 'playSelectedMovie':
      name = title
    elif name != 'None' and category != 'None' and page == 'None':
      name = category
    elif name != 'None' and category != 'None' and page != 'None' and not self.isNumeric(page): 
      name = page
    if iconimage == '':
      iconimage = "DefaultVideo.png"
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo('video', metadata )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
    

  def LOAD_AND_PLAY_VIDEO(self, videoUrl, title):
    ok=True
    if videoUrl == '':
      return False
    thumbnail = xbmc.getInfoImage("ListItem.Thumb")
    liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    liz.setInfo( type="Video", infoLabels={ "Title": title } )
    try:
      xbmcPlayer = xbmc.Player()
      xbmcPlayer.play(videoUrl, liz)
    except:
      d = xbmcgui.Dialog()
      d.ok('Błąd przy przetwarzaniu, lub wyczerpany limit czasowy oglądania.', 'Zarejestruj się i opłać abonament.', 'Aby oglądać za darmo spróbuj ponownie za jakiś czas')		
    return ok


  def handleService(self):
    params = self.parser.getParams()
    name = str(self.parser.getParam(params, "name"))
    title = str(self.parser.getParam(params, "title"))
    category = str(self.parser.getParam(params, "category"))
    page = str(self.parser.getParam(params, "page"))
    name = name.replace("+", " ")
    title = title.replace("+", " ")
    category = category.replace("+", " ")
    page = page.replace("+", " ")
  	
    if name == 'None':
      self.requestLoginData()
      self.listsAddDirMenu(self.getMenuTable(), 'None', 'None', 'None')
    elif name == self.setTable()[1] and category == 'None':
      self.listsAddDirMenu(self.getCategoryName(), name, 'None', 'None')
    elif name == self.setTable()[1] and category != 'None' and page == 'None':
      self.listsAddLinkMovie(self.getMovieTab(mainUrl + '/filmy,' + category + ',1,1.html'))
    elif name == 'nastepna' and category != 'None' and self.isNumeric(page):
      if category == 'lektor' or category=='napisy':
	self.listsAddLinkMovie(self.getMovieTab(mainUrl + '/tag,' + category + ',' + page + '.html'))		  
      else:
	self.listsAddLinkMovie(self.getMovieTab(mainUrl + '/filmy,' + category + ',1,' + page + '.html'))
      page = str(int(page) + 1)
    #lektor
    if name == self.setTable()[2]:
      self.listsAddLinkMovie(self.getMovieTab(self.setDubLink()))
    #napisy
    if name == self.setTable()[3]:
      self.listsAddLinkMovie(self.getMovieTab(self.setSubLink()))
    #najpopularniejsze
    if name == self.setTable()[4]:
      self.listsAddLinkMovie(self.getMoviesPopTab())
    #serial
    if name == self.setTable()[5] and category == 'None':
      self.listsAddDirMenu(self.getSerialNames(), name, 'None', 'None')
    elif name == self.setTable()[5] and category != 'None' and page == 'None':
      self.listsAddDirMenu(self.getSeasonsTab(self.getSerialURL(category)), name, category, page)
    elif name == self.setTable()[5] and category != 'None' and page != 'None':
      self.listsAddLinkSerial(self.getSeasonPartsTitle(page, category), category)
    #szukaj
    if name == self.setTable()[6]:
      text = self.searchInputText()
      if text != None:
	self.listsAddLinkMovie(self.searchTab(text))
  	
    if name == 'playSelectedMovie':
      urlLink = ''
      if title != 'None' and category == 'movie':
	urlLink = self.getMovieURL(self.searchTab(title), title)
      elif title != 'None' and category == 'serial' and page != 'None':
	urlLink = self.getPartURL(title, page)	  		
      if urlLink.startswith('http://'):
	log.info("url: " + urlLink)
	self.LOAD_AND_PLAY_VIDEO(self.videoMovieLink(urlLink), title)
