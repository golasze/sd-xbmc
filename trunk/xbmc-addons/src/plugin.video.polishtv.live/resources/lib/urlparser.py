# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcaddon, xbmc, xbmcgui, simplejson

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

import pLog, xppod, Parser, settings, pCommon
import maxvideo, anyfiles

log = pLog.pLog()
sets = settings.TVSettings()

DEBUG = True
HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

chars_table = {
  'f': 'A',
  'F': 'a',
  'a': 'F',
  'A': 'f',
  'k': 'B',
  'K': 'b',
  'b': 'K',
  'B': 'k',
  'm': 'I',
  'M': 'i',
  'i': 'M',
  'I': 'm',
  'D': 'x',
  'x': 'D',
  'O': 'y',
  'y': 'O',
  'C': 'z',
  'z': 'C'
}


class urlparser:
  def __init__(self):
    self.cm = pCommon.common()

  def replaceChars(self, char):
      out_char = char
      for char_in, char_out in chars_table.items():
          if char == char_in:
              out_char = char_out
              break
      return out_char  


  def createString(self, string):
      string_in_tab = list(string)
      string_out_tab = []
      string_out = string
      for i in range(len(string_in_tab)):
          string_out_tab.append(self.replaceChars(string_in_tab[i]))
      for a in range(len(string_out_tab)):
          if a == 0:
              string_out = string_out_tab[a]
          else:
              string_out += string_out_tab[a]
      return string_out


  def getHostName(self, url, nameOnly = False):
    hostName = ''       
    match = re.search('http://(.+?)/',url)
    if match:
      hostName = match.group(1)
      if (nameOnly):
	n = hostName.split('.')
	hostName = n[-2]
    return hostName


#  def requestData(self, url, postdata = {}):
#	req = urllib2.Request(url)
#	req.add_header('User-Agent', HOST)
#	response = urllib2.urlopen(req)
#	data = response.read()
#	response.close()	
#	return data


  def getVideoLink(self, url):
    nUrl=''
    host = self.getHostName(url)
    log.info("video hosted by: " + host)
    log.info(url)
    
    if host == 'www.putlocker.com':
        nUrl = self.parserPUTLOCKER(url)
    if host == 'www.sockshare.com':
        nUrl = self.parserSOCKSHARE(url)
    if host == 'megustavid.com':
        nUrl = self.parserMEGUSTAVID(url)
    if host == 'hd3d.cc':
        nUrl = self.parserHD3D(url)
    if host == 'sprocked.com':
        nUrl = self.parserSPROCKED(url)
    if host == 'odsiebie.pl':
        nUrl = self.parserODSIEBIE(url) 
    if host == 'www.wgrane.pl':
        nUrl = self.parserWGRANE(url)
    if host == 'www.cda.pl':
        nUrl = self.parserCDA(url)
    if host == 'maxvideo.pl' or host == 'nextvideo.pl':
        nUrl = self.parserMAXVIDEO(url)
#    if host == 'nextvideo.pl':
#        nUrl = self.parserNEXTVIDEO(url)
    if host == 'video.anyfiles.pl':
        nUrl = self.parserANYFILES(url)
    if host == 'www.videoweed.es' or host == 'www.videoweed.com' or host == 'videoweed.es' or host == 'videoweed.com':
        nUrl = self.parserVIDEOWEED(url)
    if host== 'www.novamov.com':
        nUrl = self.parserNOVAMOV(url)
    if host== 'www.nowvideo.eu':
        nUrl = self.parserNOWVIDEO(url)
    if host== 'www.rapidvideo.com':
        nUrl = self.parserRAPIDVIDEO(url)
    if host== 'www.videoslasher.com':
        nUrl = self.parserVIDEOSLASHER(url)

	
    return nUrl

#nUrl - "" ; brak obslugi hosta
#nUrl - False ; broken parser, cos sie pewnie zmienilo
#nUrl - "http:...." ; link do streamu


  def parserPUTLOCKER(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)    
    r = re.search('value="(.+?)" name="fuck_you"', link)
    if r:
      if DEBUG: log.info("hash: " + r.group(1))
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "putlocker.cookie"
      query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
      postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
      link = self.cm.getURLRequestData(query_data, postdata)
      match = re.compile("playlist: '(.+?)'").findall(link)
      if len(match) > 0:
        if DEBUG: log.info("get_file.php:" + match[0])
        url = "http://www.putlocker.com" + match[0]
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        if DEBUG: log.info(link)
        match = re.compile('</link><media:content url="(.+?)" type="video').findall(link)
        if len(match) > 0:
          url = match[0].replace('&amp;','&')
          if DEBUG: log.info("final link: " + url)
          return url
        else:
          return False
      else:
        return False
    else:
      return False


  def parserMEGUSTAVID(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)    
    match = re.compile('value="config=(.+?)">').findall(link)
    if len(match) > 0:
      p = match[0].split('=')
      url = "http://megustavid.com/media/nuevo/player/playlist.php?id=" + p[1]
      if DEBUG: log.info("newlink: " + url)     
      query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)      
      if DEBUG: log.info(link)
      match = re.compile('<file>(.+?)</file>').findall(link)
      if len(match) > 0:
        if DEBUG: log.info("final link: " + match[0])
        return match[0]
      else:
        return False
    else: 
      return False


  def parserHD3D(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    match = re.compile("""url: ["'](.+?)["'],.+?provider:""").findall(link)
    if len(match) > 0:
      if DEBUG: log.info("final link: " + match[0])
      ret = match[0]
    else:
     ret = False
    return ret


  def parserSPROCKED(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    match = re.search("""url: ['"](.+?)['"],.*\nprovider""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))       
      return match.group(1)
    else: 
      return False


  def parserODSIEBIE(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    try:
      (v_ext, v_file, v_dir, v_port, v_host) = re.search("\|\|.*SWFObject",link).group().split('|')[40:45]
      url = "http://%s.odsiebie.pl:%s/d/%s/%s.%s" % (v_host, v_port, v_dir, v_file, v_ext);
    except:
      url = False
    return url


  def parserWGRANE(self,url):
    hostUrl = 'http://www.wgrane.pl'            
    playlist = hostUrl + '/html/player_hd/xml/playlist.php?file='
    key = url[-32:]
    nUrl = playlist + key
    if DEBUG: log.info("playlist: " + nUrl)
    query_data = { 'url': nUrl, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    match = re.search("""<mainvideo url=["'](.+?)["']""",link)
    if match:
      ret = match.group(1).replace('&amp;','&')
      if DEBUG: log.info("final link: " + ret)
      return ret
    else: 
      return False


  def parserCDA(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    match = re.search("""file: ['"](.+?)['"],""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))       
      return match.group(1)
    else: 
      return False


  def parserDWN(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    #<iframe src="http://dwn.so/player/embed.php?v=DS301459CC&width=850&height=440"
    match = re.search("""<iframe src="(.+?)&""",link)
    if match:
      query_data = { 'url': match.group(1), 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)
      if DEBUG: log.info(link)  
    else: 
      return False


  def parserANYFILES(self,url):
    self.anyfiles = anyfiles.serviceParser()
    retVal = self.anyfiles.getVideoUrl(url)
    return retVal
  
  
  def parserWOOTLY(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    #c.value="9ee163b21f5b018544e977cf1fe87569231e4816";
    c = re.search("""c.value="(.+?)";""",link)
    #log.info("match: " +str(c.group(1)))
    if c:
      cval = c.group(1)   
    else: 
      return False    
    #<input type="hidden" value="148184646935bc200ed80035c2d16304" class="textbox" name="9ee163b21f5b018544e977cf1fe87569231e4816"
    match = re.compile("""<input type=['"]hidden['"] value=['"](.+?)['"].+?name=['"](.+?)['"]""").findall(link)
    if len(match) > 0:
      postdata = {};
      for i in range(len(match)):
        if (len(match[i][0])) > len(cval):
          postdata[cval] = match[i][1]
        else:
          postdata[match[i][0]] = match[i][1]
      if DEBUG: log.info(str(postdata))
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "wootly.cookie"
      query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
      link = self.cm.getURLRequestData(query_data, postdata)
      if DEBUG: log.info(link)
      #<video src="http://r012.wootly.ch/v/01/d6f5ec9acce1bf5c370fac5cb401fe02c30ee4fc.mp4" 
      match = re.search("""<video.*\n.*src=['"](.+?)['"]""",link)
      #log.info("match: " +str(match.group(1)))
      if match:
        if DEBUG: log.info("final link: " + match.group(1))
        return match.group(1)
      else: 
        return False
    else: 
      return False


  def parserMAXVIDEO(self, url):
      self.api = maxvideo.API()
      
      #addon settings
      self.servset = sets.getSettings('maxvideo')
      if self.servset['maxvideo_notify'] == 'true': notify = True
      else: notify = False

      videoUrl = ''
      videoHash = url.split('/')[-1]
      login = self.api.Login(self.servset['maxvideo_login'], self.servset['maxvideo_password'], notify)
      if (login):
	  self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
	  cookiefile = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "maxvideo.cookie"	
      else: 
	  cookiefile = ''	
      videoUrl = self.api.getVideoUrl(videoHash, cookiefile, notify)
      return videoUrl
    
      
  def parserVIDEOWEED(self, url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match_domain = re.compile('flashvars.domain="(.+?)"').findall(link)
    match_file = re.compile('flashvars.file="(.+?)"').findall(link)
    match_filekey = re.compile('flashvars.filekey="(.+?)"').findall(link)
    if len(match_domain) > 0 and len(match_file) > 0 and len(match_filekey) > 0:
        get_api_url = ('%s/api/player.api.php?user=undefined&codes=1&file=%s&pass=undefined&key=%s') % (match_domain[0], match_file[0], match_filekey[0])
        link_api = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	#link_api = self.requestData(get_api_url)
        if 'url' in link_api:
              parser = Parser.Parser()
              params = parser.getParams(link_api)
              if DEBUG: log.info("final link: " + parser.getParam(params, "url"))
              return parser.getParam(params, "url")
        else:
              return False
    else:
        return False
	
      
  def parserNOVAMOV(self, url):
      query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)
      match_file = re.compile('flashvars.file="(.+?)";').findall(link)
      match_key = re.compile('flashvars.filekey="(.+?)";').findall(link)
      if len(match_file) > 0 and len(match_key) > 0:
          get_api_url = ('http://www.novamov.com/api/player.api.php?key=%s&user=undefined&codes=1&pass=undefined&file=%s') % (match_key[0], match_file[0])
	  link_api = link_api = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	  #link_api = self.requestData(get_api_url)
          match_url = re.compile('url=(.+?)&title').findall(link_api)
          if len(match_url) > 0:
              return match_url[0]
          else:
              return False

  def parserNOWVIDEO(self, url):
      query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)
      match_file = re.compile('flashvars.file="(.+?)";').findall(link)
      match_key = re.compile('flashvars.filekey="(.+?)";').findall(link)
      if len(match_file) > 0 and len(match_key) > 0:
          get_api_url = ('http://www.nowvideo.eu/api/player.api.php?codes=1&key=%s&user=undefined&pass=undefined&file=%s') % (match_key[0], match_file[0])
	  query_data = { 'url': get_api_url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
	  link_api = self.cm.getURLRequestData(query_data)
          match_url = re.compile('url=(.+?)&title').findall(link_api)
          if len(match_url) > 0:
              return match_url[0]
          else:
              return False


  def parserSOCKSHARE(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data) 
    r = re.search('value="(.+?)" name="fuck_you"', link)
    if r:
      if DEBUG: log.info("hash: " + r.group(1))
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "sockshare.cookie"
      postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
      query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
      link = self.cm.getURLRequestData(query_data, postdata) 
      match = re.compile("playlist: '(.+?)'").findall(link)
      if len(match) > 0:
        if DEBUG: log.info("get_file.php:" + match[0])
        url = "http://www.sockshare.com" + match[0]
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data) 
        if DEBUG: log.info(link)
        match = re.compile('</link><media:content url="(.+?)" type="video').findall(link)
        if len(match) > 0:
          url = match[0].replace('&amp;','&')
          if DEBUG: log.info("final link: " + url)
          return url
        else:
          return False
      else:
        return False
    else:
      return False

  def parserRAPIDVIDEO(self,url):
    query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    if DEBUG: log.info(link)
    match = re.search("""'(.+?)','720p'""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))       
      return match.group(1)
    else: 
      return False


  def parserVIDEOSLASHER(self, url):
    self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "videoslasher.cookie"
    query_data = { 'url': url.replace('embed', 'video'), 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
    postdata = {'confirm': 'Close Ad and Watch as Free User', 'foo': 'bar'}
    data = self.cm.getURLRequestData(query_data, postdata)
    
    match = re.compile("playlist: '/playlist/(.+?)'").findall(data)
    if len(match)>0:
      query_data = { 'url': 'http://www.videoslasher.com//playlist/' + match[0], 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE,  'use_post': True, 'return_data': True }
      data = self.cm.getURLRequestData(query_data)
      #url="http://proxy4.videoslasher.com/free/Y/YR/YRW6OFQAPDWA.flv?h=XekQ5nvD9Ub6jJ7kMLlgaw&e=1357989166"
      match = re.compile('<title>Video</title><media:content url="(.+?)"').findall(data)
      if len(match)>0:
	sid = self.cm.getCookieItem(self.COOKIEFILE,'authsid')
	if sid != '':
	  #Cookie="authsid=08jv4vdln1ocd22do043r91vg4"
	  streamUrl = match[0] + '|Cookie="authsid=' + sid + '"'
	  return streamUrl	
	else:
	  return False
      else:
	return False
    else:
      return False



          
