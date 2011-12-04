# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re
import xbmcgui, xbmc, xbmcplugin

import elementtree.ElementTree as ET
from xml.dom.minidom import parseString

import pLog, settings

log = pLog.pLog()

TVP_MAIN_MENU_TABLE = [
    "Przegapiłes|xml|http://www.tvp.pl/pub/stat/missed?src_id=1885&object_id=-1&offset=-1&dayoffset=-1&rec_count=12",
    "Najcześciej oglądane|xml|http://www.tvp.pl/pub/stat/videolisting?src_id=1885&object_id=929547&object_type=video&child_mode=SIMPLE&rec_count=12",
    "Teleexpress|html|http://www.tvp.info/teleexpress/wideo/",
    "Wiadomości|html|http://tvp.info/wiadomosci/wideo",
    "Panorama|html|http://tvp.info/panorama/wideo",
    "Makłowicz w podróży|xml|http://www.tvp.pl/pub/stat/videolisting?object_id=1364&with_subdirs=true&sort_desc=true&rec_count=12&sort_by=RELEASE_DATE&child_mode=SIMPLE",
    "Kraków - najczęściej oglądane|xml|http://www.tvp.pl/pub/stat/videolisting?src_id=1885&object_id=929711&object_type=video&child_mode=SIMPLE&rec_count=12&sort_by=RELEASE_DATE&sort_desc=true",
    "Kronika|xml|http://www.tvp.pl/pub/stat/videolisting?object_id=1277349&object_type=video&child_mode=SIMPLE&rec_count=12&sort_by=RELEASE_DATE&sort_desc=true",
]

PAGE_MOVIES = 10
NEXT_PAGE_HTML = '?sort_by=POSITION&sort_desc=false&start_rec=6'

HOST = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
HANDLE = int(sys.argv[1])

class tvp:
    mode = 0
    #__settings__ = sys.modules[ "__main__" ].ptv
    __moduleSettings__ =  settings.TVSettings()

    def __init__(self):
        log.info("Starting TVP.INFO")

    def addDir(self,name,url,mode,category,iconimage):
        u = sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&url="+urllib.quote_plus(url)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

    def addVideoLink(self,prop,url,iconimage,listsize=0):
        ok=True
        if not 'description' in prop:
            prop['description'] = ''
        if not 'time' in prop:
            prop['time'] = 0
        if not 'aired' in prop:
            prop['aired'] = ''
        if not 'overlay' in prop:
            prop['overlay'] = 0
        if not 'TVShowTitle' in prop:
            prop['TVShowTitle'] = ''
        if not 'episode' in prop:
            prop['episode'] = 0


        liz=xbmcgui.ListItem(prop['title'], iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={
            "Title": prop['title'],
            "Plot": prop['description'],
            "Duration": str(prop['time']/60),
            "Premiered": prop['aired'],
            "Overlay": prop['overlay'],
            "TVShowTitle" : prop['TVShowTitle'],
            "Episode" : prop['episode']
        } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False,totalItems=listsize)
        return ok

    def listsCategories(self, mainList):
        for item in mainList:
            xbmcplugin.setContent(HANDLE, 'albums')
            #print "test[2]: " + str(item)
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
            epgItems = elems.findall("directory_standard/video")
        if not epgItems:
            epgItems = elems.findall("video")


        print "test[6]: " + str(len(epgItems))

        findVideo=False
        listsize = len(epgItems)
        for epgItem in epgItems:
            prop = {'title':  epgItem.find("title").text.encode('utf-8') }
            if epgItem.attrib['hptitle'] <> '':
                prop['title'] = epgItem.attrib['hptitle'].encode('utf-8')
            iconUrl = ''
            videoUrl = ''
            iconFileNode = epgItem.find('video/image')
            if not iconFileNode:
                iconFileNode = epgItem.find('image')

            if iconFileNode:
                iconFileName = iconFileNode.attrib['file_name']
                iconFileName = iconFileName.split('.')
                iconUrl = 'http://s.v3.tvp.pl/images/6/2/4/uid_%s_width_700.jpg' % iconFileName[0]
                iconTitle = iconFileNode.find('title').text.encode('utf-8')
                if len(iconTitle) > 4 and iconTitle <> prop['title']:
                    if iconTitle <> 'zdjecie domyślne' and iconTitle <> 'image' and iconTitle <> 'obrazek':
                        iconTitle = iconTitle.split(',')[0]
                        prop['title'] = iconTitle + " - " + prop['title']
                #print "test[4]: " + iconUrl

            videManioNode = epgItem.find('video')
            if videManioNode:
                #print "test[7]: " + ET.dump(videoNode)
                # 2400 00:41:28  2488
                # 2100 00:35:50  2150
                prop['time'] = int(videManioNode.attrib['duration'])
                iconTitle = videManioNode.find('title').text.encode('utf-8')
                if len(iconTitle) > 4 and iconTitle <> prop['title']:
                    if iconTitle <> 'zdjecie domyślne' and iconTitle <> 'image' and iconTitle <> 'obrazek':
                        iconTitle = iconTitle.split(',')[0]
                        prop['title'] = prop['title'] + " - " + iconTitle

            videoNode = epgItem.find('video/video_format')
            if not videoNode:
                videoNode = epgItem.find('video_format')

            if videoNode:
                videoUrl = videoNode.attrib['temp_sdt_url']

            if videoUrl != '':
                if self.watched(videoUrl):
                    prop['overlay'] = 7

                self.addVideoLink(prop,videoUrl,iconUrl,listsize)
                #print "test[4]: " + prop['title'] + ", " + iconUrl + ", " + videoUrl
                findVideo=True
        if findVideo:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
    def getVideoListHTML(self):
        #print "test[5]: " + self.url
        findVideo=False
        req = urllib2.Request(self.url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        allVideos = re.compile('<div class="videoBox invert">(.+?)</div>').findall(link)
        if not allVideos:
            allVideos = re.compile('<div class="videoBox">(.+?)</div>').findall(link)

        listsize = len(allVideos)
        xbmcplugin.setContent(HANDLE, 'episodes')

        for video in allVideos:
            iconUrl = re.compile('src="(.+?)"').findall(video)
            videoUrl = re.compile('redir\(\'(.+?)\'\);').findall(video)
            videoUrl = videoUrl[0].split('/')
            videoId = videoUrl[len(videoUrl)-1]
            videoInfoUrl = 'http://www.tvp.pl/pub/stat/videolisting?src_id=1885&object_id=' + str(videoId)
            videoDoc = ET.parse(urllib.urlopen(videoInfoUrl)).getroot()
            prop = {'title' : videoDoc.find("video/title").text.encode('utf-8'),
                    'TVShowTitle': self.name,
                    'episode': 0}
            if videoDoc.find("video").attrib['duration']:
                duration = videoDoc.find("video").attrib['duration']
                duration = int(duration)
                prop['time'] = duration
            if videoDoc.find("video").attrib['release_date']:
                prop['aired'] = videoDoc.find("video").attrib['release_date']
            if videoDoc.find("website/cue_card/text_paragraph_standard"):
                videoDesc = videoDoc.find("website/cue_card/text_paragraph_standard")
                prop['description'] = videoDesc.findtext('text').encode('utf-8')
                #print ET.dump(prop['description'])

            videoUrlNode = videoDoc.find("video/video_format")
            videoUrl = ''
            if videoUrlNode:
                videoUrl = videoUrlNode.attrib['temp_sdt_url']

            if videoUrl != '':
                if self.watched(videoUrl):
                    prop['overlay'] = 7

                self.addVideoLink(prop,videoUrl,iconUrl[0],listsize)
                findVideo=True
        if findVideo:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def watched(self, videoUrl):
        videoFile = videoUrl.split('/')[-1]
        sql_data = "select count(*) from files WHERE strFilename ='%s' AND playCount > 0" % videoFile
        xml_data = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % urllib.quote_plus( sql_data ), )
        wasWatched = re.findall( "<field>(.*?)</field>", xml_data)[0]
        if wasWatched == "1":
            return True
        else :
            return False




    def handleService(self):
        self.name = str(self.__moduleSettings__.paramName)
        self.title = str(self.__moduleSettings__.paramTitle)
        self.category = str(self.__moduleSettings__.paramCategory)
        self.mode = str(self.__moduleSettings__.paramMode)
        self.url = str(self.__moduleSettings__.paramURL)
        #print ""
        #print "test[1]: " + self.mode #sys.argv[2]
        if self.name == 'None':
            self.listsCategories(TVP_MAIN_MENU_TABLE)
        elif self.name != 'None' and self.category == 'xml':
            self.getVideoListXML()
        elif self.name != 'None' and self.category == 'html':
            self.getVideoListHTML()

