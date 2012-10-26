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
            [ "Óčko TV", "rtmp://194.79.52.79/ockoi/ockoHQ1" ],  
            [ "TVN", "rtmp://198.105.217.36/live/telewizyjka_pl_mix_?id=119553" ],
            [ "Polsat", "rtmp://75.126.203.130/stream/darmowatelewizjacompolsat?id=59168" ],
            [ "TVP INFO ", "rtmp://freeview.fms.visionip.tv/live/tvnetwork-polskaplus-tvpinfo-hsslive-25f-4x3-SDh?extsessionid=50444e8f09104-69afb3db1bb7434f243177b5996b8af1" ],
            [ "TVP MIX 1", "http://195.245.213.199/Ch0003" ],
            [ "TVP MIX 2", "http://195.245.213.204/Ch0018" ],
            [ "TVP MIX 3", "http://195.245.213.204/Ch0019" ],
            [ "TVP Sport stream 1", "http://195.245.213.204/Ch0002" ],
            [ "TVP Sport stream 2", "http://195.245.213.204/Ch0006" ],
            [ "TVP Sport stream 3", "http://195.245.213.204/Ch0001" ],
            [ "orange sport", "rtmp://cdn.rtmp.tp.pl/orangecontent_s4/fmlestream" ],
            [ "Trwam", "http://195.94.205.211/Trwam" ],
            [ "Word of God", "mms://media.WordofGod.gr/WordofGod150PL" ],
            [ "Christus Vincit ", "http://82.160.147.122/pustelnia" ],
            [ "EduSat", "rtmp://178.73.10.66:1935/live/mpegts.stream" ],
            [ "iTV", "mms://stream.mni.pl/ITV" ],
            [ "Kosmica TV", "rtmp://streamserver.smartcast.de/kosmicaber/kosmicaber.stream" ],
            [ "Pomerania TV", "mms://pomerania.tv:8080/" ],
            [ "Telewizja sudecka", "mms://82.139.8.249/sudecka" ],
            [ "Dami Radom", "mms://82.139.8.249/dami/" ],
            [ "TV Kujawy", "http://77.91.63.211:8090/stream.flv" ],
            [ "TV Narew", "http://93.105.142.26:2525/" ],
            [ "TOYA ", "http://217.113.224.22/TVToya" ],
            [ "RTV Lubuska", "rtmp://94.23.0.87/bankier/rtl" ],
            [ "TV Asta ", "http://xeon.asta-net.pl/tvasta" ],
            [ "CW24TV", "rtmp://cdn4.stream360.pl:1935/CW24/transmisja_live" ],
            [ "Tawizja", "rtmp://wwz1.4vod.tv:1935/4vod-rtp/tawizja.stream " ],
            [ "Dla Ciebie.Tv", "rtsp://mediaserver02.artcom.pl/live/DlaCiebieTv800.stream" ],        
            [ "Telewizja lubuszan", "rtmp://212-112.livestream.com:80/mogulus-stream-edge/tllive/rtmp://212-47.livestream.com/mogulus/tllive/1da1455e-f1ad-47bb-b019-d8a0099bd196" ],
            [ "TiWi", "rtmp://extondemand.livestream.com:80/ondemand/trans/dv02/mogulus-user-files/chv2tivinet/2009/05/11/b4ae4fc2-a938-488b-9731-cb93278a10ad" ],
            [ "Panorama Polska", "rtmp://extondemand.livestream.com/ondemand/trans/dv03/mogulus-user-files/chpanoramapolska/2010/01/07/5825602e-bdd1-490f-8680-4054c7db78ca" ],
            [ "Zdrowy Puls", "rtmp://extondemand.livestream.com/ondemand/trans/dv15/mogulus-user-files/chzdrowypuls/2012/04/04/15bbcc6c-30dc-4f08-91ca-b14dc40bbe3a" ],
#           [ "SKY NEWS", "mms://194.88.72.17:1755/skynews_wmlz_live300k" ],
#           [ "CNN", "rtsp://media2.lsops.net:554/live/cnn_en_medium.sdp" ],
#           [ "Russia Today", "rtmp://fms5.visionip.tv/live/RT_3" ],
#           [ "3Sat", "rtsp://a62.l12560554061.c125605.g.lm.akamaistream.net/D/62/125605/v0001/reflector:54061" ],
#           [ "The Voice", "http://62.41.56.32:80/PUBLIC_votv_fi" ],
#           [ "France 24 FR ", "http://stream1.france24.yacast.net/f24_livefr" ],
#           [ "France 24 ANG ", "http://stream1.france24.yacast.net/f24_liveen" ],
#           [ "ČT24 ", "rtmp://wcdn42.nacevi.cz:80/CT24?id=HRydF7MABFzyrU7&publisher=lss/CT24-MP4_576p.stream" ],
#             [ "Publika TV", "rtmp://91.230.214.56/publika/livepublika1" ],
#            [ "Big Pond Sport ", "http://cht-cdn220-is-12.se.bptvlive.ngcdn.telstra.com/bp_online_bpsport_high" ],
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
