# -*- coding: utf-8 -*-
import re, os, sys, cookielib
import urllib, urllib2, re, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import datetime
import time
import simplejson as json

scriptID   = sys.modules[ "__main__" ].scriptID
t = sys.modules[ "__main__" ].language
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, pCommon

log = pLog.pLog()
cj = cookielib.LWPCookieJar()

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
#mainUrl = "http://www.wlacz.tv"
#mainChannels = mainUrl + "/kanaly"
mainUrl = 'http://www.wlacz.tv'
playerUrl = mainUrl + '/api/setPlayer'
channelsUrl = mainUrl + '/api/online_channels'
loginUrl = mainUrl + '/api/login'
isLoggedUrl = mainUrl + '/api/is_logged'

COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "wlacztv.cookie" 

login = ptv.getSetting('wlacztv_login')
password = ptv.getSetting('wlacztv_pass')
record = ptv.getSetting('wlacztv_rec')
rtmppath = ptv.getSetting('default_rtmp')
dstpath = ptv.getSetting('default_dstpath')
timedelta_h = ptv.getSetting('default_timedelta_hours')
timedelta_m = ptv.getSetting('default_timedelta_minutes')

VIDEO_MENU = [ t(55611).encode("utf-8"), t(55613).encode("utf-8"), t(55614).encode("utf-8") ]


class Channels:
    def __init__(self):
        log.info("Loading wlacz.tv")
        self.parser = Parser.Parser()
        self.common = pCommon.common()

    def dec(self, string):
        json_ustr = json.dumps(string, ensure_ascii=False)
        return json_ustr.encode('utf-8')
   
    def checkDirCookie(self):
        if not os.path.isdir(ptv.getAddonInfo('path') + os.path.sep + "cookies"):
            os.mkdir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    
    def isLogged(self):
        content_json = self.common.getURLFromFileCookieData(isLoggedUrl, COOKIEFILE)
        result_json = json.loads(content_json)
        res = self.dec(result_json['logged_in']).replace("\"", "")
        if res == 'true':
            return True
        else:
            return False
    
    def requestLoginData(self):
        if login == "" or password == "":
            d = xbmcgui.Dialog()
            d.ok(t(55604).encode("utf-8"), t(55605).encode("utf-8"), t(55606).encode("utf-8"))
            exit()
        else:
            post = { 'username': login, 'password': password }
            self.checkDirCookie()
            self.common.saveURLToFileCookieData(loginUrl, COOKIEFILE, post)
    
    def channelsList(self, url):
        if self.isLogged():
            raw_json = self.common.getURLFromFileCookieData(url, COOKIEFILE)
            result_json = json.loads(raw_json)
            for o in result_json:
                title = self.dec(o['name']).replace("\"", "")
                #url = self.dec(o['uri']).replace("\"", "")
                icon = self.dec(o['image']).replace("\"", "")
                key = self.dec(o['key']).replace("\"", "")
                self.addChannel('wlacztv', title, key, icon)
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def getChannelRTMPLink(self, key, title, icon):
        post = { 'key': key }
        #log.info('rtmp: ' + str(self.common.postURLFromFileCookieData(playerUrl, COOKIEFILE, post)))
        rtmp_json = json.loads(self.common.postURLFromFileCookieData(playerUrl, COOKIEFILE, post))
        #tcurl = rtmp_json['rtmp_server'] + '/wlacztv/' + rtmp_json['playPath']
        rtmp = rtmp_json['rtmp_server'] + "/" + rtmp_json['app'] + '?wlacztv_session_token=' + rtmp_json['token']
        return { 'title': title, 'icon': icon, 'key': key, 'rtmp': rtmp, 'playpath': rtmp_json['playPath'] }
    
    def addChannel(self, service, title, key, icon):
        u = "%s?service=%s&title=%s&key=%s&icon=%s" % (sys.argv[0], service, title, key, urllib.quote_plus(icon))
        liz = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage = icon)
        liz.setInfo(type="Video", infoLabels={ "Title": title, })
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)

        
class Player:
    def __init__(self):
        pass

    def InputTime(self):
        nowTime = datetime.datetime.now() + datetime.timedelta(hours = int(timedelta_h), minutes = int(timedelta_m))
        text = None
        k = xbmc.Keyboard(str(nowTime.strftime("%H:%M")), t(55616).encode("utf-8") + " " + str(nowTime.strftime("%H:%M")) + ". " + t(55617).encode("utf-8"))
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return self.GetTime(text)
    
    def GetTime(self, end):
        rectime = 0
        if ":" in end:
            nowTime = datetime.datetime.now() + datetime.timedelta(hours = int(timedelta_h), minutes = int(timedelta_m))
            st = time.mktime(nowTime.timetuple())
            nowDate = str(nowTime.strftime("%Y-%m-%d"))
            t = end.split(":")
            tH = t[0]
            tM = t[1]
            tS = "00"
            endTime = nowDate + " " + str(tH) + ":" + str(tM) + ":" + str(tS) + ".0"
            endFormat = "%Y-%m-%d %H:%M:%S.%f"
            endTuple = time.strptime(endTime, endFormat)
            et = time.mktime(datetime.datetime(*endTuple[:7]).timetuple())
            rectime = int(et - st)
            if rectime < 0:
                rectime = 0
        return rectime
        
    def LOAD_AND_PLAY_VIDEO(self, jsonUrl = {}):
        if jsonUrl['rtmp'] == '':
            d = xbmcgui.Dialog()
            d.ok(t(55607).encode("utf-8"), t(55608).encode("utf-8"))
            exit()
        rectime = 0
        item = 1
        if record == 'true':
            d = xbmcgui.Dialog()
            item = d.select(t(55615), VIDEO_MENU)
            if item == 0:
                dwnl = RTMPDownloader()
                if dwnl.isRTMP(rtmppath):
                    rectime = self.InputTime()
                    if os.path.isdir(dstpath):
                        if rectime > 0:
                            dwnl = RTMPDownloader()
                            params = { "url": jsonUrl['rtmp'], "playpath": jsonUrl['playpath'], "download_path": dstpath, "title": jsonUrl['title'], "duration": int(rectime) }
                            dwnl.download(rtmppath, params)
                else:
                    msg = xbmcgui.Dialog()
                    msg.ok(t(55618).encode("utf-8"), t(55619).encode("utf-8"))
            elif item == 2:
                rec = Record()
                rec.Init(playerUrl, jsonUrl['key'], jsonUrl['title'], loginUrl)
                exit()
        if record == 'false' or item == 1:
            try:
                liz = xbmcgui.ListItem(jsonUrl['title'], iconImage = jsonUrl['icon'], thumbnailImage = jsonUrl['icon'])
                liz.setInfo( type="Video", infoLabels={ "Title": jsonUrl['title'], } )
                 
                videoUrl = jsonUrl['rtmp']
                videoUrl += " playpath=" + jsonUrl['playpath']
                videoUrl += " live=true"
                log.info('rtmp raw: ' + videoUrl)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(videoUrl, liz)
            except:
                #log.info('tutaj')
                d = xbmcgui.Dialog()
                d.ok(t(55609).encode("utf-8"), t(55610).encode("utf-8"))  


class RTMPDownloader: 
    def isRTMP(self, fpath):
        res = False
        if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
            res = True
        return res

    def download(self, app, params = {}):
        td = datetime.datetime.now() + datetime.timedelta(hours = int(timedelta_h), minutes = int(timedelta_m))
        nt = time.mktime(td.timetuple())
        today = datetime.datetime.fromtimestamp(nt)
        file = os.path.join(str(params['download_path']), str(params['title']).replace(" ", "_") + "-" + str(today).replace(" ", "_").replace(":", ".") + ".flv")
        os.system(str(app) + " -B " + str(params['duration']) + " -r " + str(params['url']) + " -y " + str(params['playpath']) + " -v live -o " + file)


class Record:
    def __init__(self):
        self.recdir = os.path.join(ptv.getAddonInfo('path'), "recs")
        self.cmddir = os.path.join(ptv.getAddonInfo('path'), "cmd")

    def input(self, text, header):
        k = xbmc.Keyboard(text, header)
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    
    def Init(self, url, key, title, login_url):
        nowTime = datetime.datetime.now() + datetime.timedelta(hours = int(timedelta_h), minutes = int(timedelta_m))
        nowDate = str(nowTime.strftime("%Y-%m-%d"))
        nTime = str(nowTime.strftime("%H:%M"))
        s_Date = self.input(nowDate, t(55620).encode("utf-8"))
        s_Start = self.input(nTime, t(55621).encode("utf-8"))
        e_Date = self.input(nowDate, t(55622).encode("utf-8"))
        e_End = self.input(nTime, t(55623).encode("utf-8"))
        setTime = self.SetTime(s_Date, s_Start, e_Date, e_End)
        nameRec = title.replace(" ", "_") + "_" + s_Date + "." + s_Start.replace(":", ".")
        opts = { 'service': 'wlacztv', 'key': key, 'login_url': login_url, 'date': s_Date, 'start': s_Start, 'rectime': str(setTime[1]), 'name': nameRec, 'url': url, 'login': login, 'password': password, 'dst_path': dstpath, 'rtmp_path': rtmppath, 'hours_delta': timedelta_h, 'minutes_delta': timedelta_m }
        self.saveFile(opts)
        xbmc.executebuiltin('AlarmClock(' + str(nameRec) + ', "RunScript(' + str(self.cmddir) + str(os.sep) + 'record.py, ' + str(self.recdir) + str(os.sep) + str(nameRec) + '.json)", ' + str(setTime[0]) + '))')
        
    def saveFile(self, opts = {}):
        out = json.dumps(opts)
        file = self.recdir + os.sep + opts['name'] + '.json'
        wfile = open(file, "w")
        wfile.write(out)
        wfile.close()

    def SetTime(self, startDate, startTime, endDate, endTime):
        nowTime = datetime.datetime.now() + datetime.timedelta(hours = int(timedelta_h), minutes = int(timedelta_m))
        start = startDate + " " + startTime + ":00.0"
        end = endDate + " " + endTime + ":00.0"
        format = "%Y-%m-%d %H:%M:%S.%f"
        startTuple = time.strptime(start, format)
        endTuple = time.strptime(end, format)
        nt = time.mktime(nowTime.timetuple())
        st = time.mktime(datetime.datetime(*startTuple[:7]).timetuple())
        et = time.mktime(datetime.datetime(*endTuple[:7]).timetuple())
        alarmtime = int(float(st - nt) / 60)
        rectime = int(et - st)
        return [ alarmtime, rectime ]

    def GetAlarmTime(self, startDate, startTime):
        nowTime = datetime.datetime.now() + datetime.timedelta(hours = int(timedelta_h), minutes = int(timedelta_m))
        start = startDate + " " + startTime + ":00.0"
        format = "%Y-%m-%d %H:%M:%S.%f"
        startTuple = time.strptime(start, format)
        nt = time.mktime(nowTime.timetuple())
        st = time.mktime(datetime.datetime(*startTuple[:7]).timetuple())
        alarmtime = int(float(st - nt) / 60)
        return alarmtime
        
    
    def loadFiles(self):
        if os.path.isdir(self.recdir):
            for fileName in os.listdir(self.recdir):
                pathFile = self.recdir + os.sep + fileName
                if pathFile.endswith('.json'):
                    raw = open(pathFile, 'r').read()
                    res = json.loads(raw)
                    alarmtime = self.GetAlarmTime(res['date'], res['start'])
                    if int(alarmtime) < 0:
                        os.remove(pathFile)
                    else:
                        xbmc.executebuiltin('CancelAlarm(' + str(res['name']) + ', silent)')
                        xbmc.executebuiltin('AlarmClock(' + str(res['name']) + ', "RunScript(' + str(self.cmddir) + str(os.sep) + 'record.py, ' + str(self.recdir) + str(os.sep) + str(res['name']) + '.json)", ' + str(alarmtime) + '))')


class WlaczTV:	
    def __init__(self):
        self.parser = Parser.Parser()
        self.channel = Channels()
        self.player = Player()
    	
    def handleService(self):
        params = self.parser.getParams()
        title = str(self.parser.getParam(params, "title"))
        key = str(self.parser.getParam(params, "key"))
        icon = str(self.parser.getParam(params, "icon"))
        log.info('title: ' + title)
        #log.info('url: ' + url)
        if title == 'None':
	 		self.channel.requestLoginData()
	 		self.channel.channelsList(channelsUrl)
        elif title != '' and key != '':
            self.player.LOAD_AND_PLAY_VIDEO(self.channel.getChannelRTMPLink(key, title, icon))
            #self.channel.getChannelRTMPLink(key, title, icon)

    def handleRecords(self):
        d = xbmcgui.Dialog()
        rec = Record()
        qrec = d.yesno("Nagrywanie", "Czy odświeżyć nagrywanie wszystkich pozycji?")
        if qrec == 1:
            rec.loadFiles()



