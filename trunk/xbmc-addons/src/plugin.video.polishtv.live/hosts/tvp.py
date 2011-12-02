# -*- coding: utf-8 -*-
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcplugin
from datetime import datetime

import elementtree.ElementTree as ET
from xml.dom.minidom import parseString

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings

log = pLog.pLog()

TVP_MAIN_MENU_TABLE = [
	"Przegapiłes|xml|http://www.tvp.pl/pub/stat/missed?src_id=1885&object_id=-1&offset=-1&dayoffset=-1&rec_count=12",
	"Najcześciej oglądane|xml|http://www.tvp.pl/pub/stat/videolisting?src_id=1885&object_id=929547&object_type=video&child_mode=SIMPLE&rec_count=12",
	"Kraków|xml|http://www.tvp.pl/pub/stat/videolisting?src_id=1885&object_id=929711&object_type=video&child_mode=SIMPLE&rec_count=12",
	"Teleexpress|html|http://www.tvp.info/teleexpress/wideo/"
]

PAGE_MOVIES = 10
NEXT_PAGE_HTML = '?sort_by=POSITION&sort_desc=false&start_rec=6'

HOST = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
HANDLE = int(sys.argv[1])

class tvp:
	mode = 0

	def __init__(self):
		log.info("Starting TVP.INFO")
		self.settings = settings.TVSettings()

	def addDir(self,name,url,mode,category,iconimage):
		u = sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&url="+urllib.quote_plus(url)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

	def addVideoLink(self,name,url,mode,iconimage):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
		return ok

	def listsCategories(self, mainList):
		for item in mainList:
			xbmcplugin.setContent(HANDLE, 'albums')
			print "test[2]: " + str(item)
			value = item.split('|')
			self.addDir(value[0],value[2],self.mode,value[1],'')

		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	def getVideoListXML(self):
		print "test[3]: " + self.url
		elems = ET.parse(urllib.urlopen(self.url)).getroot()
		epgItems = elems.findall("epg_item")
		if not epgItems:
			epgItems = elems.findall("directory_stats/video")
		if not epgItems:
			epgItems = elems.findall("video")

		print "test[6]: " + str(len(epgItems))

		findVideo=False
		for epgItem in epgItems:
			title = epgItem.find("title").text.encode('utf-8')
			iconUrl = ''
			videoUrl = ''
			iconFileNode = epgItem.find('video/image')
			if not iconFileNode:
				iconFileNode = epgItem.find('image')

			if iconFileNode:
				iconFileName = iconFileNode.attrib['file_name']
				iconFileName = iconFileName.split('.')
				iconUrl = 'http://s.v3.tvp.pl/images/6/2/4/uid_%s_width_700.jpg' % iconFileName[0]
				print "test[4]: " + iconUrl

			videoNode = epgItem.find('video/video_format')
			if not videoNode:
				videoNode = epgItem.find('video_format')

			if videoNode:
				videoUrl = videoNode.attrib['temp_sdt_url']

			if videoUrl != '':
				self.addVideoLink(title,videoUrl,self.mode,iconUrl)
				print "test[4]: " + title + ", " + iconUrl + ", " + videoUrl
				findVideo=True
		if findVideo:
			xbmcplugin.endOfDirectory(int(sys.argv[1]))
	def getVideoListHTML(self):
		print "test[5]: " + self.url
		findVideo=False
		req = urllib2.Request(self.url)
		req.add_header('User-Agent', HOST)
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		allVideos = re.compile('<div class="videoBox invert">(.+?)</div>').findall(link)
		for video in allVideos:
			xbmcplugin.setContent(HANDLE, 'episodes')
			iconUrl = re.compile('src="(.+?)"').findall(video)
			videoUrl = re.compile('redir\(\'(.+?)\'\);').findall(video)
			videoUrl = videoUrl[0].split('/')
			videoId = videoUrl[len(videoUrl)-1]
			videoInfoUrl = 'http://www.tvp.pl/pub/stat/videolisting?src_id=1885&object_id=' + str(videoId)
			videoDoc = ET.parse(urllib.urlopen(videoInfoUrl)).getroot()
			title = videoDoc.find("video/title").text.encode('utf-8')
			videoUrlNode = videoDoc.find("video/video_format")
			videoUrl = ''
			if videoUrlNode:
				videoUrl = videoUrlNode.attrib['temp_sdt_url']

			if videoUrl != '':
				self.addVideoLink(title,videoUrl,self.mode,iconUrl[0])
				findVideo=True
		if findVideo:
			xbmcplugin.endOfDirectory(int(sys.argv[1]))


	def handleService(self):
		self.name = str(self.settings.paramName)
		self.title = str(self.settings.paramTitle)
		self.category = str(self.settings.paramCategory)
		self.mode = str(self.settings.paramMode)
		self.url = str(self.settings.paramURL)
		print ""
		print "test[1]: " + self.mode #sys.argv[2]
		if self.name == 'None':
			self.listsCategories(TVP_MAIN_MENU_TABLE)
		elif self.name != 'None' and self.category == 'xml':
			self.getVideoListXML()
		elif self.name != 'None' and self.category == 'html':
			self.getVideoListHTML()

