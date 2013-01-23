# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math, json
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import elementtree.ElementTree as ET
try:
	from hashlib import md5
except ImportError:
	import md5

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, pCommon

log = pLog.pLog()

SERVICE = 'iplex'
COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + SERVICE +".cookie"

mainUrl = 'http://www.iplex.pl'
playerUrl = mainUrl + '/player_feed/'
sort_asc = '?o=rosnaco&f=tytul'
sort_desc = '?o=malejaco&f=tytul'
iplexplus = False

adult = ptv.getSetting('iplex_adult')

MENU_TAB = { 1: "Kategorie",
	     2: "Kolekcje",
	     3: "Kanaly",
#	     4: "Bajki", 
             5: "Szukaj" }


class IPLEX:
  def __init__(self):
	log.info('Starting ' + SERVICE)
	self.settings = settings.TVSettings()
	self.parser = Parser.Parser()
	self.common = pCommon.common()


  def listsMainMenu(self, table):
	for num, val in table.items():
		self.add('iplex', 'main-menu', val, 'None', 'None', 'None', self.videoMetadata(), True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def listsCategoriesMenu(self,category):
	query_data = { 'url': mainUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	data = self.common.getURLRequestData(query_data)
	match = re.compile('<li><a href="/' + category + '(.+?)">(.+?)</a></li>').findall(data)
	if len(match) > 0:
		for i in range(len(match)):
			url = mainUrl + '/' + category + match[i][0]
			self.add('iplex', 'sub-menu', match[i][1], 'None', 'None', url, self.videoMetadata(), True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def getSearchURL(self, key):
	url = mainUrl + '/szukaj/?q=' + urllib.quote_plus(key) + '&i='
	return url
        

  def listsItems(self, url):
	if not url.startswith("http://"):
		url = mainUrl + url
	query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	data = self.common.getURLRequestData(query_data)
	if len(data) > 0:
		#poswiadczenie pelnoletnosci
		match = re.compile('<input type="hidden" name="next" value="(.+?)"/>').findall(data)
		if len(match) > 0:
			if adult =='true':
				self.common.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
				query_data = {'url': mainUrl + '/adultagreement', 'use_host': False, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIEFILE, 'use_post': True, 'return_data': True}
				post_data = {'adult_agreement' : 'on', 'next' : match[0]}
				data = self.common.getURLRequestData(query_data, post_data)
			else:
				d = xbmcgui.Dialog()
				d.ok('Tylko dla doroslych', 'Materialy przeznaczone dla widzow dorosly.', 'Aby obejrzec film, musisz miec ukonczone 18 lat.')
		#sprawdz czy to ostatnia strona 
		lastPage = True
		match = re.compile('page=(.+?)">ostatnia strona</a>').findall(data)
		if len(match) > 0:
			lastPage = False
		data = data.replace('\n', '').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').split('class="movie"')
		for i in range(len(data)):
			#match[a][3] to blok gdzie moze znajdowac sie duration i mpaa
		        match = re.compile('<a class=".+?" href="(.+?)" title=".+?"> <img src="(.+?)" alt=".+?" /> <span class="hover sprite"></span> </a>.+?<h1><a class="title" href=".+?">(.+?)</a></h1>(.+?)<span class="title">(.+?)</span>.+?<span class="year"> <span class="label">Rok produkcji:</span> <span class="value">(.+?)</span>.+?<span class="rating"> <span class="label">Ocena:</span> <span class="value rating-desc">(.+?)</span>.+?<span class="votes">.+?<span class="value">(.+?)</span>.+?<span class="description"> <span class="label">Opis:</span><br /> <span class="value">(.+?)</span> </span> </div> </div>').findall(data[i])
			if len(match) > 0:
				for a in range(len(match)):
					time=""
					if 'liczba odcinków:' in data[i]:
						category = match[a][4]
						name = "sub-menu"
					else:
						category = "None"
						matchDuration = re.compile('<span class="duration">czas: (.+?)min</span>').findall(match[a][3])
						if len(matchDuration) > 0:
							time = matchDuration[0]
						if 'iplexplus' in data[i] and not iplexplus:
							name = 'blockPlaySelectedMovie'
						else:
							name = 'playSelectedMovie'
					#sprawdz czy jest podany mpaa
					matchAge = re.compile('<span class="age">(.+?)<span class="plus">').findall(match[a][3])
					if len(matchAge) > 0:
						mpaa = matchAge[0]
					else:
						mpaa = ""		    
					dict = self.videoMetadata(match[a][4], match[a][8], match[a][6], time, match[a][5], match[a][7], mpaa)			    
					self.add('iplex', name, category, match[a][4], match[a][1], match[a][0], dict, True, False)
		#generuj linki ">> pokaz wiecej >>"
		match = re.compile('f=tytul&page=(\d+)$').findall(url)
		if lastPage==False:
			log.info(str(match[0]))
			nextpage = str(int(match[0])+1)
			if int(match[0])<10:
				url = url[:-1] + nextpage
			else:
				url = url[:-2] + nextpage
			self.add('iplex', 'items-menu', 'None', '>> pokaz wiecej >>', 'None', url, self.videoMetadata(), True, False)
	#zmien view na "Media Info 2"
	xbmcplugin.setContent(int(sys.argv[1]),'movies')
	xbmc.executebuiltin("Container.SetViewMode(503)")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def getMovieLinksFromXML(self, url, version = None):
	valTab = []
	urlLink = 'None'
	urlXml = playerUrl + self.getMovieID(url) + '?sessionid=' + str(md5(url).hexdigest()) + '&chlck=hhi7ep&r=1321745471310'
	if(version):
		urlXml +='&version='+version
	log.info('url: ' + urlXml )
	elems = ET.parse(urllib.urlopen(urlXml)).getroot()
	mediaItems = elems.find("Media").findall("MediaItem")
	for mediaItem in mediaItems:
		media = mediaItem.attrib
		resID = media['id']
		if resID == 'M' + self.getMovieID(url):
			meta = json.loads(mediaItem.find("Text").text)
			if version == None:
				for v in set(meta['available_versions']):
					if v == meta['current_version']:
						continue
					valTab += self.getMovieLinksFromXML(url, v)
			fileSets = mediaItem.findall("FileSet")
			for fileSet in fileSets:
				resFiles = fileSet.findall("File")
				if len(resFiles) > 1:
					for resFile in resFiles:
						strTab = {}
						file = resFile.attrib
						bitrate = file['rate']
						link = file['src']
						strTab['title'] = "Film z bitrate: " + bitrate + " kbps - " + meta['current_version']
						strTab['link']  = link
						valTab.append(strTab)             
	return valTab


  def selectUrl(self, urls):
	if len(urls) == 1:
		return urls[0]['link'];
	d = xbmcgui.Dialog()
	item = d.select("Wybierz wersję", [e['title'] for e in urls] )
	if item < 0:
		return None
	return urls[item]['link']


  def getMovieID(self, url):
	id = 0
	tabID = url.split(',')
	if len(tabID) > 0:
		id = tabID[1]
	return id


  def searchInputText(self):
	text = None
	k = xbmc.Keyboard()
	k.doModal()
	if (k.isConfirmed()):
		text = k.getText()
	return text


  def videoMetadata(self, title = "", plot = "", rating = 0, duration = "", year = 0, votes = "", mpaa = ""):
	#sprawdz czy year i rating sa numerycznymi wartosciami
	if self.common.isNumeric(year):
		year = int(year)
	if self.common.isNumeric(rating):
		rating = float(rating)
	plot = plot.replace("<br />","").replace("<br/>","").replace("<br>","")    
	details = {'title'    : title,
		   'plot'     : plot,
		   'rating'   : rating,
		   'duration' : duration,
		   'year'     : year,
		   'votes'    : votes,
		   'mpaa'     : mpaa}
	return details    

    
  def add(self, service, name, category, title, iconimage, url, metadata, folder = True, isPlayable = True):
	u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
	#log.info(str(u))
	if name == 'main-menu' or name == 'sub-menu':
		title = category 
	if iconimage == '':
		iconimage = "DefaultVideo.png"
	liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if isPlayable:
		liz.setProperty("IsPlayable", "true")
	liz.setInfo('video', metadata )
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)


  def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon):
	ok=True
	if videoUrl == '':
		d = xbmcgui.Dialog()
		d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
		return False
	liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": title, } )
	try:
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(videoUrl, liz)
	except:
		d = xbmcgui.Dialog()
		d.ok('Blad przy przetwarzaniu.', 'Najprawdopodobniej brak wsparcia vividas w ffmpeg.')        
	return ok


  def handleService(self):
	params = self.parser.getParams()
	name = self.parser.getParam(params, "name")
	category = self.parser.getParam(params, "category")
	url = self.parser.getParam(params, "url")
	title = self.parser.getParam(params, "title")
	icon = self.parser.getParam(params, "icon")
	if name == None:
		self.listsMainMenu(MENU_TAB)
	elif name == 'main-menu' and category == 'Kategorie':
		self.listsCategoriesMenu('kategorie')
	elif name == 'main-menu' and category == 'Kolekcje':
		self.listsCategoriesMenu('kolekcje')
	elif name == 'main-menu' and category == 'Kanaly':
		self.listsCategoriesMenu('kanaly')
	elif name == 'main-menu' and category == "Szukaj":
		key = self.searchInputText()
		self.listsItems(self.getSearchURL(key))
	elif name == 'sub-menu' and category != 'None':
		destUrl = url + sort_asc + '&page=1'
		self.listsItems(destUrl)
	elif name == 'items-menu':
		self.listsItems(url)

	if name == 'playSelectedMovie':
		url = self.selectUrl(self.getMovieLinksFromXML(url))
		if url:
			self.LOAD_AND_PLAY_VIDEO(url, title, icon)
	elif name == 'blockPlaySelectedMovie':
		dialog = xbmcgui.Dialog()
		dialog.ok("IPLEX PLUS", "Ten film nie będzie odtwarzany.", "Brak obsługi IPLEX-PLUS.")
        
  
