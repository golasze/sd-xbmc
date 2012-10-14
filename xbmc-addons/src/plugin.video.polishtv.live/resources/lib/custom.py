# -*- coding: utf-8 -*-

'''
make sure XBMC has write access to <destination> 
example XML file:
<custom id="plugin.video.polishtv.live">
	<file>
		<source>c:\default.py</source>
		<destination>default.py</destination></file>
	<file>
		<source>http://domain.com/iplex.py</source>
		<destination>hosts/iplex.py</destination>
	</file>
</custom>
'''

import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcaddon, xbmc, xbmcgui
from xml.dom.minidom import parseString, parse

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

HOST = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'

custom_update = ptv.getSetting('default_customupdate')

  
class CustomUpdate:
  def __init__(self):
    print "starting Custom Update"
    self.customUpdate()


  def requestData(self, url):
    if 'http://' in url:
      try: 	
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
      except:
        data=''
    else:
      try:
        f = open(url, 'r')
        data = f.read()
        f.close()
      except:
	data = '' 	
    return data


  def getText(self, nodelist):
    rc = []
    for node in nodelist:
      if node.nodeType == node.TEXT_NODE:
        rc.append(node.data)
      return ''.join(rc)


  def readUpdateFile(self, url):
    strTab = []
    outTab = []
    data = self.requestData(url)
      
    if len(data) > 0:
      d = parseString(data)
      for node in d.getElementsByTagName('file'):
	source = node.getElementsByTagName('source')[0]
	destination = node.getElementsByTagName('destination')[0]
        strTab.append(self.getText(source.childNodes))
        strTab.append(self.getText(destination.childNodes))
        outTab.append(strTab)
	strTab = []
    print str(outTab)
    return outTab


  def writeFiles(self, strTab):
    for file in strTab:
      source = self.requestData(file[0])
      f = open(ptv.getAddonInfo('path') + os.path.sep  + file[1], 'w')
      f.write(source)
      f.close
	
	
  def customUpdate(self):
    if custom_update<>'':
      xbmc.executebuiltin("XBMC.Notification(Please Wait!,Running Custom Update,2000)")
      updateData = self.readUpdateFile(custom_update)
      if len(updateData) > 0:
        self.writeFiles(updateData)
      else:
        d = xbmcgui.Dialog()
        d.ok('Błąd pliku custom_update', 'Plik ma nieprawidlowy format lub nie istnieje', custom_update)
    else:
      d = xbmcgui.Dialog()
      d.ok('Błąd pliku custom_update', 'Brak sciezki do pliku XML')


CustomUpdate() 