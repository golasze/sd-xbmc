# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import traceback

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, Parser, urlparser, pCommon, Navigation, Errors

log = pLog.pLog()

dbg = ptv.getSetting('default_debug')
dstpath = ptv.getSetting('default_dstpath')

SERVICE = 'kinomaniak'
MAINURL = 'http://www.kinomaniak.tv'
LOGOURL = os.path.join(ptv.getAddonInfo('path'), "images/") + SERVICE + '.png'

SEARCH_URL = MAINURL + '/szukaj?'
LIST_URL = MAINURL + '/filmy?'

SERVICE_MENU_TABLE = {1: "Kategorie Filmowe",
		      2: "Ostatnio dodane",
		      3: "Najwyżej ocenione",
		      4: "Najczęściej oceniane",
		      5: "Najczęściej oglądane",
		      6: "Ulubione",
		      7: "Najnowsze",
		      #
		      10: "Szukaj",
		      11: "Historia Wyszukiwania"
		      }

class Kinomaniak:

    def __init__(self):
	log.info('Loading ' + SERVICE)
	self.parser = Parser.Parser()
	self.up = urlparser.urlparser()
	self.cm = pCommon.common()
	self.history = pCommon.history()
	self.navigation = Navigation.VideoNav()
	self.chars = pCommon.Chars()
	self.exception = Errors.Exception()


    def setTable(self):
	return SERVICE_MENU_TABLE


    def listsMainMenu(self, table):
	for num, val in table.items():
	    self.addDir(SERVICE, 'main-menu', val, '', '', '', LOGOURL, True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getCategoryTab(self, url):   
	strTab = []
	valTab = []
	query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    data = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
	match = re.compile('<li id="c_(\d+)"><a href="(?:.+?)">(.+?)<span>(.+?)</span></a>').findall(data)
	if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(value[0])
		strTab.append(value[1] + value[2])	
		valTab.append(strTab)
		strTab = []
	    valTab.sort(key = lambda x: x[1])
	return valTab


    def listsCategoriesMenu(self, table):
	for i in range(len(table)):
	    value = table[i]
	    self.addDir(SERVICE, 'category', value[0], value[1], '', '', '', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getFilmTab(self, url, category, page):
	strTab = []
	valTab = []
	query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	data = self.cm.getURLRequestData(query_data)
	#data = self.cm.requestData(url)
	matchAll = re.compile('<div class="filtered-movies">(.+?)<hr />(?:\s+)</div>', re.S).findall(data);
	match = re.compile('<img src="(.+?)" alt="" width="90" height="90">').findall(str(matchAll[0]))
	if len(match) > 0:
	    img = match
	else:
	    img = []
	match = re.compile('<a class="en" href="(.+?)">(.+?)</a>').findall(str(matchAll[0]))
	if len(match) > 0:
	    for i in range(len(match)):
		value = match[i]
		strTab.append(img[i].replace('small.jpg', 'big.jpg').replace('_1.jpg', '_2.jpg'))
		strTab.append(MAINURL + value[0])
		strTab.append(value[1])	
		valTab.append(strTab)
		strTab = []
	match = re.compile('<a class="page" href="(?:.+?)">' + str(int(page) + 1)  + '</a>').findall(data)
	if len(match) > 0:
	    strTab.append('')
	    strTab.append('')
	    strTab.append('Następna strona')
	    strTab.append(page)
	    strTab.append(category)
	    valTab.append(strTab)
	return valTab


    def getFilmTable(self, table):
	for i in range(len(table)):
	    value = table[i]
	    title = value[2].replace("&#039;", "'").replace('&amp;', '&')
	    if value[2] != 'Następna strona':
		self.addDir(SERVICE, 'playSelectedMovie', '', title, '', value[1], value[0], True, False)
	    else:
		page = str(int(value[3]) + 1)
		category = value[4]
		self.addDir(SERVICE, 'category', category, value[2], '', page, '', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def setLinkTable(self, host, url):
	strTab = []
	strTab.append(host)
	strTab.append(url)
	return strTab


    def getItemTitles(self, table):
	out = []
	for i in range(len(table)):
	    value = table[i]
	    out.append(value[0])
	return out 


    def listsHistory(self, table):
	for i in range(len(table)):
	    if table[i] <> '':
		self.addDir(SERVICE, table[i], 'history', table[i], 'None', LOGOURL, 'None', True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchTable(self, table):
	for i in range(len(table)):
	    value = table[i]
	    title = value[2].replace("&#039;", "'").replace('&amp;', '&')
	    if re.search('/seriale/', value[1]) and not re.search('s\d+e\d+$', value[1]):
		self.addDir(SERVICE, 'getEpisodes', 'history', title, '', value[1], value[0], True, False)
	    else:
		self.addDir(SERVICE, 'playSelectedMovie', 'history', title, '', value[1], value[0], True, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def searchInputText(self):
	text = None
	k = xbmc.Keyboard()
	k.doModal()
	if (k.isConfirmed()):
	    text = k.getText()
	    self.history.addHistoryItem(SERVICE, text)
	return text


    def searchTab(self, url, text):
	strTab = []
	valTab = []
	idxTab = []
	if text == None or str(text) == '':
	    return valTab
	sUrl = url + 'q=' + str(text)
	query_data = { 'url': sUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    link = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
	match = re.compile('<img src="(.+?)" alt="(.+?)" title="(.+?)" height="90" width="90"').findall(link)
	if len(match) > 0:
	    img = match
	else:
	    img = []
	match = re.compile('<div class="result">\s+<a href="(.+?)"', re.S).findall(link)
	if len(match) > 0:
	    for i in range(len(match)):
		if not match[i] in idxTab:
		    idxTab.append(match[i])
		    strTab.append(img[i][0].replace('small.jpg', 'big.jpg').replace('_1.jpg', '_2.jpg'))
		    strTab.append(MAINURL + match[i])
		    strTab.append(img[i][2])
		    valTab.append(strTab)
		    strTab = []
	return valTab


    def searchEpisodesTab(self, url):
	strTab = []
	valTab = []
	query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    link = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
	match = re.compile('<a rel="poster" href="(.+?)">').findall(link)
	print match
	if len(match) > 0:
	    img = match
	else:
	    img = [];
	match = re.compile('<a style="color: #FFAE00; line-height: 2em;" href="(.+?)"><span style="color: white;">(.+?)<\/span>(.+?)<\/a>').findall(link)
	if len(match) > 0:
	    for i in range(len(match)):
		strTab.append(img[0])
		strTab.append(MAINURL + match[i][0])
		strTab.append(match[i][1] + match[i][2])
		valTab.append(strTab)
		strTab = []
	return valTab

    def getHostTable(self,url):
	valTab = []
	videoID = ''
	query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	try:
	    link = self.cm.getURLRequestData(query_data)
	except Exception, exception:
	    traceback.print_exc()
	    self.exception.getError(str(exception))
	    exit()
	match = re.compile('<div id=".*">([\\\\x0-9a-f\']+)</div>').findall(link)
	matchFiltered = []
	for i in range(len(match)):
	    exec 'decodedStr = u"%s".encode("utf-8")' % (match[i].replace("'",''))
	    if re.search('(.*)getplayer(.*)&limit(.*)', decodedStr):
		matchFiltered.append(decodedStr)
	match = matchFiltered
	if len(match) > 0:
	    for i in range(len(match)):
		query_data = { 'url': MAINURL + match[i], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
		try:
		    link = self.cm.getURLRequestData(query_data)
		except Exception, exception:
		    traceback.print_exc()
		    self.exception.getError(str(exception))
		    exit()
		link = re.sub('<!--(.+?)-->', '', link)
		data = link.replace('putlocker.com/file', 'putlocker.com/embed')
		match2 = re.compile('http://(.+?)["\\r]').findall(data)
		if len(match2) > 0:
		    for i in range(len(match2)):
			match2[i] = 'http://' + match2[i]
			valTab.append(self.setLinkTable(self.up.getHostName(match2[i], True), match2[i]))
			valTab.sort(key = lambda x: x[0])

	d = xbmcgui.Dialog()
	item = d.select("Wybór filmu", self.getItemTitles(valTab))
	if item != -1:
	    videoID = str(valTab[item][1])
	    log.info('mID: ' + videoID)
	return videoID


    def addDir(self, service, name, category, title, plot, page, iconimage, folder = True, isPlayable = True):
	u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&page=" + urllib.quote_plus(page)
	if name == 'main-menu':
	    title = category
	if iconimage == '':
	    iconimage = "DefaultVideo.png"
	liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if isPlayable:
	    liz.setProperty("IsPlayable", "true")
	liz.setInfo( type="Video", infoLabels={ "Title": title, "Plot": plot } )
	if dstpath != "None" or not dstpath and name == 'playSelectedMovie':
	    if dbg == 'true':
		#log.info('addDir() -> service: ' + service)
		#log.info('addDir() -> name: ' + name)
		#log.info('addDir() -> category: ' + category)
		#log.info('addDir() -> title: ' + title)
		#log.info('addDir() -> plot: ' + plot)
		log.info('addDir() -> page: ' + page)
		#log.info('addDir() -> iconimage: ' + iconimage)
		#log.info('addDir() -> folder: ' + str(folder))
		#log.info('addDir() -> isPlayable: ' + str(isPlayable))
		#log.info('addDir() -> dstpath: ' + os.path.join(dstpath, SERVICE))
	    cm = self.navigation.addVideoContextMenuItems({ 'service': SERVICE, 'title': urllib.quote_plus(self.chars.replaceChars(title)), 'url': urllib.quote_plus(page), 'path': os.path.join(dstpath, SERVICE) })
	    liz.addContextMenuItems(cm, replaceItems=False)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)


    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title):
	ok=True
	if videoUrl == '':
	    d = xbmcgui.Dialog()
	    d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
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
	name = self.parser.getParam(params, "name")
	title = self.parser.getParam(params, "title")
	category = self.parser.getParam(params, "category")
	page = self.parser.getParam(params, "page")
	icon = self.parser.getParam(params, "icon")
	link = self.parser.getParam(params, "url")
	vtitle = self.parser.getParam(params, "vtitle")
	service = self.parser.getParam(params, "service")
	action = self.parser.getParam(params, "action")
	path = self.parser.getParam(params, "path")

	if dbg == 'true':
	    #log.info ('handleService() -> name: ' + str(name))
	    #log.info ('handleService() -> title: ' + str(title))
	    #log.info ('handleService() -> category: ' + str(category))
	    log.info ('handleService() -> page: ' + str(page))
	    #log.info ('handleService() -> icon: ' + str(icon))
	    #log.info ('handleService() -> link: ' + str(link))
	    #log.info ('handleService() -> vtitle: ' + str(vtitle))
	    #log.info ('handleService() -> service: ' + str(service))
	    #log.info ('handleService() -> action: ' + str(action))
	    #log.info ('handleService() -> path: ' + str(path))

	if str(page) == 'None' or page == '': page = 1

	if name == None:
	    self.listsMainMenu(SERVICE_MENU_TABLE)
	elif category == self.setTable()[1]:
	    self.listsCategoriesMenu(self.getCategoryTab(MAINURL + '/filmy'))
	elif category == self.setTable()[2]:
	    self.getFilmTable(self.getFilmTab(LIST_URL + '&page=' + str(page), category, page))
	elif category == self.setTable()[3]:
	    self.getFilmTable(self.getFilmTab(LIST_URL + '&sort=score&order=desc&page=' + str(page), category, page))
	elif category == self.setTable()[4]:
	    self.getFilmTable(self.getFilmTab(LIST_URL + '&sort=votes&order=desc&page=' + str(page), category, page))
	elif category == self.setTable()[5]:
	    self.getFilmTable(self.getFilmTab(LIST_URL + '&sort=visits&order=desc&page=' + str(page), category, page))
	elif category == self.setTable()[6]:
	    self.getFilmTable(self.getFilmTab(LIST_URL + '&sort=favourites&order=desc&page=' + str(page), category, page))
	elif category == self.setTable()[7]:
	    self.getFilmTable(self.getFilmTab(LIST_URL + '&sort=year&order=desc&page=' + str(page), category, page))
	elif category == self.setTable()[10]:
	    text = self.searchInputText()
	    self.getSearchTable(self.searchTab(SEARCH_URL, text))
	elif category == self.setTable()[11]:
	    t = self.history.loadHistoryFile(SERVICE)
	    self.listsHistory(t)

	if category == 'history' and name == 'getEpisodes':
	    self.getSearchTable(self.searchEpisodesTab(page))
	elif category == 'history' and name != 'playSelectedMovie':
	    self.getSearchTable(self.searchTab(SEARCH_URL, name))

	if category > 0:
	    if category.isdigit() == True:
		self.getFilmTable(self.getFilmTab(LIST_URL + '&c=' + category + '&page=' + str(page), category, page))

	if name == 'playSelectedMovie':
	    url = self.getHostTable(page)
	    if url != '':
		linkVideo = self.up.getVideoLink(url)
		if linkVideo != False:
		    self.LOAD_AND_PLAY_VIDEO(linkVideo, title)
		else:
		    d = xbmcgui.Dialog()
		    d.ok('Brak linku', SERVICE + ' - przepraszamy, chwilowa awaria.', 'Zapraszamy w innym terminie.')
	    else:
		self.getSearchTable(self.searchTab(SEARCH_URL, title))

	if service == SERVICE and action == 'download' and link != '':
	    self.cm.checkDir(os.path.join(dstpath, SERVICE))
	    if dbg == 'true':
		log.info(SERVICE + ' - handleService()[download][0] -> title: ' + urllib.unquote_plus(vtitle))
		log.info(SERVICE + ' - handleService()[download][0] -> url: ' + urllib.unquote_plus(link))
		log.info(SERVICE + ' - handleService()[download][0] -> path: ' + path)	
	    if urllib.unquote_plus(link).startswith('http://'):
		urlTempVideo = self.getHostTable(urllib.unquote_plus(link))
		linkVideo = self.up.getVideoLink(urlTempVideo)
		if dbg == 'true':
		    log.info(SERVICE + ' - handleService()[download][1] -> title: ' + urllib.unquote_plus(vtitle))
		    log.info(SERVICE + ' - handleService()[download][1] -> temp url: ' + urlTempVideo)
		    log.info(SERVICE + ' - handleService()[download][1] -> url: ' + linkVideo)
		if linkVideo != False:
		    if dbg == 'true':
			log.info(SERVICE + ' - handleService()[download][2] -> title: ' + urllib.unquote_plus(vtitle))
			log.info(SERVICE + ' - handleService()[download][2] -> url: ' + linkVideo)
			log.info(SERVICE + ' - handleService()[download][2] -> path: ' + path)
		    import downloader
		    dwnl = downloader.Downloader()
		    dwnl.getFile({ 'title': urllib.unquote_plus(vtitle), 'url': linkVideo, 'path': path })
