# -*- coding: utf-8 -*-
import os, urllib, urllib2, re, sys, math

tmp_path = os.getenv("HOME") + '/.xbmc/addons/plugin.video.polishtv.live/tmp'


def tmpFile():
  return tmp_path + '/movie.tmp'


def getTMPFile(url):
  #file_name = url.split('/')[-1]
  file_name = tmpFile()
  u = urllib2.urlopen(url)
  f = open(file_name, 'w')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)

  file_size_dl = 0
  block_sz = 8192
  while True:
      buffer = u.read(block_sz)
      if not buffer:
	  break

      file_size_dl += block_sz
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,
  f.close()

getTMPFile('http://www1235.megavideo.com/files/34720761c95577dd4411585e16a41e4f/?.flv')