# Modyfikacje pluginu TVGuide #

## Poprawne wyświetlanie godziny w TVGuide ##
jeśli godzina wyświetla się np.: _1220:20_ zamiast _12:20_, edytujemy plik `langinfo.xml`, ktory znajduje się w

|Windows|c:\Program Files\XBMC\language\Polish|
|:------|:------------------------------------|
|ATV2   |/Applications/XBMC.frappliance/XBMCData/XBMCHome/Language/Polish|

jest:
```
<time symbolAM="" symbolPM="">HH:mm:ss</time>
```
zmieniamy na:
```
<time symbolAM="" symbolPM="">H:mm:ss</time>
```
i godzina wyświetla się normalnie.


## Zmiana podświetlenia programu ##
U mnie na TV (na PC działa normalnie) podświetlona pozycja w programie zlewa się z reszta, aby to rozwiązać edytujemy plik `tvguide-program-grey-focus.png`, znajduje się on w:
```
\Dane aplikacji\XBMC\addons\script.tvguide\resources\skins\Default\media
```

Zmieniłem podświetlenie na czerwony wygląda to tak:
![https://lh6.googleusercontent.com/-g6PlKJXNXCQ/UIvuaHT6aiI/AAAAAAAAA3M/xymMdMc_ebc/s800/screenshot002.png](https://lh6.googleusercontent.com/-g6PlKJXNXCQ/UIvuaHT6aiI/AAAAAAAAA3M/xymMdMc_ebc/s800/screenshot002.png)


## Zmiana wygladu TVGuide ##
Jezeli mamy dosyc domyslnego wygladu TVGuide, to mozemy go zmodyfikowac by wygladal tak:
![http://oi45.tinypic.com/2u8yp7r.jpg](http://oi45.tinypic.com/2u8yp7r.jpg)

W zaleznosci od skin'a ktorego uzywamy, sciagmy odpowiednia paczke:
|Confluence|http://sd-xbmc.org/xbmc/tvguide/Blue_EPG_by_maly95_v1.1.zip|
|:---------|:----------------------------------------------------------|
|Aeon Nox  |http://sd-xbmc.org/xbmc/tvguide/Blue_EPG_by_maly95_v1.1_skin_aeon_nox.zip|
|Rapier    |http://sd-xbmc.org/xbmc/tvguide/Blue_EPG_by_maly95_v1.1_skin_rapier.zip|

Po sciagnieciu odpowiedniego pliku, rozpakowywuje i jego zawartosc przerzucamy do
```
Documents and Settings\User\Dane aplikacji\XBMC\addons\script.tvguide\resources\skins\Default
```