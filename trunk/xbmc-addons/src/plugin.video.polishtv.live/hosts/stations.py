# -*- coding: utf-8 -*-
import string, sys
import os, time
import xbmcgui, xbmcplugin, xbmcaddon

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog

log = pLog.pLog()


MENU_TAB = [ [ "ESKA TV", "mms://streamtv.eska.pl:6000/eskatv" ],
             [ "Interia TV", "mms://streamlive.interia.pl/interiatv400" ],
             [ "iTVP", "mms://stream.mni.pl/ITV" ],
             [ "Trwam", "http://195.94.205.211/Trwam" ],
             [ "TVN", "http://89.191.147.33/3" ],
             [ "TVN24 [chello]", "mms://stream.livetv.chello.pl/TVN24" ] ]


class StreamStations:
    #def __init__(self):
    

    def showStations(self):
        #MENU_TAB.sort()
        for i in range(len(MENU_TAB)):
            self.addLink(MENU_TAB[i][0], MENU_TAB[i][1])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def addLink(self, title, url):
        u = url
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage="DefaultVideo.png")
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
        
    def handleService(self):
        self.showStations()