# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcgui

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"

import pLog

log = pLog.pLog()

DEBUG = True
HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

class urlparser:
  def __init__(self):
    pass

  def getHost(self, url):
    nUrl=''
    match = re.compile('http://(.+?)/').findall(url)
    host = match[0]
    log.info("video hosted by: " + host)
    
    if host=='hd3d.cc':
	nUrl = self.parserHD3D(url)
    if host=='megustavid.com':
	nUrl = self.parserMEGUSTAVID(url)
    if host=='www.putlocker.com':
	nUrl = self.parserPUTLOCKER(url)
    if host=='www.wgrane.pl':
	nUrl = self.parserWGRANE(url)
    if host=='sprocked.com':
	nUrl = self.parserSPROCKED(url)
    if host=='www.cda.pl':
	nUrl = self.parserCDA(url)
#    if host=='www.wootly.ch':
#	nUrl = self.parserWOOTLY(url)

#    if host=='video.anyfiles.pl':
#	nUrl = self.parserANYFILES(url)

    if nUrl=='':
	d = xbmcgui.Dialog()
	d.ok('Znaleziono nowy host', 'brak obslugi ' + host)
	nUrl = False;
    return nUrl

  def parserPUTLOCKER(self,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    r = re.search('value="(.+?)" name="fuck_you"', link)
    if r:
      if DEBUG: log.info("hash: " + r.group(1))
      data = urllib.urlencode({'fuck_you' : r.group(1),
                               'confirm'  : 'Close Ad and Watch as Free User'})
      req = urllib2.Request(url,data)
      req.add_header('User-Agent', HOST)
      cj = cookielib.LWPCookieJar()
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      resp = opener.open(req)
      link = resp.read()
      resp.close()
      match = re.compile("playlist: '(.+?)'").findall(link)
      if len(match) > 0:
	if DEBUG: log.info("get_file.php:" + match[0])
	url = "http://www.putlocker.com" + match[0]
	req = urllib2.Request(url)
	req.add_header('User-Agent', HOST)
	resp = opener.open(req)
	link = resp.read()
	resp.close()
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
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('value="config=(.+?)">').findall(link)
    if len(match) > 0:
      p = match[0].split('=')
      url = "http://megustavid.com/media/nuevo/player/playlist.php?id=" + p[1]
      if DEBUG: log.info("newlink: " + url)
      req = urllib2.Request(url)
      req.add_header('User-Agent', HOST)
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      match = re.compile('<file>(.+?)</file>').findall(link)
      if len(match) > 0:
	if DEBUG: log.info("final link: " + match[0])
	return match[0]
      else:
	return False
    else: 
      return False

  def parserHD3D(self,url):
    url = url + "?i"
    if DEBUG: log.info("hd3d url: " + url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if DEBUG: log.info(link)
    match = re.compile("""url: ["'](.+?)["'],.+?provider:""").findall(link)
    if len(match) > 0:
      if DEBUG: log.info("final link: " + match[0])
      ret = match[0]
    else:
      d = xbmcgui.Dialog()
      d.ok('Brak linku hd3d', 'Przekroczony limit.','Odczekaj chwile i sprobuj jeszcze raz.')
      ret = False
    return ret


  def parserSPROCKED(self,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if DEBUG: log.info(link)
    #autoBuffering: false, url: 'http://178.33.233.217/movies/267?st=YBjFJeEH_u8r-38XCYoD7A', provider: 'lighttpd'
    match = re.search("""url: ['"](.+?)['"],.*\nprovider""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))	
      return match.group(1)
    else: 
      return False


  def parserANYFILES(self,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if DEBUG: log.info(link)
    #<meta property="og:video" content="http://video.anyfiles.pl/uppod/uppod.swf?st=c:I7Jwt8nZ1UvXvkxZ1bFYWevXmkxB1ozl1LdwWeVs3kVhWex2PysGP45Ld4abN7s0v4wV" >
    match = re.search("""<meta property="og:video" content=['"](.+?)['"].*>""",link)
    log.info(match.group(1))
    if match:
      return match.group(1)
    else: 
      return False
 

  def parserWGRANE(self,url):
    hostUrl = 'http://www.wgrane.pl' 		
    playlist = hostUrl + '/html/player_hd/xml/playlist.php?file='
    key = url[-32:]
    nUrl = playlist + key
    if DEBUG: log.info("playlist: " + nUrl)    
    req = urllib2.Request(nUrl)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if DEBUG: log.info(link)
    #<mainvideo url="http://s1.wgrane.pl/download.php?file=168585&amp;time=1334552782"
    match = re.search("""<mainvideo url=["'](.+?)["']""",link)
    #log.info(match.group(1))
    if match:
      ret = match.group(1).replace('&amp;','&')
      if DEBUG: log.info("final link: " + ret)
      return ret
    else: 
      return False

  def parserCDA(self,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if DEBUG: log.info(link)
    #file: 'http://srv2.cda.pl/13480562406186.mp4?st=a0kN7Z2QoBh-S7kzd0JCiQ&e=1348514615', provider: 'http'
    match = re.search("""file: ['"](.+?)['"],""",link)
    #log.info("match: " +str(match.group(1)))
    if match:
      if DEBUG: log.info("final link: " + match.group(1))	
      return match.group(1)
    else: 
      return False


  def parserWOOTLY(self,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if DEBUG: log.info(link)
    #c.value="9ee163b21f5b018544e977cf1fe87569231e4816";
    c = re.search("""c.value="(.+?)";""",link)
    log.info("match: " +str(c.group(1)))
    if c:
      cval = c.group(1)   
    else: 
      return False    
    #<input type="hidden" value="148184646935bc200ed80035c2d16304" class="textbox" name="9ee163b21f5b018544e977cf1fe87569231e4816"
    #file: 'http://srv2.cda.pl/13480562406186.mp4?st=a0kN7Z2QoBh-S7kzd0JCiQ&e=1348514615', provider: 'http'
    match = re.compile("""<input type=['"]hidden['"] value=['"](.+?)['"].+?name=['"](.+?)['"]""").findall(link)
    if len(match) > 0:
      postdata = {};
      for i in range(len(match)):
	if (len(match[i][0])) > len(cval):
	  postdata[cval] = match[i][1]
	else:
	  postdata[match[i][0]] = match[i][1]
      if DEBUG: log.info(str(postdata))
      data = urllib.urlencode(postdata)
      req = urllib2.Request(url,data)
      req.add_header('User-Agent', HOST)
      cj = cookielib.LWPCookieJar()
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      resp = opener.open(req)
      link = resp.read()
      resp.close()
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

