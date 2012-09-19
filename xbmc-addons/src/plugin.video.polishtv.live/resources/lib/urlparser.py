# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"

import pLog

log = pLog.pLog()

DEBUG = False
HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'


#przyklady hostow:
#http://megustavid.com/e=VAQMQC8
#http://www.putlocker.com/embed/E3E8E5F6FB802638
#http://hd3d.cc/file,embed,6747419166EBE0D6.html
#http://nextvideo.pl/embed/630x430/w/9pAGgL8Os5iRx0rx

class urlparser:
  def __init__(self):
    pass

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
	  if DEBUG:
            log.info("final link: " + url)
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
    req = urllib2.Request(url)
    req.add_header('User-Agent', HOST)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile("url: '(.+?)', provider").findall(link)
    if len(match) > 0:
      if DEBUG: log.info("final link: " + match[0])
      return match[0]
    else:
      return False
