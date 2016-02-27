# Opisy i modyfikacje wykonane na TV Guide v1.3.5 + XBMC 11 Eden + WIN XP SP3 #
Autorem jest **midcars1@gmail.com**

## Instalacja pluginu TV Guide ##
W XBMC wchodzimy w _programy => pobierz więcej_ i z listy wybieramy TV Guide.


## Konfiguracja ##
Wchodzimy  w _system => wtyczki => włączone wtyczki => wtyczki programów => TV Guide_

Klikamy ustaw, jako źródło ustawiamy XMLTV, następnie ściągamy na dysk którąś z wersji EPG:

|http://sd-xbmc.org/xbmc/epg/epg_weebtv.xml| wersja na 48 godzin dla weeb.tv|
|:-----------------------------------------|:-------------------------------|
|http://sd-xbmc.org/xbmc/epg/epg_weebtv_CST.xml| wersja na 48 godzin dla weeb.tv dla strefy czasowej CST|
|http://sd-xbmc.org/xbmc/epg/epg_weebtv_EST.xml| wersja na 48 godzin dla weeb.tv dla strefy czasowej EST|
|http://sd-xbmc.org/xbmc/epg/epg_weebtv_PST.xml| wersja na 48 godzin dla weeb.tv dla strefy czasowej PST|
|http://sd-xbmc.org/xbmc/epg/epg.xml       | wersja na 7 dni dla 160+ kanałów, około 16Mb|
|https://www.dropbox.com/s/fhh9mkh9o60kbtg/epg.Uk.xml|wersja na 4 dni posegregowana tematycznie 93 kanały weeb.tv+wlacz.tv+srtumienie Dla czasu Gmt (UK)|
|https://dl.dropbox.com/s/u6aqn3cdaqzku6d/epgPL.xml| wersja na 4 dni posegregowana tematycznie 93 kanały weeb.tv+wlacz.tv+srtumienie |
|https://dl.dropbox.com/s/prqrvhk1s1j2i6z/epgPL2.xml|wersja na 4 dni posegregowana tematycznie 93 kanały weeb.tv+wlacz.tv+srtumienie+dodatkowe opisy programów|
|https://dl.dropbox.com/s/61kyqrvt933ggc3/picons.zip| loga kanałów do wersji epg na 4 dni |
|https://dl.dropbox.com/s/bj1nys0zmxuwh5u/stream%20tv%20strm.zip| pliki strm strumieni do wersji epg na 4 dni|


W polu plik XMLTV wskazujemy ścieżkę do pliku który ściągnęliśmy.


## Dodanie loga kanałów do TV Guide ##
ściągamy: http://dl.dropbox.com/u/42558348/weeb.tv/picons.rar

po wypakowaniu podajemy ścieżkę ikonek stacji w _"wyszukaj obrazki kanałów w"_, całość wygląda tak:
![https://lh4.googleusercontent.com/-rccbG6DSxjc/UIvdmFkMVOI/AAAAAAAAA20/Z881nOryGDs/s800/screenshot001.png](https://lh4.googleusercontent.com/-rccbG6DSxjc/UIvdmFkMVOI/AAAAAAAAA20/Z881nOryGDs/s800/screenshot001.png)

## Podlinkowanie kanałów TV Guide z plikami STRM wygenerowanymi przez wtyczke polishtv.live ##
We wtyczce w zakladce Weeb.tv wybieramy miejsce do zapisu plików STRM.
![https://lh5.googleusercontent.com/-wq020zzHppI/UKi8bF3gjOI/AAAAAAAAA3g/X6FsNIvI3wM/s800/screenshot003.png](https://lh5.googleusercontent.com/-wq020zzHppI/UKi8bF3gjOI/AAAAAAAAA3g/X6FsNIvI3wM/s800/screenshot003.png)
Odpalamy TV Guide, zaznaczamy np: Polsat wciskamy ENTER => _wybierz plik STRM_.
Następnie ta czynność powtarzamy dla reszty stacji.

## Usunięcie powiadomienia "otwieram strumień" ##
ściągamy :
http://jatrn.com/xbmc/wiki/gui.py


Następnie kopiujemy plik do:
|Win XP| `C:\Documents and Settings\<user name>\Dane aplikacji\XBMC\addons\script.tvguide\`|
|:-----|:----------------------------------------------------------------------------------|
|Win7  | `C:\Uzytkownicy\<uzytkownik>\AppData\xbmc\addons\script.tvguide\`                 |
|AppleTV 2| `/private/var/mobile/Library/Preferences/XBMC/addons/script.tvguide/`             |

_W systemach Windows, folder `Dane Aplikacji` jest ukryty._


## Automatyczne pobieranie pliku z programem EPG ##
### Wersja dla Windows ###
Sciagamy paczke http://sd-xbmc.org/xbmc/files/autoepg.zip i rozpakowywujemy ja do `C:\autoepg`. Teraz w folderze `C:\autoepg` znajduja sie nastepujace pliki:
  * wget.exe - narzedzie do pobieranie plikow,
  * autoepg.bat - plik wsadowy,
  * source.cmd - plik z lokacja EPG do sciagniecia.
Edytujemy pliki `source.cmd` i wskazujemy adres skad EPG mam byc sciagniety. Domyslnie wyglada to tak:
```
SET epgurl=http://sd-xbmc.org/xbmc/epg/epg_weebtv_CST.xml
```
Teraz po uruchomieniu `autoepg.bat`, plik z EPG zostanie sciagniety i zapisany do `c:\autoepg\epg.xml`. We wtyczce, TVGuide jako zrodlo XMLTV, nalez wybrac `c:\autoepg\epg.xml`.
By automatycznie scigac EPG po uruchomieniu komputera nalezy skopiowac `autoepg.bat` do Autostart. Mozna rowniez uzyc Windows Task Scheduler a by sciagac go w regularnych odstepach czasowych.


## Dodadkowe modyfikacje ##
W tym momencie powinnsmy miec wpelni dzialajacy TVGuide z obsluga streamow z wtyczki **plugin.vide.polishtv.live**. O modyfikacjach wygladu samego TVGuide, mozesz poczytac w [ModyfikacjeTVGuide](ModyfikacjeTVGuide.md).