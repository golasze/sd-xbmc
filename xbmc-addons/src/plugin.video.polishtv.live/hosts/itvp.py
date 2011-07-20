# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc


BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()

mainUrl = 'http://www.tvp.pl/vod'

ITVP_MAIN_MENU_TABLE = { 1: "Seriale",
		   2: "Filmy fabularne",
		   3: "Dokumenty",
		   4: "Archiwa",
		   5: "Najczęściej oglądane",
		   6: "Wyszukaj" }

ITVP_SERIAL_MENU_TABLE = { 1: "Archiwalne",
			   2: "Obyczajowe",
			   3: "Komedie",
			   4: "Sensacja" }

ITVP_MOVIES_MENU_TABLE = { 1: "Filmy darmowe",
			   2: "Klasyka",
			   3: "Komedia",
			   4: "Romans",
			   5: "Dramat",
			   6: "Obyczajowe",
			   7: "Inne" }
			   
ITVP_DOC_MENU_TABLE = { 1: "Polityka",
			2: "Religia i wiara",
			3: "Sztuka",
			4: "Historia",
			5: "Ludzie",
			6: "Wykluczeni",
			7: "Społeczeństwo" }
			
ITVP_ARCH_MENU_TABLE = { 1: "Archiwizja",
			 2: "Tak było",
			 3: "Rocznice i wydarzenia" }
			 

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
PAGE_MOVIES = 10
DUB_LINK = mainUrl + '/tag,lektor.html'
SUB_LINK = mainUrl + '/tag,napisy.html'
STREAM_LINK = 'http://127.0.0.1:4001/megavideo/megavideo.caml?videoid='


class iTVP:
  def __init__(self):
    log.info("Starting iTVP")
    
    
  def setMainMenu(self):
    return ITVP_MAIN_MENU_TABLE
    

  def setSerialsMenu(self):
    return ITVP_SERIAL_MENU_TABLE
    
  
  def setMoviesMenu(self):
    return ITVP_MOVIES_MENU_TABLE
    
    
  def setDocumentsMenu(self):
    return ITVP_DOC_MENU_TABLE
    
    
  def setArchivesMenu(self):
    return ITVP_ARCH_MENU_TABLE


  def getMenuTable(self, table):
    nTab = []
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def searchInputText(self):
    text = None
    k = xbmc.Keyboard()
    k.doModal()
    if (k.isConfirmed()):
      text = k.getText()
    return text
    
    
  def getMovieTable(self, url, key):
    strTab = []
    valTab = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('<div class="item"><a href="(.+?)"><span class="img"><img alt=".+?" src="(.+?)"/></span><strong>(.+?)</strong><span>(.+?)</span></a><div class="clr"></div></div>').findall(link)
    if len(match) > 0:
      #log.info(str(match))
      for i in range(len(match)):
	#log.info(match[i])
	if key in match[i][0]:
	  strTab.append(match[i][1])
	  strTab.append(match[i][2])
	  strTab.append(match[i][3])
	  strTab.append(match[i][0])
	  valTab.append(strTab)
	  strTab = []
    #log.info(str(valTab))
    return valTab


  def showFreeMoviesTitles(self):
    titleTab = []
    url = mainUrl + '/filmy-fabularne/filmy-za-darmo'
    key = 'filmy-za-darmo'
    tab = self.getMovieTable(url, key)
    for i in range(len(tab)):
      value = tab[i]
      titleTab.append(value[1])
    return titleTab


  def getFreeMovieURL(self, title):
    link = ''
    url = mainUrl + '/filmy-fabularne/filmy-za-darmo'
    key = 'filmy-za-darmo'
    tab = self.getMovieTable(url, key)
    for i in range(len(tab)):
      value = tab[i]
      if title in value[1]:
	link = value[3]
    return link
    

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

    
  def getMovieFalseURL(self, url):
    fl = None
    if url.startswith('http://'):
      req = urllib2.Request(url)
      req.add_header('User-Agent', HOST)
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      match1 = re.compile('<span class=".+?"><a href="(.+?)"><img alt=".+?" src=".+?" /><span class="seeWideo">').findall(link)
      match2 = re.compile('<div class="item"><a href="(.+?)"><span class="img"><img alt=".+?" src=".+?"/></span><strong>.+?</strong><span>(.+?)<br/></span></a>').findall(link)
      if (len(match1) == 1) and (len(match2) == 0):
	fl = match1[0]
      elif len(match2) > 1:
	valTab = []
	strTab = []
	for i in range(len(match2)):
	  strTab.append(str(match2[i][1]))
	  strTab.append(str(match2[i][0]))
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


#  def videoMovieLink(self, url):
#    nUrl = self.getMovieFalseURL(url)
#    log.info('link: ' + str(nUrl))
#    if nUrl != 'None':
#      cookiejar = cookielib.LWPCookieJar()
#      cookiejar = urllib2.HTTPCookieProcessor(cookiejar) 
#      opener = urllib2.build_opener(cookiejar)
#      urllib2.install_opener(opener)
#      values = { 'aaa' : 'aaa' }
#      headers = { 'User-Agent' : HOST }
#      data = urllib.urlencode(values)
#      req = urllib2.Request(nUrl, data, headers)
      #req.add_header('User-Agent', HOST)
#      response = urllib2.urlopen(req)
#      link = response.read()
#      log.info(link)
#      response.close()
      #match = re.compile('<param name="movie" value="(.+?)"></param>').findall(link)
#      match = re.compile('<param name="initParams" value=".+?media=(.+?),vortal_id=.+?">').findall(link)
#      log.info('match: ' + str(match))
#      if len(match) == 1:
#	log.info(str(match[0][0]))
#	tUrl = str(match[0][0])
#	log.info(tUrl)
#	return tUrl
	
	
  def videoMovieLink(self, url):
    nUrl = self.getMovieFalseURL(url)
    log.info('link: ' + str(nUrl))
    if nUrl != 'None':
      req = urllib2.Request(nUrl)
      req.add_header('User-Agent', HOST)
      response = urllib2.urlopen(req)
      link = response.read()
      log.info(link)
      response.close()
      #match = re.compile('<param name="movie" value="(.+?)"></param>').findall(link)
      match = re.compile('<param name="initParams" value=".+?media=(.+?),vortal_id=.+?">').findall(link)
      log.info('match: ' + str(match))
      if len(match) == 1:
	log.info(str(match[0][0]))
	tUrl = str(match[0][0])
	log.info(tUrl)
	return tUrl


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
		mm = self.listsMenu(self.getMenuTable(self.setMainMenu()), "Wybór typu")
		if mm == 'Seriale':
	  		sm = self.listsMenu(self.getMenuTable(self.setSerialsMenu()), "Wybór kategorii")
	  		if sm == 'Archiwalne':
	  			log.info('')
		  	elif sm == 'Obyczajowe':
		  		log.info('')
		  	elif sm == 'Komedie':
		  		log.info('')
		  	elif sm == 'Sensacja':
		  		log.info('')
		elif mm == 'Filmy fabularne':
			mm = self.listsMenu(self.getMenuTable(self.setMoviesMenu()), "Wybór kategorii")
	  		if mm == 'Filmy darmowe':
	  			title = self.listsMenu(self.showFreeMoviesTitles(), "Wybór tytułu")
	    		if title != '':
	    			urlLink = self.videoMovieLink(self.getFreeMovieURL(title))
		      	 	if urlLink.startswith('http://'):
				      	 self.LOAD_AND_PLAY_VIDEO(urlLink)
		elif mm == 'Dokumenty':
	  		sm = self.listsMenu(self.getMenuTable(self.setDocumentsMenu()), "Wybór kategorii")
		elif mm == 'Archiwa':
	  		sm = self.listsMenu(self.getMenuTable(self.setArchivesMenu()), "Wybór kategorii")
		elif mm == 'Najczęściej oglądane':
	  		log.info('')
		elif mm == 'Wyszukaj':
	  		text = self.searchInputText()



