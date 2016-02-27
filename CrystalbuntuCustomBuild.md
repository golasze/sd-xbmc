# Apple TV 1 i wtyczka plugin.video.polishtv.live #



Crystalbuntu to jeden z najprostszych sposobów na uruchomienie XBMC na Apple TV 1. Jest to system operacyjny na bazie Ubuntu 8.0.4, który w parze z karta CrystalHD umożliwia odtwarzanie video w rozdzielczości 1080p. Sama instalacja systemu jest stosunkowa prosta, ja pokaże jak zainstalować "custom build" XBMC, który pozwoli nam na odpalenie Iplex i weeb.tv z wtyczki plugin.video.polishtv.live.

Po zainstalowaniu Crystalbuntu łaczymy się z nim używajac SSH.

System spyta nas o nazwe użytkownika i hasło, wpisujemy _**atv**_ jako użytkowanik i jako hasło.

Po zalogowaniu uruchamiamy narzędzie do konfiguracji
```
./configure
```

a następnie wybieramy z listy _XBMC Install a custom XBMC build_

W oknie z adresem podajemy http://jatrn.com/xbmc/atv.tar.gz lub http://xbmc.tefnet.pl/atv/xbmc-nightly-03-03-2012.tar.gz (jest to dokładnie ten sam build znajdujący się na dwóch różnych serwerach) i naciskamy _OK_.

Narzędzie konfiguracyjne rozpocznie sciąganie, a po jego zakończeniu automatycznie zainstaluje custom build XBMC. Apple TV powinno nam się zresetować i załadować nasz nowy XBMC.