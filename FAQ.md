### _Wtyczka wyswietla: Error script failed_ ###
Zapostuj problem, podaj swoja dystrybucje, podaj krok po kroku w jaki sposob blad jest generowany i najwazniejsze, zalacz `xbmc.log`

### _Gdzie znajduje sie xbmc.log?_ ###
Wszystkie informacje na temat **xbmc.log** znajduja sie w [WIKI](XBMC_debug.md)

### _MacOSX lub Android: Error script failed_ ###
W logach pojawia sie: `ImportError: dynamic module does not define init function (initParser)`

MacOSX skopiuj:
```
/Users/xxx/Library/Application Support/XBMC/addons/plugin.video.polishtv.live/resources/lib/Parser.py
```
do
```
/Users/xxx/Library/Application Support/XBMC/addons/plugin.video.polishtv.live/Parser.py
```

Android skopiuj:
```
/mnt/sdcard/Android/data/org.xbmc.xbmc/files/.xbmc/addons/plugin.video.polishtv.live/resources/lib/Parser.py
```
do
```
/mnt/sdcard/Android/data/org.xbmc.xbmc/files/.xbmc/addons/plugin.video.polishtv.live/Parser.py
```



### _Windows: Error script failed_ ###
Nazwa uzytkownika systemu Windows nie moze zawierac polskich znakow.

### _TVNPlayer nie dziala poza granicami Polski_ ###
Zloz donacje na sd-xbmc.org a dostaniesz namiary na nasz serwer proxy. Po otrzymaniu ich, Ustawienia->Globals wpisz swoi email i haslo a w Ustawienia->TVN zaznacz "use sd-xbmc proxy".