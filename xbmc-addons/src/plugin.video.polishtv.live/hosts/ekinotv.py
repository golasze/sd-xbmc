# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc
import thread


BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, megavideo, cacaoweb

log = pLog.pLog()

mainUrl = 'http://www.ekino.tv'

EKINO_MENU_TABLE = { 1: "Filmy [wg. gatunków]",
		   2: "Filmy [lektor]",
		   3: "Filmy [napisy]",
		   4: "Filmy [najpopularniejsze]",
		   5: "Seriale",
		   6: "Wyszukaj" }


HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
PAGE_MOVIES = 10
MEGAVIDEO_MOVIE_URL = 'http://www.megavideo.com/v/'
DUB_LINK = mainUrl + '/tag,lektor.html'
SUB_LINK = mainUrl + '/tag,napisy.html'
STREAM_LINK = 'http://127.0.0.1:4001/megavideo/megavideo.caml?videoid='


class EkinoTV:
  def __init__(self):
    log.info('Loading EkinoTV')
    
    
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
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    #tabURL = link.replace('\n', '').split('<')
    tabURL = link.replace(' ', '').split('\n')
    for line in tabURL:
      #expr = re.match(r'<a href="(' + mainUrl + '/filmy,.+?)" title="(.+?)">$', line, re.M|re.I)
      expr = re.match(r'<ahref="(' + mainUrl + '/filmy,.+?)"title="(.+?)"><divclass="columnspan-4">.+?<span>\((.+?)\)</span></div></a>$', line, re.M|re.I)
      if expr:
	strTab.append(expr.group(1))
	strTab.append(expr.group(2))
	strTab.append(expr.group(3))
	#log.info(str(strTab))
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
    
  
  def getCategoryNums(self, key):
    num = ''
    origTab = self.getCategories()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[1]
      if key in name:
	num = value[2]
	break
    return num
    
  
  def getSortMovies(self, title):
    sortTab = []
    s = self.getCategoryNums(title)
    #log.info(s + ', ' + title)
    a = math.ceil(float(s) / float(PAGE_MOVIES))
    for i in range(int(a)):
      strNum = i + 1
      strText = 'Lista z filmami: '
      sortTab.append(strText + str(strNum))
    return sortTab  


  def getSortLinkMovies(self, url):
    sortTab = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('<p>.+?<b>(.+?)</b>.+?"<b>.+?</b>".+?</p>').findall(link)
    log.info('match: ' + str(match))
    if len(match) > 0:
      a = math.ceil(float(match[0]) / float(PAGE_MOVIES))
      for i in range(int(a)):
	strNum = i + 1
	strText = 'Lista z filmami: '
	sortTab.append(strText + str(strNum))
    #log.info(str(sortTab))
    return sortTab 


  def getMovieTab(self, url):
    strTab = []
    valTab = []
    values = {'sSort': 't', 'sHow': 'asc'}
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    #tabURL = link.replace('\n', '').split('<')
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      #log.info(line)
      #expr1 = re.match(r'^.+?<img class="link_img" src="(.+?)" title="(.+?)" alt=".+?" width=".+?" height=".+?" />', line, re.M|re.I)
      expr1 = re.match(r'^.+?<img class="link_img" src="(.+?)" title="(.+?)" .+ />', line, re.M|re.I)
      expr2 = re.match(r'^<p>(.+?)<a href="(.+?)" title=".+?">.+?</a></p>$', line, re.M|re.I)
      if expr1:
	#log.info(expr1.group(1))
	strTab.append(expr1.group(1))
	strTab.append(expr1.group(2))
      if expr2:
	#log.info(expr2.group(1))
	#log.info(expr2.group(2))
	strTab.append(expr2.group(1))
	strTab.append(expr2.group(2))
	valTab.append(strTab)
      if '<div class="column span-15 movie_container">' in line:
	strTab = []
    #log.info(str(valTab))
    return valTab


  def getMoviesCatTab(self, page, category):
    catt = self.getCategoryURL(category).split(',')
    cat = catt[2].split('.html')
    num = page.split(': ')
    url = ''
    if num[1] == 1:
      url = mainUrl + '/filmy,' + category + ',' + cat[0] + '.html'
    else:
      url = mainUrl + '/filmy,' + category + ',' + cat[0] + ',' + num[1] + '.html'
    return self.getMovieTab(url)


  def getMoviesDubTab(self, page):
    num = page.split(': ')
    url = ''
    if num[1] == 1:
      url = mainUrl + '/tag,lektor.html'
    else:
      url = mainUrl + '/tag,lektor,' + num[1] + '.html'
    return self.getMovieTab(url)


  def getMoviesSubTab(self, page):
    num = page.split(': ')
    url = ''
    if num[1] == 1:
      url = mainUrl + '/tag,napisy.html'
    else:
      url = mainUrl + '/tag,napisy,' + num[1] + '.html'
    return self.getMovieTab(url)


  def getMoviesPopTab(self):
    url = mainUrl + '/kategorie.html'
    return self.getMovieTab(url)


  def getMovieNamesTab(self, table):
    nameTab = []
    for i in range(len(table)):
      value = table[i]
      name = value[1]
      nameTab.append(name)
    nameTab.sort()
    return nameTab    


  def getMovieCatNames(self, page, category):
    origTab = self.getMoviesCatTab(page, category)
    return self.getMovieNamesTab(origTab)


  def getMovieDubNames(self, page):
    origTab = self.getMoviesDubTab(page)
    return self.getMovieNamesTab(origTab)


  def getMovieSubNames(self, page):
    origTab = self.getMoviesSubTab(page)
    return self.getMovieNamesTab(origTab)
    

  def getMoviePopNames(self):
    origTab = self.getMoviesPopTab()
    return self.getMovieNamesTab(origTab)


  def getMovieURL(self, table, key):
    link = ''
    for i in range(len(table)):
      value = table[i]
      name = value[1]
      if key in name:
	link = value[3]
	break
    return link


  def getMovieCatURL(self, page, category, key):
    origTab = self.getMoviesCatTab(page, category)
    return self.getMovieURL(origTab, key)


  def getMovieDubURL(self, page, key):
    origTab = self.getMoviesDubTab(page)
    return self.getMovieURL(origTab, key)


  def getMovieSubURL(self, page, key):
    origTab = self.getMoviesSubTab(page)
    return self.getMovieURL(origTab, key)


  def getMoviePopURL(self, key):
    origTab = self.getMoviesPopTab()
    return self.getMovieURL(origTab, key)


  def getSerialsTab(self):
    valTab = []
    strTab = []
    url = mainUrl + '/seriale-online.html'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    #tabURL = link.replace('\n', '').split('<')
    tabURL = link.replace('\t', '').replace('<sup class=\'red\'>new!</sup>', '').split('</li>')
    for line in tabURL:
      #log.info(line)
      expr = re.match(r'.+?<a class=".+?" href="(.+?)" title=".+?">(.+?)</a>', line, re.M|re.I)
      #<a class="serNewA" href="link" title="tytul">tytul</a>
      #expr = re.match(r'<ahref="(' + mainUrl + '/filmy,.+?)"title="(.+?)"><divclass="columnspan-4">.+?<span>\((.+?)\)</span></div></a>$', line, re.M|re.I)
      if expr:
	#log.info(expr.group(2))
	strTab.append(expr.group(2).replace('&nbsp;', ''))
	strTab.append(expr.group(1))
	valTab.append(strTab)
	strTab = []
    #log.info(valTab)
    return valTab
    

  def getSerialNamesTab(self, table):
    nameTab = []
    for i in range(len(table)):
      value = table[i]
      name = value[0]
      nameTab.append(name.replace('&nbsp;', ''))
    #nameTab.sort()
    return nameTab 
    
  
  def getSerialNames(self):
    return self.getSerialNamesTab(self.getSerialsTab())
    

  def getSerialInfoTab(self, url):
    strTab = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    #tabURL = link.replace('\n', '').split('<')
    tabURL = link.replace('\t', '').split('</div>')
    for line in tabURL:
      #log.info(line.replace('\n', ''))
      expr1 = re.match(r'.+?<div class="content" style="text-align:center">.+?<img src="(.+?)" alt="(.+?)"/>', line.replace('\n', ''), re.M|re.I)
      expr2 = re.match(r'.+?<div class="content">.+?<center><img src=".+?" title=".+?" style="max-width:450px;"></center>.+?<p class="truncate200">(.+?)</p>', line.replace('\n', ''), re.M|re.I)
      if expr1:
	strTab.append(expr1.group(2))
	strTab.append(expr1.group(1))
      if expr2:
	strTab.append(expr2.group(1).replace('\t' , '').replace('  ', ''))
    #log.info(strTab)
    return strTab    


  def getSeasonsTab(self, url):
    strTab = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    #tabURL = link.replace('\n', '').split('<')
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      #log.info(line)
      expr = re.match(r'.+?<div class="header"><h2>(.+?)</h2></div>$', line, re.M|re.I)
      if expr:
	if 'Sezon ' in expr.group(1):
	  strTab.append(expr.group(1))
    #log.info(strTab)
    return strTab    


  def getPartsTab(self, url):
    valTab = []
    strTab = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    tabURL = link.replace('\t', '').split('\n')
    for line in tabURL:
      #log.info(line)
      expr = re.match(r'.+?<li>(.+)<a href="(.+?)" title="(.+?) Odcinek\:.+?">(.+?)</a></li>$', line, re.M|re.I)
      if expr:
	if expr.group(2).startswith('http://'):
	  #log.info(expr1.group(1))
	  strTab.append(expr.group(1).replace('\t' , '').replace('  ', ''))
	  strTab.append(expr.group(2))
	  strTab.append(expr.group(3))
	  strTab.append(expr.group(4))
	  valTab.append(strTab)
	  strTab = []
    #log.info('result: ' + str(valTab))
    return valTab
    

  def getSerialURL(self, title):
    url = ''
    origTab = self.getSerialsTab()
    for i in range(len(origTab)):
      value = origTab[i]
      name = value[0]
      if title == name:
	url = value[1]
    #log.info(url)
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
    #log.info(titles)
    return titles
    
    
  def getPartURL(self, key, title):
    url = ''
    table = self.getPartsTab(self.getSerialURL(title))
    for i in range(len(table)):
      value = table[i]
      name = value[3]
      #log.info(name + ' < jest w > ' + key)
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
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('<div style=".+?" onclick="(.+?)"></div>').findall(link)
    if len(match) == 1:
      fLink = match[0].split('\'')
      fl = str(fLink[1])
    elif len(match) > 1:
      valTab = []
      strTab = []
      for i in range(len(match)):
	a = i + 1
	fLink = match[i].split('\'')
	strTab.append('Film ' + str(a))
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
      d.ok('Brak linku do filmu', 'Przepraszamy, ale w tej chwili nie możemy wyświetlić', 'Ci pełnej tego wersji filmu.')
      fl = 'None'
    return fl


  def videoMovieLink(self, url):
    link = self.getMovieURLFalse(url)
    if link != 'None':
      req = urllib2.Request(link)
      req.add_header('User-Agent', HOST)
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      #match = re.compile('<param name="movie" value="(.+?)"></param>').findall(link)
      match = re.compile('<param name="movie" value="(.+?)">').findall(link)
      log.info('match: ' + str(match))
      if len(match) > 0:
	p = match[0].split('=')
	l = p[1].split('&')
	log.info(str(l[0]))
	mega = megavideo
	nUrl = mega.Megavideo(MEGAVIDEO_MOVIE_URL + l[0])
	#log.info(nUrl)
	return nUrl


  def getUnlimitVideoLink(self, url):
    linkVideo = ''
    link = self.getMovieURLFalse(url)
    log.info('link: ' + link)
    if link != 'None':
      req = urllib2.Request(link)
      req.add_header('User-Agent', HOST)
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      #match = re.compile('<param name="movie" value="(.+?)"></param>').findall(link)
      match = re.compile('<param name="movie" value="(.+?)">').findall(link)
      #log.info('match: ' + str(match))
      if len(match) > 0:
	cw = cacaoweb.CacaoWeb()
	cw.runApp()
	p = match[0].split('=')
	l = p[1].split('&')
	linkVideo = STREAM_LINK + str(l[0])
	#log.info(str(linkVideo))
    return linkVideo
    
    
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
    #tabURL = link.replace('\t', '').split('\n')
    tabURL = link.replace('\n', '').split('<p class="separator_h_5">')
    for line in tabURL:
      expr = re.match(r'^.+?<img class="link_img" src="(.+?)" title=".+?" alt=".+?" /></a>.+?</div>.+?<p class="h2"><a href=".+?" title=">.+?">(.+?)</a></p>.+?<p>(.+?)<a href="(.+?)" title=".+?">.+?</a></p>', line, re.M|re.I)
      if expr:
	#log.info('1: ' + expr.group(2))
	strTab.append(expr.group(1))
	strTab.append(expr.group(2))
	strTab.append(expr.group(3))
	strTab.append(expr.group(4))
	valTab.append(strTab)
	strTab = []
    #log.info(str(valTab))
    return valTab


  def getMovieSearchNames(self, text):
    origTab = self.searchTab(text)
    return self.getMovieNamesTab(origTab)
    
  
      