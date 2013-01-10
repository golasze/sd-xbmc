# -*- coding: utf-8 -*-

import string, StringIO
import os
import re, sys
import xbmcaddon, xbmc, xbmcgui
from xml.dom.minidom import parseString, parse
import traceback

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

import pCommon, pLog, Errors

log = pLog.pLog()
dbg = ptv.getSetting('default_debug')

STATUSURL = 'http://sd-xbmc.org/xbmc/servicestatus.xml'
#get actioncodes from keymap.xml

ACTION_ALL = 111
ACTION_ONLINE = 112
ACTION_WORK = 113
ACTION_OFFLINE = 114
ACTION_EXIT = 117
ACTION_LIST = 120

  
class ServiceInfo:
    def __init__(self):
        print "starting Service Info"
        self.common = pCommon.common()
        self.exception = Errors.Exception()
   
    
    def getServiceInfo(self):
        strTab = []
        outTab = []
        query_data = {'url': STATUSURL, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True}
        try:    
            data = self.common.getURLRequestData(query_data)
        except Exception, exception:
            traceback.print_exc()
            self.exception.getError(str(exception))
            exit()
  
        if len(data) > 0:
            try:
                d = parseString(data)
                for node in d.getElementsByTagName('service'):
                    status = node.getElementsByTagName('status')[0]
                    date = node.getElementsByTagName('date')[0]
                    description = node.getElementsByTagName('description')[0]
                    if self.getText(status.childNodes) != None:
                        strTab.append(node.attributes.items()[1][1])
                        strTab.append(self.getText(status.childNodes))
                        strTab.append(self.getText(date.childNodes))
                        strTab.append(self.getText(description.childNodes))
                        outTab.append(strTab)
                        strTab = []
            except Exception, exception:
                traceback.print_exc()
                self.exception.getError(str(exception))
                exit()
        return outTab 
  
    
    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
            return ''.join(rc)


    def getWindow(self):
        mydisplay = WindowServiceInfo("ServiceInfo.xml", ptv.getAddonInfo('path'), "Default")
        mydisplay .doModal()
        del mydisplay


class WindowServiceInfo(xbmcgui.WindowXMLDialog):
    def __init__(self, strXMLname, strFallbackPath, strDefaultName, forceFallback = True):
        self.si = ServiceInfo()
        self.sTab = self.si.getServiceInfo()
        #self.list = {}      
       
    def onInit(self):
        if dbg == 'true':
            log.info('ServiceInfo - WindowServiceInfo()[onInit] -> table: ' + str(self.sTab))
        self.generateListItem(ACTION_ALL)
    
    def onAction(self, action):
        if action == 1001:
            self.close()
        elif action == 1002:
            self.generateListItem(ACTION_ALL)
        elif action == 1003:
            self.generateListItem(ACTION_WORK)
        elif action == 1004:
            self.generateListItem(ACTION_OFFLINE)
        elif action == 1005:
            self.generateListItem(ACTION_ONLINE)
        
    
    def onClick(self, controlID):
        if controlID == ACTION_EXIT:
            self.onAction(1001)
        elif controlID == ACTION_ALL:
            self.onAction(1002)
        elif controlID == ACTION_WORK:
            self.onAction(1003)
        elif controlID == ACTION_OFFLINE:
            self.onAction(1004)
        elif controlID == ACTION_ONLINE:
            self.onAction(1005)
    
    def onFocus(self, controlID):
        pass
     
    def generateListItem(self, id):
        if dbg == 'true':
            log.info('ServiceInfo - WindowServiceInfo()[generateListItem] -> action id: ' + str(id))
        list = self.getControl(ACTION_LIST)
        list.reset()
        if len(self.sTab) > 0:
            for i in range(len(self.sTab)):
                nameS = self.sTab[i][0]
                statusS = self.sTab[i][1]
                dateS = self.sTab[i][2]
                descS = self.sTab[i][3]
                descR = '[I]' + descS + '[/I]'
                if id == ACTION_ALL:
                    statusR = '[I][COLOR green]' + statusS + '[/COLOR][/I]'
                    descR = '[I]' + descS + '[/I]'
                    if statusS == 'OFFLINE':
                        statusR = '[I][COLOR red]' + statusS + '[/COLOR][/I]'
                    elif statusS == 'WORKAROUND':
                        statusR = '[I][COLOR yellow]' + statusS + '[/COLOR][/I]'
                    info = "%s (%s, %s)" % ('[B][COLOR blue]' + nameS + '[/COLOR][/B]', statusR, dateS)
                    l = xbmcgui.ListItem(label = info, label2 = descR)
                    list.addItem(l)    
                elif id == ACTION_WORK:
                    if statusS == 'WORKAROUND':
                        statusR = '[I][COLOR yellow]' + statusS + '[/COLOR][/I]'
                        info = "%s (%s, %s)" % ('[B][COLOR blue]' + nameS + '[/COLOR][/B]', statusR, dateS)
                        l = xbmcgui.ListItem(label = info, label2 = descR)
                        list.addItem(l)
                elif id == ACTION_OFFLINE:
                    if statusS == 'OFFLINE':
                        statusR = '[I][COLOR red]' + statusS + '[/COLOR][/I]'
                        info = "%s (%s, %s)" % ('[B][COLOR blue]' + nameS + '[/COLOR][/B]', statusR, dateS)
                        l = xbmcgui.ListItem(label = info, label2 = descR)
                        list.addItem(l)
                elif id == ACTION_ONLINE:
                    if statusS == 'ONLINE':
                        statusR = '[I][COLOR green]' + statusS + '[/COLOR][/I]'
                        info = "%s (%s, %s)" % ('[B][COLOR blue]' + nameS + '[/COLOR][/B]', statusR, dateS)
                        l = xbmcgui.ListItem(label = info, label2 = descR)
                        list.addItem(l)                    