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
                [0, "Ogólnotematyczne"],
                [1, "Informacyjne"],
                [2, "Sportowe"],
                [3, "Muzyczne"],
                [4, "Religijne"],
                [5, "Lokalne"],
                [6, "Zagraniczne"],
                [7, "Polskie stacje radiowe"],
                [8, "Okiem Kamery"]
               ]

#           [title, category_id, videoUrl]
MENU_TAB = [  
            [ "TVN stream2", 0, "rtmp://94.23.39.164/satlive/tvn playpath=tvn swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-127.htm  live=true swfVfy=true" ],
            [ "ATM Rozrywka", 0, "rtmp://creyden.popler.tv:80/rtplive?play=123452/fdg4324" ],
            [ "TVP2", 0, "rtmp://94.23.39.164/satlive/tvp2 playpath=tvp2 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-131.htm  live=true swfVfy=true" ],
            [ "TVN", 0, "rtmp://75.126.203.130/stream/JardelloTV3333?id=59199" ],
            [ "Polsat LQ1", 0, "rtmp://50.23.115.84/stream/telewizyjka?id=61660" ],
            [ "TVN24", 1, "rtmp://94.23.39.164/satlive/tvn24 playpath=tvn24 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-129.htm  live=true swfVfy=true" ],
#           [ "POLSAT", 0, "rtsp://publish.001.wlacz.tv:1935/live/polsat.stream" ],
            [ "Polsat", 0, "rtmp://198.105.209.124/stream/JardelloTV4343?id=59200" ],
            [ "Polsat LQ", 0, "rtmp://75.126.203.130/stream/darmowatelewizjacompolsat?id=59168" ],
#           [ "TV4", 0, "rtsp://publish.005.wlacz.tv:1935/live/tv4.stream" ],
#           [ "TVN7", 0, "rtsp://publish.001.wlacz.tv:1935/live/polsatsportnews.stream" ],
#           [ "HBO", 0, "rtsp://publish.001.wlacz.tv:1935/live/hbo1.stream" ],
#           [ "TTV", 0, "rtsp://publish.001.wlacz.tv:1935/live/utv.stream" ],
#           [ "ATM Rozrywka", 0, "rtsp://publish.001.wlacz.tv:1935/live/atm.stream" ],
            [ "TVP1", 0, "rtmp://94.23.39.164/satlive/tvp1 playpath=tvp1 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-126.htm  live=true swfVfy=true" ],
            [ "HBO", 0, "rtmp://94.23.39.164/satlive/hbo playpath=hbo swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-137.htm  live=true swfVfy=true" ],
            [ "Canal Plus Film", 0, "rtmp://94.23.39.164/satlive/canalplusfilm playpath=canalplusfilm swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-132.htm  live=true swfVfy=true" ],

            [ "TVP INFO ", 1, "rtmp://freeview.fms.visionip.tv/live/tvnetwork-polskaplus-tvpinfo-hsslive-25f-4x3-SDh?extsessionid=50444e8f09104-69afb3db1bb7434f243177b5996b8af1" ],
            [ "TVP MIX 1", 0, "http://195.245.213.199/Ch0003" ],
            [ "TVP MIX 2", 0, "http://195.245.213.204/Ch0018" ],
            [ "TVP MIX 3", 0, "http://195.245.213.204/Ch0019" ],
            [ "Nick jr.", 0, "http://95.188.126.233:1234/udp/233.7.70.169:5000" ],
            [ "CanalPlus Sport (satlive.pl)", 2, "rtmp://94.23.39.164/satlive/channel1 playpath=channel1 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-120.htm  live=true swfVfy=true" ],
            [ "CanalPlus Gol (satlive.pl)", 2, "rtmp://94.23.39.164/satlive/channel2 playpath=channel2 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-121.htm  live=true swfVfy=true" ],
            [ "Eurosport2 (satlive.pl)", 2, "rtmp://94.23.39.164/satlive/channel5 playpath=channel5 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-124.htm  live=true swfVfy=true" ],
            [ "Polsat Sport (satlive.pl)", 2, "rtmp://94.23.39.164/satlive/channel3 playpath=channel3 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-122.htm  live=true swfVfy=true" ],
            [ "Sport mix (satlive.pl)", 2, "rtmp://94.23.39.164/satlive/channel4 playpath=channel4 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-123.htm  live=true swfVfy=true" ],
            [ "nSport (satlive.pl)", 2, "rtmp://94.23.39.164/satlive/channel6 playpath=channel6 swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-125.htm  live=true swfVfy=true" ],
            [ "Polsat HD", 0, "rtmp://94.23.39.164/satlive/polsat playpath=polsat swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-128.htm  live=true swfVfy=true" ],

            [ "Nova Sport", 2, "http://212.79.96.134:8023/" ],
            [ "ČT Sport", 2, "http://212.79.96.134:8014/" ],
            [ "TVP Sport stream 1", 2, "http://195.245.213.204/Ch0002" ],
            [ "TVP Sport stream 2", 2, "http://195.245.213.204/Ch0006" ],
            [ "TVP Sport stream 3", 2, "http://195.245.213.204/Ch0001" ],
            [ "TVP Parlament", 1, "http://195.245.213.204/Ch0014" ],
            [ "orange sport", 2, "rtmp://cdn.rtmp.tp.pl/orangecontent_s4/fmlestream" ],
            [ "ESKA TV", 3, "rtmp://46.105.112.212:1935/live playpath=mpegts.stream swfUrl=http://www.eska.tv/thrdparty/flowplayer/flowplayer.rtmp-3.1.4.swf pageUrl=http://www.eska.tv/player  live=true swfVfy=true" ],
            [ "Rebel.tv", 3, "rtmp://gdansk.popler.tv:80/publishlive?play=123452/rebeltv playpath=rebeltv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=405  live=true swfVfy=true" ],
            [ "4Fun TV", 3, "rtmp://creyden.popler.tv:80/publishlive?play=123452/4funtv playpath=4funtv swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=55  live=true swfVfy=true" ],
            [ "NEXT Music", 3, "rtmp://vod.wowza.astrosa.pl:80/rtplive/:music_540p.stream" ],
            [ "Deluxe Music", 3, "rtmp://flash.cdn.deluxemusic.tv/deluxemusic.tv-live/web_850.stream" ],
            [ "TV Disco", 3, "rtmp://gdansk.popler.tv:80/publishlive?play=123452/tvdisco playpath=tvdisco swfUrl=http://www.popler.tv/player/flowplayer.cluster.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=55  live=true swfVfy=true" ],
            [ "Polo TV", 3, "rtmp://stream1.polotv.com.pl/polotv/stream1" ],
            [ "Tuba TV", 3, "rtmp://fms.gazeta.pl/aglive/tuba_tv playpath=tuba_tv swfUrl=http://bi.gazeta.pl/im/Player.swf pageUrl=http://www.megawypas.pl/readarticle.php?article_id=358  live=true swfVfy=true" ],
            [ "Czwórka  Polskie Radio", 3, "rtmp://stream85.polskieradio.pl/video/czworka.sdp" ],
            [ "Kiss TV", 3, "rtmp://kisstelevision.es.flash3.glb.ipercast.net/kisstelevision.es-live/live" ],
            [ "CT.Fm", 3, "rtmp://80.245.113.12/live/pubtalk2?ctfm&ctfm2012pgp" ],
            [ "Óčko TV", 3, "rtmp://194.79.52.79/ockoi/ockoHQ1" ],  
            [ "Trwam", 4, "http://195.94.205.211/Trwam" ],
            [ "Word of God", 4, "mms://media.WordofGod.gr/WordofGod150PL" ],
            [ "Christus Vincit ", 4, "http://82.160.147.122/pustelnia" ],
            [ "EduSat", 0, "rtmp://178.73.10.66:1935/live/mpegts.stream" ],
            [ "iTV", 0, "mms://stream.mni.pl/ITV" ],
            [ "TVBiznes", 1, "http://dcs-188-64-84-12.atmcdn.pl/streams/o2/TVBiznes/TVbiznes.livx playpath=TVbiznes swfUrl=http://cm2.atmitv.pl/ContentManager/swf/Player.swf pageUrl=http://www.tv.jardello.eu/08/5/index.php  live=true swfVfy=true" ],

            [ "Kosmica TV", 0, "rtmp://streamserver.smartcast.de/kosmicaber/kosmicaber.stream" ],
            [ "Pomerania TV", 5, "mms://pomerania.tv:8080/" ],
            [ "Telewizja sudecka", 5, "mms://82.139.8.249/sudecka" ],
            [ "Dami Radom", 5, "mms://82.139.8.249/dami/" ],
            [ "TV Kujawy", 5, "http://77.91.63.211:8090/stream.flv" ],
            [ "TV Narew", 5, "http://93.105.142.26:2525/" ],
            [ "TV Toruń ", 5, "http://217.173.176.107:1935/live/ngrp:tvk.stream_all/chunklist-b1399547.m3u8?wowzasessionid=1841105475" ],
            [ "TOYA ", 5, "http://217.113.224.22/TVToya" ],
            [ "RTV Lubuska", 5, "rtmp://94.23.0.87/bankier/rtl" ],
            [ "TV Asta ", 5, "http://xeon.asta-net.pl/tvasta" ],
            [ "CW24TV", 5, "rtmp://cdn4.stream360.pl:1935/CW24/transmisja_live" ],
            [ "Tawizja", 5, "rtmp://wwz1.4vod.tv:1935/4vod-rtp/tawizja.stream " ],
            [ "Dla Ciebie.Tv", 5, "rtsp://mediaserver02.artcom.pl/live/DlaCiebieTv800.stream" ],        
            [ "Telewizja lubuszan", 5, "rtmp://212-112.livestream.com:80/mogulus-stream-edge/tllive/rtmp://212-47.livestream.com/mogulus/tllive/1da1455e-f1ad-47bb-b019-d8a0099bd196" ],
            [ "TiWi", 0, "rtmp://extondemand.livestream.com:80/ondemand/trans/dv02/mogulus-user-files/chv2tivinet/2009/05/11/b4ae4fc2-a938-488b-9731-cb93278a10ad" ],
            [ "Panorama Polska", 0, "rtmp://extondemand.livestream.com/ondemand/trans/dv03/mogulus-user-files/chpanoramapolska/2010/01/07/5825602e-bdd1-490f-8680-4054c7db78ca" ],
            [ "Zdrowy Puls", 0, "rtmp://extondemand.livestream.com/ondemand/trans/dv15/mogulus-user-files/chzdrowypuls/2012/04/04/15bbcc6c-30dc-4f08-91ca-b14dc40bbe3a" ],
            [ "SKY NEWS", 6,"mms://194.88.72.17:1755/skynews_wmlz_live300k" ],
            [ "BBC World News HD", 6,"http://212.79.96.134:8011/" ],
            [ "BBC 1", 6,"rtsp://195.90.118.93/bbc1_1" ],
            [ "BBC 2", 6,"rtsp://195.90.118.93/bbc2_1" ],
            [ "Россия 24", 6,"http://cdnvideowmlive.fplive.net/cdnvideowmlive-live/r24_hq" ],
            [ "CBBC", 6,"rtsp://195.90.118.93/CBBC_1" ],
            [ "EuroNews", 6,"http://212.79.96.134:8013/" ],
            [ "Pro7", 6,"http://212.79.96.134:8009/" ],
            [ "Rtl", 6,"http://212.79.96.134:8008/" ],
            [ "Sat1", 6,"http://212.79.96.134:8010/" ],
            [ "Prima Cool HD", 6, "http://212.79.96.134:8021/" ],
            [ "ČT 1", 6, "http://212.79.96.134:8001/" ],
            [ "CT 24 HD", 6, "http://212.79.96.134:8015/" ],
            [ "Nova Cinema HD", 6, "http://212.79.96.134:8020/" ],
            [ "Noe TV HD", 6, "http://212.79.96.134:8017/" ],
            [ "TV Paprika HD", 6, "http://212.79.96.134:8018/" ],
            [ "Focuz TV", 6, "http://gelretv.streamonline.nl:80/gelretv" ],
            [ "TV Rijnmond", 6, "rtsp://wm1.ams.cdn.surf.net/surfnetvdox=RTVRijnmond=TVRijnmond3" ],
            [ "Rai2", 6, "http://212.162.68.162:80/prodtvr2" ],
            [ "BFM TV", 6, "http://vipmms9.yacast.net:80/bfm_bfmtv" ],
            
            [ "Discovery Channel", 6,"rtmp://78.129.146.62/edge3/BETUK/BETUK" ],
            [ "LTV 1", 6,"http://82.135.235.37:80/LTV" ],
            [ "LTV World", 6,"http://82.135.235.37:80/LTVworld" ],
            [ "MTV Россия", 3,"http://77.91.77.19:7015/?sid=" ],
            [ "CNN", 6,"rtsp://media2.lsops.net:554/live/cnn_en_medium.sdp" ],
            [ "Russia Today", 6,"rtmp://fms5.visionip.tv/live/RT_3" ],
            [ "3Sat", 6,"rtsp://a62.l12560554061.c125605.g.lm.akamaistream.net/D/62/125605/v0001/reflector:54061" ],
            [ "The Voice", 6,"http://62.41.56.32:80/PUBLIC_votv_fi" ],
            [ "France 24 FR ", 6,"http://stream1.france24.yacast.net/f24_livefr" ],
            [ "France 24 ANG ", 6,"http://stream1.france24.yacast.net/f24_liveen" ],
            [ "ČT24 ", 6,"rtmp://wcdn40.nacevi.cz:80/CT24?id=HRscyPhgdFWqra6&publisher=lss/CT24-MP4_576p.stream" ],
            [ "Publika TV", 6,"rtmp://91.230.214.56/publika/livepublika1" ],
            [ "Big Pond Sport ", 6,"http://cht-cdn220-is-12.se.bptvlive.ngcdn.telstra.com/bp_online_bpsport_high" ],
            [ "TVN24 [chello]", 0, "mms://stream.livetv.chello.pl/TVN24" ],
            [ "TVN TURBO", 0, "rtmp://94.23.39.164/satlive/tvnturbo playpath=tvnturbo swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-132.htm  live=true swfVfy=true" ],

 #          [ "Poslkie stacje radiowe", 0, "http://xbmc.cba.pl/zbmc/onair.m3u" ],
            [ "Jedynka Polskie Radio", 7,"rtmp://stream85.polskieradio.pl/live/pr1.sdp" ],
            [ "Dwójka Polskie Radio", 7,"rtmp://stream85.polskieradio.pl/live/pr2.sdp" ],
            [ "Trójka Polskie Radio", 7,"rtmp://stream85.polskieradio.pl/live/pr3.sdp" ],
            [ "Czwórka Polskie Radio", 7,"rtmp://stream85.polskieradio.pl/live/pr4.sdp" ],
            [ "RMF FM", 7,"http://195.150.20.243/RMFFM48" ],
            [ "RMF CLASSIC", 7,"http://195.150.20.246/RMFCLASSIC48" ],
            [ "RMF MAXX", 7,"http://217.74.72.10/RMFMAXXX48" ],
            [ "Radio ZET", 7,"http://radiozetmp3-17.eurozet.pl:8400/;stream.nsv?seed=6046.38266377151" ],
            [ "ChilliZET", 7,"http://chillizetmp3-03.eurozet.pl:8400/;stream.nsv?seed=13186.232442967594" ],
            [ "Planeta FM", 7,"http://planetamp3-01.eurozet.pl:8400/;stream.nsv?seed=3665.857259184122" ],
            [ "Antyradio ", 7,"http://94.23.88.162:9200/;stream.nsv?seed=20.587672479450703" ],
            [ "Radio Plus", 7,"http://plus-siec-01.eurozet.pl:8500/;stream.nsv?seed=15073.804180137813" ],
            [ "TOK FM", 7,"http://fm.tuba.pl/stream.pls?radio=10" ],
            [ "Radio Złote Przeboje", 7,"http://fm.tuba.pl/stream.pls?radio=9" ],
            [ "Roxy FM", 7,"http://fm.tuba.pl/stream.pls?radio=8" ],
            [ "Eska", 7,"http://poznan5-5.radio.pionier.net.pl:8000/eska-warszawa.mp3" ],
            [ "Eska Rock", 7,"http://poznan5.radio.pionier.net.pl:8000/eskarock.mp3" ],
            [ "Radio Maryja", 7,"http://195.94.205.211/rm?MSWMExt=.asf" ],
            [ "Radio Wrocław", 7,"http://poznan5-1.radio.pionier.net.pl:8000/prwroclaw.mp3" ],
            [ "Radio Lublin", 7,"http://www.radio.lublin.pl/streaming/64k.m3u" ],
            [ "Radio Kraków", 7,"http://panel.nadaje.com:9150/radiokrakow.ogg?1352066977890.ogg" ],
            [ "Radio Rzeszów", 7,"http://radiointernetowe.net:9500/" ],
            [ "Radio Białystok", 7,"http://bh2.pl:9938" ],
            [ "Radio Katowice", 7,"http://85.11.77.142:8000/RadioKatowice.mp3.m3u" ],
            [ "Radio Kielce", 7,"http://gra.radio.kielce.com.pl:8000/rk1" ],
            [ "Radio Opole", 7,"http://213.73.25.178:7055/" ],
            [ "Radio Szczecin", 7,"http://www.radio.szczecin.pl/onair.m3u" ],
            [ "Radio Kaszëbë", 7,"http://stream3.nadaje.com:8048/;;0" ],
            [ "Radio Fest", 7,"http://209.62.16.60/radiofest" ],
            [ "Radio CCM", 7,"http://209.62.16.60/radioccm?1352151821734.mp3" ],
            [ "Radio Piekary", 7,"http://shot2.inten.pl:8412/" ],
            [ "Białystok Rynek Kościuszki", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera35.stream" ],
            [ "Ciechocinek, fontanna Grzybek", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera53.stream" ],
            [ "Darłowo Hotel Apollo", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera37.stream" ],
            [ "Gdańsk ul.Długa", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera31.stream" ],
            [ "Gogołów, wyciąg narciarski Pod Dziedzicem", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera46.stream" ],
            [ "Jastarnia", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera58.stream" ],
            [ "Korbielów, kolej krzesełkowa BABA", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera50.stream" ],
            [ "Korbielów, Schronisko na Hali Miziowej", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera65.stream" ],
            [ "Krajno, Park Rozrywki Sabat Krajno", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera52.stream" ],
            [ "Kraków Rynek Główny", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera9.stream" ],
            [ "Kraków ul. Floriańska", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera8.stream" ],
            [ "Kuźnica (Jastarnia)", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera57.stream" ],
            [ "Łeba - Plaża, Agados", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera33.stream" ],
            [ "Łódź Plac Wolności", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera19.stream" ],
            [ "Łódź Rondo Solidarności", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera20.stream" ],
            [ "Łódź ul.Piotrkowska", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera7.stream" ],
            [ "Międzybrodzie Bialskie, kompleks RELAKS", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera62.stream" ],
            [ "Poznań Stary Rynek", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera24.stream" ],
            [ "Poznań ul.Głogowska", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera22.stream" ],
            [ "Poznań ul.Hetmańska / ul.Głogowska", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera21.stream" ],
            [ "Poznań, Lodowisko Chwiałka", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera63.stream" ],
            [ "Sopot Klub Atelier", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera32.stream" ],
            [ "Góra Kamieńsk Stok narciarski", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera25.stream" ],
            [ "Szczyrk, Hotel Meta", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera48.stream" ],
            [ "Szczyrk, Kompleks narciarski Biały Krzyż", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera68.stream" ],
            [ "Ustka Restauracja Korsarz", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera38.stream" ],
            [ "Ustroń, Kolej Linowa Palenica", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera61.stream" ],
            [ "Warszawa Al. Jana Pawła II / ul.Anielewicza", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera2.stream" ],
            [ "Warszawa Al. Solidarności / Al. Jana Pawła II", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera15.stream" ],
            [ "Warszawa Plac Konstytucji", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera18.stream" ],
            [ "Warszawa ul.Chmielna", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera12.stream" ],
            [ "Warszawa ul.Marszałkowska", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera6.stream" ],
            [ "Warszawa, Plac Defilad", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera16.stream" ],
            [ "Wisła, Kolej Linowa Cieńków", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera49.stream" ],
            [ "Wisła, Ośrodek Narciarski Nowa Osada", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera47.stream" ],
            [ "Wisła, Ośrodek Narciarski Stożek", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera51.stream" ],
            [ "Wrocław Hostel Tu i Teraz", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera28.stream" ],
            [ "Wrocław Rynek", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera27.stream" ],
            [ "Wrocław ul. Wyszyńskiego", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera26.stream" ],
            [ "Wrocław ul.Świdnicka, Cafe Borówka", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera29.stream" ],
            [ "Zagroń Istebna, ośrodek narciarski", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera64.stream" ],
            [ "Zakopane Gubałówka, widok na Giewont", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera10.stream" ],
            [ "Zwardoń, wyciąg- Duży Rachowiec", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera45.stream" ],
            [ "Świnoujście Plaża", 8,"rtmp://vod.wowza.astrosa.pl:80/rtplive/:camera41.stream" ],
            [ "Trzebinia placyk obok wieży multimedialnej i wylot ul. Narutowicza", 8,"http://89.231.239.50:7098/video2.mjpg" ],
            [ "Trzebinia otoczenie wieży multimedialnej", 8,"http://89.231.239.50:7097/video2.mjpg" ],
            [ "Trzebinia widok na fontannę", 8,"http://89.231.239.50:7095/video2.mjpg" ],
            [ "Trzebinia Rynek", 8,"http://89.231.239.50:7096/video2.mjpg" ],
            [ "Kraków Wawel i zakole Wisły", 8,"rtmp://h264.webcamera.pl/krakow_cam_4c3e37/krakow_cam_4c3e37.stream" ],
            [ "Kraków Podziemia Rynku Głównego", 8,"rtmp://h264.webcamera.pl/krakow_cam_c44608/krakow_cam_c44608.stream" ],
            [ "Kraków Grodzka", 8,"rtmp://h264.webcamera.pl/krakow_cam_702b61/krakow_cam_702b61.stream" ],
            [ "Kraków Widok z ulicy Brackiej", 8,"rtmp://h264.webcamera.pl/krakow_cam_9a3b91/krakow_cam_9a3b91.stream" ],

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
