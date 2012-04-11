# -*- coding: utf-8 -*-
import urllib, urllib2, httplib
import re, sys, os, cgi
import xbmcplugin, xbmcgui, xbmcaddon, xbmc
import threading
import simplejson as json
import datetime
import time

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
#sys.path.append( os.path.join( os.getcwd(), "../" ) )

import pLog, settings

log = pLog.pLog()

mainUrl = 'http://weeb.tv'
playerUrl = mainUrl + '/api/setplayer'
apiUrl = mainUrl + '/api/getChannelList'
iconUrl = 'http://static2.weeb.tv/ci/'
HOST = 'XBMC'

login = ptv.getSetting('weebtv_login')
password = ptv.getSetting('weebtv_password')
multi = ptv.getSetting('weebtv_hq')
record = ptv.getSetting('weebtv_rec')
rtmppath = ptv.getSetting('weebtv_rtmp')
dstpath = ptv.getSetting('weebtv_dstpath')

VIDEO_MENU = [ "Nagrywanie", "Odtwarzanie" ]

SKINS = {
        'confluence': { 'opt1': 500, 'opt2': 50 },
        'transparency': { 'opt1': 53, 'opt2': 590 }
}


class Settings:
    def __init__(self):
        pass

    def setApiUrl(self):
        return apiUrl

    def setIconUrl(self):
        return iconUrl
    
    def setViewMode(self, view):
        if view != 'orig':
            for k,v in SKINS.items():
                if k in xbmc.getSkinDir():
                    if view == 'general':
                        xbmc.executebuiltin("Container.SetViewMode(" + str(v['opt2']) + ")")
                    elif view == 'other':
                        xbmc.executebuiltin("Container.SetViewMode(" + str(v['opt1']) + ")")
                        

class Channels:
	def __init__(self):
		pass

	def dec(self, string):
		json_ustr = json.dumps(string, ensure_ascii=False)
		return json_ustr.encode('utf-8')

	def SortedTab(self, json):
		strTab = []
		outTab = []
		for v,k in json.iteritems():
			strTab.append(int(v))
			strTab.append(k)
			outTab.append(strTab)
			strTab = []
		outTab.sort(key=lambda x: x[0])
		return outTab
	
	def API(self, url):
		res = { "0": "Null" }
		try:
			headers = { 'User-Agent' : HOST, 'ContentType' : 'application/x-www-form-urlencoded' }
			post = { 'username': login, 'userpassword': password }
			data = urllib.urlencode(post)
			req = urllib2.Request(url, data, headers)
			raw = urllib2.urlopen(req)
			res = json.loads(raw.read())
		except err:
			res = { "0": "Error" }
		return res

	def ChannelsList(self, url):
		action = 0
		channelsArray = self.SortedTab(self.API(url))
		if len(channelsArray) > 0:
			try:
				if channelsArray[0][1] == 'Null':
					msg = xbmcgui.Dialog()
					msg.ok("Błąd API", "Brak kanałów pobranych z API.")
				elif channelsArray[0][1] != 'Error' and channelsArray[0][1] != 'Null':
					for i in range(len(channelsArray)):
						row = channelsArray[i][1]
						cid = row['cid']
						name = self.dec(row['channel_name']).replace("\"", "")
						title = self.dec(row['channel_title']).replace("\"", "")
						desc = self.dec(row['channel_description']).replace("\"", "")
						tags = self.dec(row['channel_tags']).replace("\"", "")
						img = row['channel_image']
						online = row['channel_online']
						rank = row['rank']
						bitrate = row['multibitrate']
						user = self.dec(row['user_name']).replace("\"", "")
						image = iconUrl + "no_video.png"
						if img == '1':
							image = iconUrl + cid + ".jpg"
						if online == '2':
							action = 1
						else:
							action = 0
						self.addChannel('weebtv', str(action), cid, title, image, desc, tags, user, name)
					s = Settings()
					s.setViewMode('other')
					xbmcplugin.endOfDirectory(int(sys.argv[1]))
			except KeyError, keyerr:
				msg = xbmcgui.Dialog()
				print keyerr
				msg.ok("Błąd API", "Błędny klucz odczytany z API.")				
		else:
			msg = xbmcgui.Dialog()
			msg.ok("Błąd API", "Brak kanałów pobranych z API.")

	def addChannel(self, service, action, cid, title, img, desc, tags, user, name):
		label = title
		liz = xbmcgui.ListItem(label, iconImage = "DefaultFolder.png", thumbnailImage = img)
		liz.setProperty("IsPlayable", "false")
		liz.setInfo(type = "Video", infoLabels={ "Title": title,
										   "Plot": desc,
										   "Studio": "WEEB.TV",
										   "Tagline": tags,
										   "Aired": user } )
		u = '%s?service=%s&action=%d&cid=%d&title=%s' % (sys.argv[0], str(service), int(action), int(cid), urllib.quote_plus(title))
		xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
		FILE = open(os.path.join(ptv.getAddonInfo('path'), "strm", "%s.strm" % ''.join(c for c in title if c in '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')),"w+")
		FILE.write("plugin://plugin.video.polishtv.live/?service=%s&action=%d&cid=%s&title=%s" % (service, int(action), cid, urllib.quote_plus(title)))


class Parser:
    def __init__(self):
        pass
    
    def getParam(self, params, name):
        try:
            result = params[name]
            result = urllib.unquote_plus(result)
            return result
        except:
            return None

    def getIntParam (self, params, name):
        try:
            param = self.getParam(params, name)
            return int(param)
        except:
            return None
    
    def getBoolParam (self, params, name):
        try:
            param = self.getParam(params,name)
            return 'True' == param
        except:
            return None
        
    def getParams(self, paramstring = sys.argv[2]):
        param=[]
        if len(paramstring) >= 2:
            params = paramstring
            cleanedparams = params.replace('?', '')
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


class Player(xbmc.Player):
    def __init__(self, *args, **kwargs):
        self.is_active = True
        print "#Starting control WeebPlayer events#"

    def setPremium(self, premium):
        self.premium = premium
        
    def getPremium(self):
        return self.premium
    
    def onPlayBackPaused(self):
        print "#Im paused#"
        ThreadPlayerControl("Stop").start()
        self.is_active = False
        
    def onPlayBackResumed(self):
        print "#Im Resumed #"
        
    def onPlayBackStarted(self):
        print "#Playback Started#"
        try:
            print "#Im playing :: " + self.getPlayingFile()
        except:
            print "#I failed get what Im playing#"
            
    def onPlayBackEnded(self):
        msg = xbmcgui.Dialog()
        print "#Playback Ended#"
        self.is_active = False
        if self.getPremium() == 0:
            msg.ok("Błąd odtwarzania.", "Przekroczony limit lub zbyt duża liczba użytkowników.", "Wykup konto premium aby oglądać bez przeszkód.")
        else:
            msg.Warning("Błąd odtwarzania.", "Serwer odrzucił połączenie z nieznanych przyczyn.")
        
    def onPlayBackStopped(self):
        print "## Playback Stopped ##"
        self.is_active = False
    
    def sleep(self, s):
        xbmc.sleep(s)
        
		

class Video:
    def InputTime(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text

    def LinkParams(self, channel):
        data = None
        if login == '' and password == '':
            values = { 'cid': channel }
        else:
            values = { 'cid': channel, 'username': login, 'userpassword': password }
        try:
            parser = Parser()
            headers = { 'User-Agent' : HOST }
            data = urllib.urlencode(values)
            reqUrl = urllib2.Request(playerUrl, data, headers)
            response = urllib2.urlopen(reqUrl)
            resLink = response.read()
            params = parser.getParams(resLink)
            ticket = parser.getParam(params, "73")
            rtmpLink = parser.getParam(params, "10")
            playPath = parser.getParam(params, "11")
            premium = parser.getIntParam(params, "5")
            status = parser.getParam(params, "0")
            data = { 'rtmp': rtmpLink, 'ticket': ticket, 'playpath': playPath, 'premium': premium, 'status': status }
        except urllib2.URLError, urlerr:
            msg = xbmcgui.Dialog()
            data = { 'rtmp': None, 'ticket': None, 'playpath': None, 'premium': premium, 'status': status }
            print urlerr
            msg.ok("Błąd setPlayer.", "Nie uzyskano danych do autoryzacji.", "Sprawdź połączenie sieciowe.")
        return data

    def LinkPlayable(self, channel, bitrate):
        dataLink = {}
        vals = self.LinkParams(channel)
        rtmpLink = vals['rtmp']
        ticket = vals['ticket']
        playpath = vals['playpath']
        premium = vals['premium']
        status = vals['status']
        if bitrate == '1' and multi == 'true':
            playpath = playpath + 'HI'
        rtmp = str(rtmpLink) + '/' + str(playpath)
        rtmp += ' swfUrl='  + str(ticket)
        rtmp += ' pageUrl=token'
        rtmp += ' live=true'
        print 'Output rtmp link: %s' % (rtmp)
        return { 'rtmp': rtmp, 'premium': premium, 'status': status, 'ticket': '' }

    def LinkRecord(self, channel, bitrate):
        dataLink = {}
        vals = self.LinkParams(channel)
        rtmpLink = vals['rtmp']
        ticket = vals['ticket']
        playpath = vals['playpath']
        premium = vals['premium']
        status = vals['status']
        if bitrate == '1' and multi == 'true':
            playpath = playpath + 'HI'
        rtmp = str(rtmpLink) + '/' + str(playpath)
        return { 'rtmp': rtmp, 'premium': premium, 'status': status, 'ticket': ticket }

    def ChannelInfo(self, channel):
        chan = Channels()
        dataInfo = { 'title': '', 'image': '', 'bitrate': '' }
        try:
            channelsArray = chan.API(apiUrl)
            for v,k in channelsArray.items():
                if channel == int(k['cid']):
                    cid = k['cid']
                    title = chan.dec(k['channel_title']).replace("\"", "")
                    bitrate = k['multibitrate'] 
                    img = k['channel_image']
                    image = iconUrl + "no_video.png"
                    if img == '1':
                        image = iconUrl + cid + ".jpg"
                    dataInfo = { 'title': title, 'image': image, 'bitrate': bitrate }
                    break
        except TypeError, typerr:
            print typerr
        return dataInfo        

    def RunVideoLink(self, channel):
        rectime = 0
        item = 1
        videoLink = { 'status': '0' }
        val = self.ChannelInfo(channel)
        if record == 'true':
            d = xbmcgui.Dialog()
            item = d.select("Wybór", VIDEO_MENU)
            print 'item: ' + str(item)
            if item != '':
                if item == 1:
                    videoLink =  self.LinkPlayable(channel, val['bitrate'])
                elif item == 0:
                    dwnl = RTMPDownloader()
                    if dwnl.isRTMP(rtmppath):
                        msg = xbmcgui.Dialog()
                        msg.ok("Podaj czas nagrania", "Podaj wartość po jakim czasie", "ma się skończyć nagrywanie.", "Dla 1h 30m podaj 90m")
                        rectime = self.InputTime()
                        videoLink =  self.LinkRecord(channel, val['bitrate'])
                    else:
                        msg = xbmcgui.Dialog()
                        msg.ok("Informacja", "Nie masz zainstalowanego rtmpdump")
        else:
            videoLink =  self.LinkPlayable(channel, val['bitrate'])               
        if videoLink['status'] == '1':
            if videoLink['rtmp'].startswith('rtmp://') and item == 1:
                liz = xbmcgui.ListItem(val['title'], iconImage = val['image'], thumbnailImage = val['image'])
                liz.setInfo( type="Video", infoLabels={ "Title": val['title'], } )
                try:
                    player = Player()
                    player.setPremium(int(videoLink['premium']))
                    player.play(videoLink['rtmp'], liz)
                    while player.is_active:
                        player.sleep(100)
                except:
                    msg = xbmcgui.Dialog()
                    msg.ok("Błąd odtwarzania", "Wystąpił nieznany błąd.", "Odtwarzanie wstrzymano.")
            elif videoLink['rtmp'].startswith('rtmp://') and item == 0:
                if os.path.isdir(dstpath):
                    if int(rectime) > 0:
                        dwnl = RTMPDownloader()
                        params = { "url": videoLink['rtmp'], "download_path": dstpath, "title": val['title'], "live": "true", "swfUrl": videoLink['ticket'], "pageUrl": "token", "duration": int(rectime) }
                        dwnl.download(rtmppath, params)
            else:
                msg = xbmcgui.Dialog()
                msg.ok("Błąd", "Odtwarzanie wstrzymane", "z powodu błędnego linku rtmp")
        else:
            msg = xbmcgui.Dialog()
            msg.ok("Informacja", "Wystąpił problem po stronie serwera weeb.tv")



class ThreadPlayerControl(threading.Thread):
	def __init__(self, command):
		self.command = command
		threading.Thread.__init__ (self)
	
	def run(self):
		xbmc.executebuiltin('PlayerControl(' + self.command + ')')


class RTMPDownloader: 
    def isRTMP(self, fpath):
        res = False
        if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
            res = True
        return res

    def download(self, app, params = {}):
        td = datetime.datetime.now()
        nt = time.mktime(td.timetuple())
        today = datetime.datetime.fromtimestamp(nt)
        file = os.path.join(str(params['download_path']), str(params['title']).replace(" ", "_") + "-" + str(today).replace(" ", "_").replace(":", ".") + ".mp4")
        rectime = int(60 * int(params['duration']))
        os.system(str(app) + " -B " + str(rectime) + " -r " + str(params['url']) + " -s " + str(params['swfUrl']) + " -p token -v live -o " + file)
        

class WeebTV:
	def handleService(self):
		s = Settings()
		parser = Parser()
		params = parser.getParams()
		cid = parser.getIntParam(params, "cid")
		title = parser.getParam(params, "title")
		action = parser.getIntParam(params, "action")
		print "action: " + str(action) + ", title: " + str(title)
		if not os.path.isdir(os.path.join(ptv.getAddonInfo('path'), "strm")):
			os.mkdir(os.path.join(ptv.getAddonInfo('path'), "strm"))
		if action == None:
			show = Channels()
			show.ChannelsList(apiUrl + "&option=online-alphabetical")
		elif action == 1:
			s.setViewMode('other')
			if cid > 0 and title != "":
				init = Video()
				init.RunVideoLink(cid)
		elif action == 0:
			s.setViewMode('other')
			msg = xbmcgui.Dialog()
			msg.Warning(t(57005).encode('utf-8'), t(57006).encode('utf-8'), t(57007).encode('utf-8'), t(57008).encode('utf-8'))