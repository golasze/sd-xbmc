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
            [ "Rebel.tv", "rtmp://gdansk.popler.tv:80/publishlive?play=123452/rebeltv playpath=rebeltv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=405  live=true swfVfy=true" ],
            [ "4Fun TV", "rtmp://creyden.popler.tv:80/publishlive?play=123452/4funtv playpath=4funtv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=55  live=true swfVfy=true" ],
            [ "NEXT Music", "rtmp://vod.wowza.astrosa.pl/rtplive/:music_540p.stream" ],
            [ "Deluxe Music", "rtmp://flash.cdn.deluxemusic.tv/deluxemusic.tv-live/web_850.stream" ],
            [ "Polo TV", "rtmp://stream1.polotv.com.pl/polotv/stream1" ],
            [ "Tuba TV", "rtmp://fms.gazeta.pl/aglive/tuba_tv playpath=tuba_tv swfUrl=http://bi.gazeta.pl/im/Player.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=358  live=true swfVfy=true" ],
            [ "Czwórka Polskie Radio", "rtmp://stream85.polskieradio.pl/video/czworka.sdp" ],
            [ "Kiss TV", "rtmp://kisstelevision.es.flash3.glb.ipercast.net/kisstelevision.es-live/live" ],
            [ "CT.Fm", "rtmp://80.245.113.12/live/pubtalk2?ctfm&ctfm2012pgp" ],
            [ "Trwam", "http://195.94.205.211/Trwam" ],
            [ "EduSat", "rtmp://178.73.10.66:1935/live/mpegts.stream" ],
            [ "iTV", "mms://stream.mni.pl/ITV" ],
             [ "Pomerania TV", "mms://pomerania.tv:8080/" ],
             [ "Telewizja sudecka", "mms://82.139.8.249/sudecka" ],
             [ "Dami Radom", "mms://82.139.8.249/dami/" ],
             [ "TV Kujawy", "http://77.91.63.211:8090/stream.flv" ],
             [ "TV Narew", "http://93.105.142.26:2525/" ],
             [ "TOYA ", "http://217.113.224.22/TVToya" ],
             [ "TV Astra ", "http://xeon.asta-net.pl/tvasta" ],
             [ "CW24TV", "rtmp://cdn4.stream360.pl:1935/CW24/transmisja_live" ],
             [ "Telewizja lubuszan", "rtmp://212-104.livestream.com/mogulus-stream-edge/tllive/rtmp://212-97.livestream.com/mogulus/tllive/40c823ce-648b-44cd-9596-d5f4d6d31c8d" ],
             [ "TiWi", "rtmp://extondemand.livestream.com:80/ondemand/trans/dv02/mogulus-user-files/chv2tivinet/2009/05/11/b4ae4fc2-a938-488b-9731-cb93278a10ad" ],
              [ "Panorama Polska", "rtmp://extondemand.livestream.com/ondemand/trans/dv03/mogulus-user-files/chpanoramapolska/2010/01/07/5825602e-bdd1-490f-8680-4054c7db78ca" ],
             [ "Zdrowy Puls", "rtmp://extondemand.livestream.com/ondemand/trans/dv15/mogulus-user-files/chzdrowypuls/2012/04/04/15bbcc6c-30dc-4f08-91ca-b14dc40bbe3a" ],
             [ "Oczko tv", "rtmp://stream7.idnes.cz/live/ocko playpath=ocko swfUrl=http://g.idnes.cz/swf/flv/player.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=194  live=true swfVfy=true" ],
#             [ "SKY NEWS", "mms://194.88.72.17:1755/skynews_wmlz_live300k" ],
#             [ "CNN", "rtsp://media2.lsops.net:554/live/cnn_en_medium.sdp" ],
#             [ "Russia Today", "rtmp://fms5.visionip.tv/live/RT_3" ],

              
#             [ "3Sat", "rtsp://a62.l12560554061.c125605.g.lm.akamaistream.net/D/62/125605/v0001/reflector:54061" ],
             
            
#             [ "The Voice", "http://62.41.56.32:80/PUBLIC_votv_fi" ],
             

             
             
#             [ "Publika TV", "rtmp://91.230.214.56/publika/livepublika1" ],
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
