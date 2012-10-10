# -*- coding: utf-8 -*-
import urllib, urllib2, httplib, cookielib
import re, sys, os
import threading
import datetime
import time
import xbmcaddon

try:
    import simplejson as json
except ImportError:
    import json

scriptID = 'plugin.video.polishtv.live'
ptv = xbmcaddon.Addon(scriptID)

#REC_JSON_PATH = os.path.join(os.getcwd(), "../recs")
HOST_XBMC = 'XBMC'
HOST_URL = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "wlacztv.cookie"


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
        
    def getParams(self, paramstring):
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
    

class Record:
    def getOptions(self):
        file = sys.argv[1]
        if os.path.isfile(file):
            raw = open(file, 'r').read()
            res = json.loads(raw)
            return res
    
    def downloadWeebTV(self, rtmp, rectime, dstpath, name, opts = {}):
        if os.path.isfile(rtmp) and os.access(rtmp, os.X_OK) and os.path.isdir(dstpath):
            file = os.path.join(str(dstpath), name + ".flv")
            os.system(str(rtmp) + " -B " + str(rectime) + " -r " + str(opts['rtmp']) + " -s " + str(opts['ticket']) + " -p token -v live -o " + file)
            os.remove(sys.argv[1])
 
    def downloadWlaczTV(self, rtmp, rectime, dstpath, name, opts = {}):
        if os.path.isfile(rtmp) and os.access(rtmp, os.X_OK) and os.path.isdir(dstpath):
            file = os.path.join(str(dstpath), name + ".flv")
            os.system(str(rtmp) + " -B " + str(rectime) + " -r " + str(opts['rtmp']) + " -a " + str(opts['app']) + " -p " + str(opts['pageurl']) + " -t " + str(opts['tcurl']) + " -y " + str(opts['playpath']) + " -v live -o " + file)
            os.remove(sys.argv[1])
    
    def getWeebTVParams(self, playerUrl, login, password, channel, hq):
        data = None
        if login == '' and password == '':
            values = { 'cid': channel, 'platform': 'XBMC' }
        else:
            values = { 'cid': channel, 'username': login, 'userpassword': password, 'platform': 'XBMC' }
        try:
            parser = Parser()
            headers = { 'User-Agent' : HOST_XBMC }
            data = urllib.urlencode(values)
            reqUrl = urllib2.Request(playerUrl, data, headers)
            response = urllib2.urlopen(reqUrl)
            resLink = response.read()
            params = parser.getParams(resLink)
            ticket = parser.getParam(params, "73")
            rtmpLink = parser.getParam(params, "10")
            playPath = parser.getParam(params, "11")
            if hq == 'true':
                playPath = playPath + 'HI'
            rtmp = str(rtmpLink) + '/' + str(playPath)
            data = { 'rtmp': rtmp, 'ticket': ticket }
        except urllib2.URLError, urlerr:
            data = { 'rtmp': None, 'ticket': None }
            print urlerr
        return data

    def getWlaczTVParams(self, login_url, login, password, url):
        rtmp = {}
        cj = cookielib.LWPCookieJar()
        l_headers = { 'User-Agent' : HOST_URL }
        l_post = { 'email': login, 'password': password }
        l_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        l_data = urllib.urlencode(l_post)
        l_req = urllib2.Request(login_url, l_data, l_headers)
        l_response = l_opener.open(l_req)
        l_link = l_response.read()
        l_response.close()
        if not os.path.isdir(ptv.getAddonInfo('path') + os.path.sep + "cookies"):
            os.mkdir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
        cj.save(COOKIEFILE)
        if os.path.isfile(COOKIEFILE):
            cj.load(COOKIEFILE)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST_URL)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        data = response.read()
        response.close()
        match = re.compile("<param name=\"flashvars\" value=\"src=(.+?)&poster=(.+?)&streamType=live&autoPlay=true\"></param>").findall(data)
        if len(match) > 0:
            raw_rtmp_tab = match[0][0].split("?")
            split_rtmp_tab = raw_rtmp_tab[0].split("/")
            rtmp_link = raw_rtmp_tab[0]
            if split_rtmp_tab[len(split_rtmp_tab) - 1].endswith(".stream"):
                app = "live?" + raw_rtmp_tab[1]
                tcurl = "rtmp://" + split_rtmp_tab[len(split_rtmp_tab) - 3] + ":1935/live?" + raw_rtmp_tab[1]
                playpath = split_rtmp_tab[len(split_rtmp_tab) - 1]
            else:
                app = "wlacztv?" + raw_rtmp_tab[1]
                tcurl = "rtmp://" + split_rtmp_tab[len(split_rtmp_tab) - 3] + ":1935/live?" + raw_rtmp_tab[1]
                playpath = split_rtmp_tab[len(split_rtmp_tab) - 1] + "?" + raw_rtmp_tab[1]
            rtmp = {'rtmp': rtmp_link, 'app': app, 'pageurl': url, 'tcurl': tcurl, 'playpath': playpath}
            #log.info("rtmp link: " + str(rtmp))
        return rtmp


rec = Record()
opts = rec.getOptions()
params = {}
if opts['service'] == 'weebtv':
    params = rec.getWeebTVParams(opts['urlPlayer'], opts['login'], opts['password'], int(opts['channel']), opts['hq'])
    rec.downloadWeebTV(opts['rtmp_path'], opts['rectime'], opts['dst_path'], opts['name'], params)
elif opts['service'] == 'wlacztv':
    params = rec.getWlaczTVParams(opts['login_url'], opts['login'], opts['password'], opts['url'])
    rec.downloadWlaczTV(opts['rtmp_path'], opts['rectime'], opts['dst_path'], opts['name'], params)
  