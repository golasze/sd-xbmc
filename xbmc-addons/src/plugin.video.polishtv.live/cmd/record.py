# -*- coding: utf-8 -*-
import urllib, urllib2, httplib
import re, sys, os
import threading
import datetime
import time

try:
    import simplejson as json
except ImportError:
    import json

#REC_JSON_PATH = os.path.join(os.getcwd(), "../recs")
HOST = 'XBMC'


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
    
    def download(self, rtmp, rectime, dstpath, name, opts = {}):
        if os.path.isfile(rtmp) and os.access(rtmp, os.X_OK) and os.path.isdir(dstpath):
            file = os.path.join(str(dstpath), name + ".flv")
            os.system(str(rtmp) + " -B " + str(rectime) + " -r " + str(opts['rtmp']) + " -s " + str(opts['ticket']) + " -p token -v live -o " + file)
            os.remove(sys.argv[1])
    
    def getParams(self, playerUrl, login, password, channel, hq):
        data = None
        if login == '' and password == '':
            values = { 'cid': channel, 'platform': 'XBMC' }
        else:
            values = { 'cid': channel, 'username': login, 'userpassword': password, 'platform': 'XBMC' }
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
            if hq == 'true':
                playPath = playPath + 'HI'
            rtmp = str(rtmpLink) + '/' + str(playPath)
            data = { 'rtmp': rtmp, 'ticket': ticket }
        except urllib2.URLError, urlerr:
            data = { 'rtmp': None, 'ticket': None }
            print urlerr
        return data


rec = Record()
opts = rec.getOptions()
params = rec.getParams(opts['urlPlayer'], opts['login'], opts['password'], int(opts['channel']), opts['hq'])
rec.download(opts['rtmp_path'], opts['rectime'], opts['dst_path'], opts['name'], params)  