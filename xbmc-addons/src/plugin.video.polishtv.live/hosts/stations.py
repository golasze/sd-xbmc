# -*- coding: utf-8 -*-
import string, sys
import os, time
import xbmcgui, xbmcplugin, xbmcaddon, xbmc

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, Parser, pCommon

log = pLog.pLog()

CATEGORY_TAB = [
                [0, "Informacjne"],
                [1, "Sportowe"],
                [2, "Muzyczne"],
                [3, "Religijne"],
                [4, "Lokalne"],
                [5, "Ogolnotemetyczne"]
               ]

#           [title, category_id, videoUrl]
MENU_TAB = [  
#           [ "TVP2", 0, "rtsp://balancer.eu.wlacz.tv:1935/live/tvp2.stream" ],
#           [ "TVP2", 0, "rtmp://balancer.eu.wlacz.tv:1935/live/_definst_/atm.stream" ],
            [ "TVN", 0, "rtmp://75.126.203.130/stream/JardelloTV3333?id=59199" ],
            [ "TVN LQ", 0, "rtmp://50.23.115.84/stream/telewizyjka?id=61660" ],
            [ "TVN24", 0, "rtmp://50.23.65.36/stream/JardelloTV1002?id=57604" ],
#           [ "POLSAT", 0, "rtsp://publish.001.wlacz.tv:1935/live/polsat.stream" ],
            [ "POLSAT", 0, "rtmp://198.105.209.124/stream/JardelloTV4343?id=59200" ],
            [ "Polsat LQ", 0, "rtmp://75.126.203.130/stream/darmowatelewizjacompolsat?id=59168" ],
#           [ "TV4", 0, "rtsp://publish.005.wlacz.tv:1935/live/tv4.stream" ],
#           [ "TVN7", 0, "rtsp://publish.001.wlacz.tv:1935/live/polsatsportnews.stream" ],
#           [ "HBO", 0, "rtsp://publish.001.wlacz.tv:1935/live/hbo1.stream" ],
#           [ "TTV", 0, "rtsp://publish.001.wlacz.tv:1935/live/utv.stream" ],
#           [ "ATM Rozrywka", 0, "rtsp://publish.001.wlacz.tv:1935/live/atm.stream" ],
            [ "TVP INFO ", 0, "rtmp://freeview.fms.visionip.tv/live/tvnetwork-polskaplus-tvpinfo-hsslive-25f-4x3-SDh?extsessionid=50444e8f09104-69afb3db1bb7434f243177b5996b8af1" ],
            [ "TVP MIX 1", 0, "http://195.245.213.199/Ch0003" ],
            [ "TVP MIX 2", 0, "http://195.245.213.204/Ch0018" ],
            [ "TVP MIX 3", 0, "http://195.245.213.204/Ch0019" ],
            [ "Nick jr.", 0, "http://95.188.126.233:1234/udp/233.7.70.169:5000" ],
            [ "CanalPlus Sport", 1, "rtmp://94.23.39.164/satlive/channel1 playpath=channel1 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-120.htm  live=true swfVfy=true" ],
            [ "CanalPlus Gol", 1, "rtmp://94.23.39.164/satlive/channel2 playpath=channel2 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-121.htm  live=true swfVfy=true" ],
            [ "Eurosport2", 1, "rtmp://94.23.39.164/satlive/channel5 playpath=channel5 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-124.htm  live=true swfVfy=true" ],
            [ "Polsat Sport", 1, "rtmp://94.23.39.164/satlive/channel3 playpath=channel3 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-122.htm  live=true swfVfy=true" ],
            [ "Sport mix", 1, "rtmp://94.23.39.164/satlive/channel4 playpath=channel4 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-123.htm  live=true swfVfy=true" ],
            [ "Nova Sport", 1, "http://212.79.96.134:8023/" ],
            [ "ČT Sport", 0, "http://212.79.96.134:8014/" ],
            [ "TVP Sport stream 1", 1, "http://195.245.213.204/Ch0002" ],
            [ "TVP Sport stream 2", 1, "http://195.245.213.204/Ch0006" ],
            [ "TVP Sport stream 3", 1, "http://195.245.213.204/Ch0001" ],
            [ "orange sport", 1, "rtmp://cdn.rtmp.tp.pl/orangecontent_s4/fmlestream" ],
            [ "ESKA TV", 2, "rtmp://46.105.112.212:1935/live playpath=mpegts.stream swfUrl=http://www.eska.tv/thrdparty/flowplayer/flowplayer.rtmp-3.1.4.swf pageUrl=http://www.eska.tv/player  live=true swfVfy=true" ],
            [ "Rebel.tv", 2, "rtmp://gdansk.popler.tv:80/publishlive?play=123452/rebeltv playpath=rebeltv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=405  live=true swfVfy=true" ],
            [ "4Fun TV", 2, "rtmp://creyden.popler.tv:80/publishlive?play=123452/4funtv playpath=4funtv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=55  live=true swfVfy=true" ],
            [ "NEXT Music", 2, "rtmp://vod.wowza.astrosa.pl/rtplive/:music_540p.stream" ],
            [ "Deluxe Music", 2, "rtmp://flash.cdn.deluxemusic.tv/deluxemusic.tv-live/web_850.stream" ],
            [ "TV Disco", 2, "rtmp://gdansk.popler.tv:80/publishlive?play=123452/tvdisco playpath=tvdisco swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=55  live=true swfVfy=true" ],
            [ "Polo TV", 2, "rtmp://stream1.polotv.com.pl/polotv/stream1" ],
            [ "Tuba TV", 2, "rtmp://fms.gazeta.pl/aglive/tuba_tv playpath=tuba_tv swfUrl=http://bi.gazeta.pl/im/Player.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=358  live=true swfVfy=true" ],
            [ "Czwórka Polskie Radio", 2, "rtmp://stream85.polskieradio.pl/video/czworka.sdp" ],
            [ "Kiss TV", 2, "rtmp://kisstelevision.es.flash3.glb.ipercast.net/kisstelevision.es-live/live" ],
            [ "CT.Fm", 0, "rtmp://80.245.113.12/live/pubtalk2?ctfm&ctfm2012pgp" ],
            [ "Óčko TV", 0, "rtmp://194.79.52.79/ockoi/ockoHQ1" ],  
            [ "Trwam", 3, "http://195.94.205.211/Trwam" ],
            [ "Word of God", 3, "mms://media.WordofGod.gr/WordofGod150PL" ],
            [ "Christus Vincit ", 3, "http://82.160.147.122/pustelnia" ],
            [ "EduSat", 0, "rtmp://178.73.10.66:1935/live/mpegts.stream" ],
            [ "iTV", 0, "mms://stream.mni.pl/ITV" ],
            [ "Kosmica TV", 0, "rtmp://streamserver.smartcast.de/kosmicaber/kosmicaber.stream" ],
            [ "Pomerania TV", 0, "mms://pomerania.tv:8080/" ],
            [ "Telewizja sudecka", 4, "mms://82.139.8.249/sudecka" ],
            [ "Dami Radom", 4, "mms://82.139.8.249/dami/" ],
            [ "TV Kujawy", 4, "http://77.91.63.211:8090/stream.flv" ],
            [ "TV Narew", 4, "http://93.105.142.26:2525/" ],
            [ "TV Toruń ", 4, "http://217.173.176.107:1935/live/ngrp:tvk.stream_all/chunklist-b1399547.m3u8?wowzasessionid=1841105475" ],
            [ "TOYA ", 4, "http://217.113.224.22/TVToya" ],
            [ "RTV Lubuska", 4, "rtmp://94.23.0.87/bankier/rtl" ],
            [ "TV Asta ", 0, "http://xeon.asta-net.pl/tvasta" ],
            [ "CW24TV", 0, "rtmp://cdn4.stream360.pl:1935/CW24/transmisja_live" ],
            [ "Tawizja", 0, "rtmp://wwz1.4vod.tv:1935/4vod-rtp/tawizja.stream " ],
            [ "Dla Ciebie.Tv", 0, "rtsp://mediaserver02.artcom.pl/live/DlaCiebieTv800.stream" ],        
            [ "Telewizja lubuszan", 0, "rtmp://212-112.livestream.com:80/mogulus-stream-edge/tllive/rtmp://212-47.livestream.com/mogulus/tllive/1da1455e-f1ad-47bb-b019-d8a0099bd196" ],
            [ "TiWi", 0, "rtmp://extondemand.livestream.com:80/ondemand/trans/dv02/mogulus-user-files/chv2tivinet/2009/05/11/b4ae4fc2-a938-488b-9731-cb93278a10ad" ],
            [ "Panorama Polska", 0, "rtmp://extondemand.livestream.com/ondemand/trans/dv03/mogulus-user-files/chpanoramapolska/2010/01/07/5825602e-bdd1-490f-8680-4054c7db78ca" ],
            [ "Zdrowy Puls", 0, "rtmp://extondemand.livestream.com/ondemand/trans/dv15/mogulus-user-files/chzdrowypuls/2012/04/04/15bbcc6c-30dc-4f08-91ca-b14dc40bbe3a" ],
#           [ "SKY NEWS", "mms://194.88.72.17:1755/skynews_wmlz_live300k" ],
#           [ "BBC World News HD", "http://212.79.96.134:8011/" ],
#           [ "BBC 1", "rtsp://195.90.118.93/bbc1_1" ],
#           [ "BBC 2", "rtsp://195.90.118.93/bbc2_1" ],
#           [ "CBBC", "rtsp://195.90.118.93/CBBC_1" ],
#           [ "EuroNews", "http://212.79.96.134:8013/" ],
#           [ "Pro7", "http://212.79.96.134:8009/" ],
#           [ "Rtl", "http://212.79.96.134:8008/" ],
#           [ "Sat1", "http://212.79.96.134:8010/" ],
#           [ "LTV 1", "http://82.135.235.37:80/LTV" ],
#           [ "LTV World", "http://82.135.235.37:80/LTVworld" ],
#           [ "MTV Россия", "http://77.91.77.19:7015/?sid=" ],
#           [ "CNN", "rtsp://media2.lsops.net:554/live/cnn_en_medium.sdp" ],
#           [ "Russia Today", "rtmp://fms5.visionip.tv/live/RT_3" ],
#           [ "3Sat", "rtsp://a62.l12560554061.c125605.g.lm.akamaistream.net/D/62/125605/v0001/reflector:54061" ],
#           [ "The Voice", "http://62.41.56.32:80/PUBLIC_votv_fi" ],
#           [ "France 24 FR ", "http://stream1.france24.yacast.net/f24_livefr" ],
#           [ "France 24 ANG ", "http://stream1.france24.yacast.net/f24_liveen" ],
#           [ "ČT24 ", "rtmp://wcdn42.nacevi.cz:80/CT24?id=HRydF7MABFzyrU7&publisher=lss/CT24-MP4_576p.stream" ],
#           [ "Publika TV", "rtmp://91.230.214.56/publika/livepublika1" ],
#           [ "Big Pond Sport ", "http://cht-cdn220-is-12.se.bptvlive.ngcdn.telstra.com/bp_online_bpsport_high" ],
            [ "TVN24 [chello]", 0, "mms://stream.livetv.chello.pl/TVN24" ],
            [ "TVN TURBO [BEZ REKLAM]", 0, "rtmp://adm.live.tvtp.pl/TVNTurbo/ playpath=tv swfUrl=http://www.tvtp.pl/player/player_o_video.swf?pUrl=tvnturbo_c.e9baa14091ebd631a7a7d03445c18c18&allowfullscreen=true&pAutoplay=1&pStreaming=11 pageUrl=http://www.tvtp.pl/player/player_o_video.swf?pUrl=tvnturbo_c.e9baa14091ebd631a7a7d03445c18c18&allowfullscreen=true&pAutoplay=1&pStreaming=11  live=true swfVfy=true" ],
            [ "Poslkie stacje radiowe", 0, "http://xbmc.cba.pl/zbmc/onair.m3u" ],
              ]


class StreamStations:
    def __init__(self):
        self.parser = Parser.Parser()
        self.cm = pCommon.common()
    

    def showStations(self, catID):
        MENU_TAB.sort(key = lambda x: x[0])
        for i in range(len(MENU_TAB)):
            if MENU_TAB[i][1]==int(catID):
                self.add('stations', MENU_TAB[i][0], 'None', False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def showCategories(self):
        CATEGORY_TAB.sort(key = lambda x: x[1])
        for i in range(len(CATEGORY_TAB)):
            self.add('stations', CATEGORY_TAB[i][1], str(CATEGORY_TAB[i][0]))
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def add(self, service, name, val, folder = True, isPlayable = False):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&val=" + val 
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)


    def getVideoLink(self, name):
        nUrl = ""
        for i in range(len(MENU_TAB)):
            if MENU_TAB[i][0]==name:
                nUrl = MENU_TAB[i][2]
        return nUrl                
            
       
    def LOAD_AND_PLAY_VIDEO(self, videoUrl):
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoUrl)

       
    def handleService(self):
        params = self.parser.getParams()
        name = str(self.parser.getParam(params, "name"))
        val = str(self.parser.getParam(params, "val"))
        log.info("name: " + name)
        log.info("val: " + val)
        
        if name == 'None':
            self.showCategories()
        else:
            if self.cm.isNumeric(val):
                self.showStations(val)
            else:
                url = self.getVideoLink(name)
                self.LOAD_AND_PLAY_VIDEO(url)
