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


MENU_TAB = [ [ "ESKA TV", "rtmp://46.105.112.212:1935/live playpath=mpegts.stream swfUrl=http://www.eska.tv/thrdparty/flowplayer/flowplayer.rtmp-3.1.4.swf pageUrl=http://www.eska.tv/player  live=true swfVfy=true" ],
             [ "Interia TV", "mms://streamlive.interia.pl/interiatv400" ],
             [ "iTVP", "mms://stream.mni.pl/ITV" ],
             [ "Oczko tv", "rtmp://stream7.idnes.cz/live/ playpath=ocko swfUrl=http://g.idnes.cz/swf/flv/player.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=194  live=true swfVfy=true" ],
             [ "Rebel.tv", "rtmp://46.105.108.166:80/publishlive?play=123452 playpath=rebeltv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=405  live=true swfVfy=true" ],
             [ "Tele 5", "http://dcs-193-111-38-246.atmcdn.pl/streams/o2/Antel/antel.livx" ],
             [ "Trwam", "http://195.94.205.211/Trwam" ],
             [ "TV Biznes", "http://dcs-193-111-38-248.atmcdn.pl/streams/o2/TVBiznes/TVbiznes.livx" ],
             [ "TVN", "http://89.191.147.33/3" ],
             [ "TVN24 [chello]", "mms://stream.livetv.chello.pl/TVN24" ],
             [ "TVN TURBO [BEZ REKLAM]", "rtmp://adm.live.tvtp.pl/TVNTurbo/ playpath=tv swfUrl=http://www.tvtp.pl/player/player_o_video.swf?pUrl=tvnturbo_c.e9baa14091ebd631a7a7d03445c18c18&allowfullscreen=true&pAutoplay=1&pStreaming=11 pageUrl=http://www.tvtp.pl/player/player_o_video.swf?pUrl=tvnturbo_c.e9baa14091ebd631a7a7d03445c18c18&allowfullscreen=true&pAutoplay=1&pStreaming=11  live=true swfVfy=true" ] ]


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