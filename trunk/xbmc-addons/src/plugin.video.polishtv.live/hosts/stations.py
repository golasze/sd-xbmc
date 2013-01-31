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
                [0, "Ogólnotematyczne", "tv_ogolnotematyczne.png"],
                [1, "Informacyjne", "tv_informacyjne.png"],
                [2, "Sportowe", "tv_sportowe.png"],
                [3, "Muzyczne", "tv_muzyczne.png"],
                [4, "Religijne", "tv_religijne.png"],
                [5, "Lokalne", "tv_ogolnotematyczne.png"],
                [6, "Zagraniczne", "tv_zagraniczne.png"],
                [7, "Polskie stacje radiowe", "tv_stacjeradiowe.png"],
                [8, "Okiem Kamery", "tv_okiemkamery.png"]
               ]

#           [title, category_id, videoUrl]
MENU_TAB = [  
            [ "TVN", 0, "rtmp://94.23.39.164/satlive/tvn1 playpath=tvn1 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-127.htm  live=true swfVfy=true" ],
            [ "ATM Rozrywka", 0, "rtmp://creyden.popler.tv:80/rtplive?play=123452/fdg4324" ],
            [ "TVP2", 0, "rtmp://94.23.39.164/satlive/tvp22 playpath=tvp22 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-131.htm  live=true swfVfy=true" ],
#           [ "TVN", 0, "rtmp://75.126.203.130/stream/JardelloTV3333?id=59199" ],
#           [ "Polsat LQ1", 0, "rtmp://93.174.93.65/live/PolsatTelewizyjkapl" ],
            [ "TVN24", 1, "rtmp://94.23.39.164/satlive/tvn24 playpath=tvn24 swfUrl=http://tv-on.pl/player/sat.swf pageUrl=http://tv-on.pl/stream,id-124.htm  live=true swfVfy=true" ],
            [ "SkyWindows", 0, "rtmp://h264.webcamera.pl:443/nartytv/tv_medium playpath=tv_medium swfUrl=http://www.webcamera.pl/player.swf pageUrl=http://skywindows.tv/  live=true swfVfy=true" ],
#           [ "Polsat", 0, "rtmp://198.105.209.124/stream/JardelloTV4343?id=59200" ],
#           [ "Polsat LQ", 0, "rtmp://75.126.203.130/stream/darmowatelewizjacompolsat?id=59168" ],
            [ "Canal Plus", 0, "rtmp://94.23.39.164/satlive/canalplus playpath=canalplus swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-138.htm  live=true swfVfy=true" ],
            [ "TV4", 0, "rtmp://gdansk.popler.tv:80/rtplive?play=123452/titru" ],
#           [ "National Geographic", 0, "rtmp://creyden.popler.tv:80/rtplive?play=123452/istreampl5" ],
            [ "TV Puls", 0, "rtmp://creyden.popler.tv:80/rtplive?play=123452/istreampl3" ],
            [ "TV Puls 2", 0, "rtmp://poviss.popler.tv:1935/rtplive?play=123452/istreampl4" ],
#           [ "Discovery Science", 0, "rtmp://creyden.popler.tv:80/rtplive?play=123452/istreampl2" ],
            [ "TTV", 0, "rtmp://gdansk.popler.tv:80/rtplive?play=123452/admin245" ],
            [ "Eska party", 3, "rtmp://stream.supermedia.pl/t-eska/eska_party_360p" ],
            [ "4FunTV stream 2", 3, "rtmp://94.23.39.164/satlive/funtv playpath=funtv swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-142.htm  live=true swfVfy=true" ],
            [ "TVP1", 0, "rtmp://94.23.39.164/satlive/tv1 playpath=tv1 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-126.htm  live=true swfVfy=true" ],            
            [ "HBO", 0, "rtmp://94.23.39.164/satlive/hbo playpath=hbo swfUrl=http://satlive.pl/player/player.swf pageUrl=http://satlive.pl/stream,id-137.htm  live=true swfVfy=true" ],
            [ "Canal Plus Film", 0, "rtmp://94.23.39.164/satlive/canfil playpath=canfil swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-137.htm live=true swfVfy=true" ],
            [ "TVP INFO ", 1, "rtmp://freeview.fms.visionip.tv/live/tvnetwork-polskaplus-tvpinfo-hsslive-25f-4x3-SDh?extsessionid=50e3fa0e292fb-52489ced473722861898a32c76fd7f93" ],
            [ "TVP MIX 1", 0, "http://195.245.213.199/Ch0003" ],
            [ "TVP MIX 2", 0, "http://195.245.213.204/Ch0018" ],
            [ "TVP MIX 3", 0, "http://195.245.213.204/Ch0019" ],
            [ "Nick jr.", 0, "http://95.188.126.233:1234/udp/233.7.70.169:5000" ],
            [ "TVP Sport (I-stream.pl)", 2, "rtmp://68.68.31.224/app/15216 playpath=15216 swfUrl=http://www.udemy.com/static/flash/player5.9.swf pageUrl=http://sawlive.tv/embed/ppv2  live=true swfVfy=true" ],
            [ "Orange Sport (I-stream.pl)", 2, "rtmp://68.68.31.224/app/15273 playpath=15273 swfUrl=http://www.udemy.com/static/flash/player5.9.swf pageUrl=http://sawlive.tv/embed/orange-sport  live=true swfVfy=true" ],
            [ "Kanal PPV (I-stream.pl)", 2, "rtmp://68.68.31.224/app/15215 playpath=15215 swfUrl=http://www.udemy.com/static/flash/player5.9.swf pageUrl=http://sawlive.tv/embed/ppv  live=true swfVfy=true" ],
            [ "nSport (I-stream.pl)", 2, "rtmp://68.68.31.224/app/15275 playpath=15275 swfUrl=http://www.udemy.com/static/flash/player5.9.swf pageUrl=http://sawlive.tv/embed/nsport- live=true swfVfy=true" ],
            [ "Eurosport2 (I-stream.pl)", 2, "rtmp://68.68.31.224/app/14902 playpath=14902 swfUrl=http://www.udemy.com/static/flash/player5.9.swf pageUrl=http://sawlive.tv/embed/is5 live=true swfVfy=true" ],
            [ "Eurosport (I-stream.pl)", 2, "rtmp://68.68.31.224/app/14901 playpath=14901 swfUrl=http://www.udemy.com/static/flash/player5.9.swf pageUrl=http://sawlive.tv/embed/is4 live=true swfVfy=true" ],        
            [ "Canal Plus Gol (I-stream.pl)", 2, "rtmp://50.7.28.178/app/14918 playpath=14918 swfUrl=http://static2.sawlive.tv/player.swf pageUrl=http://i-stream.pl/kanal-2 live=true swfVfy=true" ],        
            [ "DiscoveryHDWorld", 6, "http://live.gslb.letv.com/gslb?stream_id=disc&tag=live&ext=m3u8&sign=live_ipad" ],
            [ "Chelsea TV", 2,"rtmp://fms.ilive.to:1935/app/29vipc2xr6lscal playpath=29vipc2xr6lscal swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42418/Chelsea_TV  live=true swfVfy=true" ],

            [ "Canal Plus Gol (TV-ON.PL)", 2, "rtmp://94.23.39.164/satlive/canalplusgol playpath=canalplusgol swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-121.htm  live=true swfVfy=true" ],
            [ "Eurosport (TV-ON.PL)", 2, "rtmp://94.23.39.164/satlive/cn3 playpath=cn3 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-122.htm  live=true swfVfy=true" ],
            [ "Eurosport2 (TV-ON.PL)", 2, "rtmp://94.23.39.164/satlive/cn4 playpath=cn4 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-123.htm  live=true swfVfy=true" ],
            [ "Polsat Sport (TV-ON.PL)", 2, "rtmp://94.23.39.164/satlive/channel5 playpath=channel5 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-124.htm live=true swfVfy=true" ],
#           [ "Chanel 4 (TV-ON.PL)", 2, "rtmp://94.23.39.164/satlive/chanel4 playpath=chanel4 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-123.htm live=true swfVfy=true" ],
            [ "nSport (TV-ON.PL)", 2, "rtmp://94.23.39.164/satlive/nsport playpath=nsport swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-144.htm  live=true swfVfy=true" ],
            [ "Polsat", 0, "rtmp://94.23.39.164/satlive/pol1 playpath=pol1 swfUrl=http://tv-on.pl/player/player.swf pageUrl=http://tv-on.pl/stream,id-128.htm  live=true swfVfy=true" ],
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
            [ "Discovery Channel pl", 0,"rtmp://94.23.39.164/satlive/discovery playpath=discovery swfUrl=http://tv-on.pl/player/sat.swf pageUrl=http://tv-on.pl/stream,id-145.htm  live=true swfVfy=true" ],
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
            [ "Cinema HD", 6,"rtmp://fms.ilive.to:1935/app/nunp4wffot67rs7 playpath=nunp4wffot67rs7 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/40855/Cinema_HD  live=true swfVfy=true" ],
            [ "TC Action", 6,"rtmp://fms.ilive.to:1935/app/u7c81q0jwsuu6f4 playpath=u7c81q0jwsuu6f4 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42227/TC_Action_(Films)  live=true swfVfy=true" ],
            [ "TC Action(Premium)", 6,"rtmp://fms.ilive.to:1935/app/wn5xssyos5x0yj7 playpath=wn5xssyos5x0yj7 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42224/TC_Premium_(Films)  live=true swfVfy=true" ],
            [ "AXN", 6,"rtmp://fms.ilive.to:1935/app/dw657dcdmdf0vap playpath=dw657dcdmdf0vap swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/40853/AXN  live=true swfVfy=true" ], 
            [ "FOX LIFE", 6,"rtmp://fms.ilive.to:1935/app/zsykl0nvdr7xf0x playpath=zsykl0nvdr7xf0x swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/40842/FOX_Life  live=true swfVfy=true" ],
            [ "Nickelodeon Jr", 6,"rtmp://fms.ilive.to:1935/app/8f7p62ebc1aq711 playpath=8f7p62ebc1aq711 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42064/Nickelodeon_Jr  live=true swfVfy=true" ],
            [ "Sony", 6,"rtmp://fms.ilive.to:1935/app/09x1kzlybbh0nne playpath=09x1kzlybbh0nne swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42220/Sony  live=true swfVfy=true" ],
            [ "Sky Poker", 6,"rtmp://fms.ilive.to:1935/app/m2bp4qvbcsgdm79 playpath=m2bp4qvbcsgdm79 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/43575/SkyPoker  live=true swfVfy=true" ],
            [ "Cinemax", 6,"rtmp://fms.ilive.to:1935/app/xwurx9o4weweazs playpath=xwurx9o4weweazs swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/44200/Cinemax  live=true swfVfy=true" ],
            [ "HBO HD", 6,"rtmp://fms.ilive.to:1935/app/k2rf6sst1y24r6j playpath=k2rf6sst1y24r6j swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42221/HBO_HD  live=true swfVfy=true" ],
            [ "ESPN", 2,"rtmp://fms.ilive.to:1935/app/li1ppxzr1s3xegu playpath=li1ppxzr1s3xegu swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42746/ESPN  live=true swfVfy=true" ],
            [ "Disney Junior", 6,"rtmp://fms.ilive.to:1935/app/tljgzu7oqfmr7h0 playpath=tljgzu7oqfmr7h0 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/40859/Disney_Junior  live=true swfVfy=true" ],
            [ "MGM", 6,"rtmp://fms.ilive.to:1935/app/b0fehgu27mjkcxu playpath=b0fehgu27mjkcxu swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42200/MGM  live=true swfVfy=true" ],
            [ "FOX", 6,"rtmp://fms.ilive.to:1935/app/g5244477x253rk4 playpath=g5244477x253rk4 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/43406/FOX  live=true swfVfy=true" ],
            [ "ESPN2", 2,"rtmp://fms.ilive.to:1935/app/o2g5ezouet25auf playpath=o2g5ezouet25auf swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/40830/ESPN2  live=true swfVfy=true" ],
            [ "SyFy", 6,"rtmp://fms.ilive.to:1935/app/ohabkpgn3e25r3v playpath=ohabkpgn3e25r3v swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/40943/SyFy  live=true swfVfy=true" ],
            [ "Discovery Channel", 6,"rtmp://fms.ilive.to:1935/app/own38fuo0upig6w playpath=own38fuo0upig6w swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42226/Discovery_Channel  live=true swfVfy=true" ],
            [ "CSI 24H", 6,"rtmp://fms.ilive.to:1935/app/aszl8hyh5d4zdvs playpath=aszl8hyh5d4zdvs swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/42532/CSI_24H  live=true swfVfy=true" ],
            [ "MAX Prime", 6,"rtmp://fms.ilive.to:1935/app/cj2rsr2iwvi1yff playpath=cj2rsr2iwvi1yff swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/44199/MAX_Prime  live=true swfVfy=true" ],
            [ "Disney Channel", 6,"rtmp://fms.ilive.to:1935/app/2tag4dzgwof5ma2 playpath=2tag4dzgwof5ma2 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/38804/Disney_channel  live=true swfVfy=true" ],
            [ "NBC", 6,"rtmp://fms.ilive.to:1935/app/l39r78izlvk5exd playpath=l39r78izlvk5exd swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/44049/NBC  live=true swfVfy=true" ],
            [ "History Channel", 6,"rtmp://fms.ilive.to:1935/app/2oe52g4dzkf7h09 playpath=2oe52g4dzkf7h09 swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/37668/HISTORY_CHANNEL  live=true swfVfy=true" ],
            [ "AXN SCI-FI", 6,"rtmp://fms.ilive.to:1935/app/ihlqpmdcjreoosz playpath=ihlqpmdcjreoosz swfUrl=http://static.ilive.to:81/jwplayer/player.swf pageUrl=http://www.ilive.to/view/25441/AXN_SCI-FI_(live)  live=true swfVfy=true" ],

#           [ "TVN24 [chello]", 0, "mms://stream.livetv.chello.pl/TVN24" ],
            [ "TVN TURBO", 0, "rtmp://94.23.39.164/satlive/tvntu playpath=tvntu swfUrl=http://tv-on.pl/player/sat.swf pageUrl=http://tv-on.pl/stream,id-132.htm live=true swfVfy=true" ],

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
            [ "Chorzów estakada", 8,"rtmp://creyden.popler.tv:80/rtplive?play=123452/kamerachorzow" ],
            [ "Sopot molo", 8,"rtmp://creyden.popler.tv:80/rtplive?play=123452/CI_TASK2" ],
            [ "Gdańsk", 8,"rtmp://gdansk.popler.tv:80/rtplive?play=123452/CI_TASK1" ],

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
            self.add('stations', CATEGORY_TAB[i][1], str(CATEGORY_TAB[i][0]), CATEGORY_TAB[i][2])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def add(self, service, name, val, icon, folder = True, isPlayable = False):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&val=" + val
        if icon != False:
          icon = os.path.join(ptv.getAddonInfo('path'), "images/") + icon
        else:
          icon = "DefaultVideoPlaylists.png"
        liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')       
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
