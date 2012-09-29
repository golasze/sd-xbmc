# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"

import pLog

log = pLog.pLog()

DEBUG = True
HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

str_table = {
  '*': '/',
  '?': ':',
  '%6z': 'l',
  '%6x': 'm',
  'maxvidej.pl': 'maxvideo.pl'
}

#to do:
#http://xvidstage.com/id6olxl28ul2
#http://flashstream.in/jnu976yuwga3
#http://muchshare.net/air7v5uggpw6
#http://maxvideo.pl/w/ZYiiszCc - almost DONE!!!
#http://nextvideo.pl/embed/630x430/w/9pAGgL8Os5iRx0rx

#generates final link but XBMC doesnt want to play it
#http://www.wootly.ch/?v=G79EEEE4

#cannot figure out these ones:
#http://www.videoweed.es/file/7a554a4b44291
#http://video.anyfiles.pl/uppod/uppod.swf?st=c:I7Jwt8nZ1UvXvkxZ1bFYWevXmkxB1ozl1LdwWeVs3kVhWex2PysGP45Ld4abN7s0v4wV
#http://dwn.so/v/DS301459CC
#http://www.novamov.com/video/ec0a25241419e

class urlparser:
  def __init__(self):
    pass

  def replaceString(self, string):
      for str_in, str_out in str_table.items():
          out = string.replace(str_in, str_out)
          string = out
      return out

  def getHostName(self, url):
    hostName = ''       
    match = re.search('http://(.+?)/',url)
    if match:
      hostName = match.group(1)
    return hostName


  def requestData(self, url, postdata = {}):
    d = ''
    if len(postdata)<>0:
      d = urllib.urlencode(postdata)  
    req = urllib2.Request(url, d) #1
    req.add_header('User-Agent', HOST) #1
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    response = opener.open(req)
    data = response.read()
    response.close()
    return data
 

  def getVideoLink(self, url):
    nUrl=''
    host = self.getHostName(url)
    log.info("video hosted by: " + host)

    if host=='www.putlocker.com':
        nUrl = self.parserPUTLOCKER(url)
    if host=='megustavid.com':
        nUrl = self.parserMEGUSTAVID(url)
    if host=='hd3d.cc':
        nUrl = self.parserHD3D(url)
    if host=='sprocked.com':
        nUrl = self.parserSPROCKED(url)
    if host=='odsiebie.pl':
        nUrl = self.parserODSIEBIE(url) 
    if host=='www.wgrane.pl':
        nUrl = self.parserWGRANE(url)
    if host=='www.cda.pl':
        nUrl = self.parserCDA(url)
    if host == 'maxvideo.pl':
        nUrl = self.parserMAXVIDEO(url)
        
#    if host=='www.novamov.com':
#       nUrl = self.parserNOVAMOV(url)
#    if host=='dwn.so':
#       nUrl = self.parserDWN(url)
#    if host=='www.wootly.ch':
#       nUrl = self.parserWOOTLY(url)
#    if host=='video.anyfiles.pl':
#       nUrl = self.parserANYFILES(url)

    return nUrl

#nUrl - "" ; brak obslugi hosta
#nUrl - False ; broken parser, cos sie pewnie zmienilo
#nUrl - "http:...." ; link do streamu


  def parserPUTLOCKER(self,url):
    link = self.requestData(url)    
    r = re.search('value="(.+?)" name="fuck_you"', link)
    if r:
      if DEBUG: log.info("hash: " + r.group(1))
      postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
      data = urllib.urlencode(postdata)
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
    link = self.requestData(url)    
    match = re.compile('value="config=(.+?)">').findall(link)
    if len(match) > 0:
      p = match[0].split('=')
      url = "http://megustavid.com/media/nuevo/player/playlist.php?id=" + p[1]
      if DEBUG: log.info("newlink: " + url)     
      link = self.requestData(url)      
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
    link = self.requestData(url)
    if DEBUG: log.info(link)
    match = re.compile("""url: ["'](.+?)["'],.+?provider:""").findall(link)
    if len(match) > 0:
      if DEBUG: log.info("final link: " + match[0])
      ret = match[0]
    else:
     ret = False
    return ret


  def parserSPROCKED(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    match = re.search("""url: ['"](.+?)['"],.*\nprovider""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))       
      return match.group(1)
    else: 
      return False


  def parserODSIEBIE(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    (v_ext, v_file, v_dir, v_port, v_host) = re.search("\|\|.*SWFObject",link).group().split('|')[40:45]
    url = "http://%s.odsiebie.pl:%s/d/%s/%s.%s" % (v_host, v_port, v_dir, v_file, v_ext);
    return url


  def parserWGRANE(self,url):
    hostUrl = 'http://www.wgrane.pl'            
    playlist = hostUrl + '/html/player_hd/xml/playlist.php?file='
    key = url[-32:]
    nUrl = playlist + key
    if DEBUG: log.info("playlist: " + nUrl)
    link = self.requestData(nUrl)
    if DEBUG: log.info(link)
    match = re.search("""<mainvideo url=["'](.+?)["']""",link)
    if match:
      ret = match.group(1).replace('&amp;','&')
      if DEBUG: log.info("final link: " + ret)
      return ret
    else: 
      return False


  def parserCDA(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    match = re.search("""file: ['"](.+?)['"],""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))       
      return match.group(1)
    else: 
      return False


  def parserNOVAMOV(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    match = re.search("""file: ['"](.+?)['"],""",link)
    if match:
      if DEBUG: log.info("final link: " + match.group(1))       
      return match.group(1)
    else: 
      return False



  def parserDWN(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    #<iframe src="http://dwn.so/player/embed.php?v=DS301459CC&width=850&height=440"
    match = re.search("""<iframe src="(.+?)&""",link)
    if match:
      link = self.requestData(match.group(1))
      if DEBUG: log.info(link)  

    else: 
      return False


  def parserANYFILES(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    match = re.search("""<meta property="og:video" content=['"](.+?)['"].*>""",link)
    if match:
      return match.group(1)
    else: 
      return False


  def parserWOOTLY(self,url):
    link = self.requestData(url)
    if DEBUG: log.info(link)
    #c.value="9ee163b21f5b018544e977cf1fe87569231e4816";
    c = re.search("""c.value="(.+?)";""",link)
    log.info("match: " +str(c.group(1)))
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

  def parserMAXVIDEO(self, url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', HOST)
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      #if DEBUG: log.info(link)
      #eval(unescape('%76%61%72%20%6C%6E%6B%20%3D%20%75%6E%65%73%63%61%70%65%28%63%68%65%63%6B%6C%6E%74%28%75%6E%65%73%63%61%70%65%28%27%25%32%35%36%38%25%32%35%37%34%25%32%35%37%34%25%32%35%37%30%25%32%35%33%66%25%32%35%32%61%25%32%35%32%61%25%32%35%37%33%25%32%35%33%31%25%32%35%32%45%25%32%35%36%78%25%32%35%36%31%25%32%35%37%38%25%32%35%37%36%25%32%35%36%39%25%32%35%36%34%25%32%35%36%35%25%32%35%36%61%25%32%35%32%45%25%32%35%37%30%25%32%35%36%7A%25%32%35%32%61%25%32%35%37%33%25%32%35%37%34%25%32%35%37%32%25%32%35%36%35%25%32%35%36%31%25%32%35%36%78%25%32%35%32%61%25%32%35%33%33%25%32%35%36%34%25%32%35%33%39%25%32%35%33%37%25%32%35%33%31%25%32%35%33%35%25%32%35%36%32%25%32%35%36%31%25%32%35%33%36%25%32%35%33%31%25%32%35%33%31%25%32%35%33%32%25%32%35%33%34%25%32%35%33%33%25%32%35%36%31%25%32%35%36%33%25%32%35%33%33%25%32%35%33%39%25%32%35%36%32%25%32%35%33%39%25%32%35%33%30%25%32%35%33%36%25%32%35%33%39%25%32%35%33%33%25%32%35%33%35%25%32%35%33%39%25%32%35%33%37%25%32%35%36%33%25%32%35%33%39%25%32%35%36%36%25%32%35%36%33%25%32%35%36%34%25%32%35%33%37%25%32%35%33%38%25%32%35%33%37%25%32%35%36%33%25%32%35%33%31%25%32%35%36%35%25%32%35%33%39%25%32%35%36%35%25%32%35%33%34%25%32%35%33%32%25%32%35%33%39%25%32%35%36%34%25%32%35%33%38%25%32%35%36%34%25%32%35%33%35%25%32%35%36%31%25%32%35%36%32%25%32%35%36%36%25%32%35%33%32%25%32%35%33%33%25%32%35%33%34%25%32%35%33%39%25%32%35%36%31%25%32%35%33%31%25%32%35%36%31%25%32%35%36%32%25%32%35%33%33%25%32%35%36%31%25%32%35%33%31%25%32%35%36%36%25%32%35%33%34%25%32%35%36%31%25%32%35%32%61%25%32%35%36%36%25%32%35%36%39%25%32%35%36%7A%25%32%35%36%35%25%32%35%32%45%25%32%35%36%36%25%32%35%36%7A%25%32%35%37%36%27%29%29%29%3B'));
      match1 = re.compile('eval\(unescape\((.+?)\)\)').findall(link)
      if len(match1) > 0:
          str1 = urllib.unquote(match1[0])
          if 'var lnk' in str1:
              tab = str1.split(" = ")
              match2 = re.compile('unescape\(checklnt\(unescape\((.+?)\)\)\)').findall(tab[1])
              if len(match2) > 0:
                  txt1 = match2[0].replace("'", "")
                  str2 = urllib.unquote(urllib.unquote(txt1))
                  if DEBUG: log.info("final link: " + self.replaceString(str2))
                  return self.replaceString(str2)
              else:
                  return False
          else:
              return False  
      else:
          return False