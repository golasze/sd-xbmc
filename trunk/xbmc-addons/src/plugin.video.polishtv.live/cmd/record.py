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

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pCommon

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
    def __init__(self):
        self.common = pCommon.common()
        #self.parser = Parser.Parser()
        
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
            os.system(str(rtmp) + " -B " + str(rectime) + " -r " + str(opts['rtmp']) + " -y " + str(opts['playpath']) + " -v live -o " + file)
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

    def getWlaczTVParams(self, login_url, login, password, url, key):
        rtmp = {}
        post_login = { 'username': login, 'password': password }
        post_key = { 'key': key }
        if not os.path.isdir(ptv.getAddonInfo('path') + os.path.sep + "cookies"):
            os.mkdir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
        self.common.saveURLToFileCookieData(login_url, COOKIEFILE, post_login)
        rtmp_json = json.loads(self.common.postURLFromFileCookieData(url, COOKIEFILE, post_key))
        rtmp_link = rtmp_json['rtmp_server'] + "/" + rtmp_json['app'] + '?wlacztv_session_token=' + rtmp_json['token']
        rtmp = {'rtmp': rtmp_link, 'playpath': rtmp_json['playPath']}
        return rtmp


rec = Record()
opts = rec.getOptions()
params = {}
if opts['service'] == 'weebtv':
    params = rec.getWeebTVParams(opts['urlPlayer'], opts['login'], opts['password'], int(opts['channel']), opts['hq'])
    rec.downloadWeebTV(opts['rtmp_path'], opts['rectime'], opts['dst_path'], opts['name'], params)
elif opts['service'] == 'wlacztv':
    params = rec.getWlaczTVParams(opts['login_url'], opts['login'], opts['password'], opts['url'], opts['key'])
    rec.downloadWlaczTV(opts['rtmp_path'], opts['rectime'], opts['dst_path'], opts['name'], params)
  