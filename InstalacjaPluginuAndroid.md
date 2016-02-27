# Opis i modyfikacje wykonane na Samsung Galaxy Tap 2 z Android 4.0 #
Autorem jest **matiszek30@gmail.com**

Na początek zaznczamy w ustawieniach bezpieczeństwa żeby można było instalować pliki z innych źródeł. Następnie ściągamy XBMC na Androida, który znajdziemy tutaj http://mirrors.xbmc.org/releases/android/xbmc-12.0-Frodo_rc2-armeabi-v7a.apk.
Instalujemy go normalnie jak każdą aplikacje i gotowe mamy XBMC na Androidzie.


## Instalacja wtyczki plugin.video.polishtv.live ##
Ściągamy Repozytorium SD-XBMC z działu [Downloads](http://code.google.com/p/sd-xbmc/downloads/list), tak jak na komputerach stacjonarnych.
Ściągnięty plik będzie się znajdował w główny katalogu `moje pliki/sdcard/` w folderze `download` lub `downloads`. Potem już podąrzamy za poradnikiem na WIKI jak zainstalowac wtyczke, [Instalacja Pluginu](http://code.google.com/p/sd-xbmc/wiki/InstalacjaPluginu).


## Modyfikacje ##
Poniżej zamieszczam poradnik jak wpisać login i hasło na Wlacz TV.

Najpierw wchodzimy w `moje foldery` i w ustawienia gdzie zaznaczamy by pokazywało ukryte pliki. Następnie ściągamy Notepad z Google z opcją edycji plików obojętnie jaki i wchodzimy w niego i dajemy edytuj plik:

```
sdcard/Android/data/org.xbmc.xbmc/files/xbmc/userdata/addon_data/plugin.video.polishtv.live/settings.xml
```

Kiedy tam wejdziemy będziemy mieli miedzy innymi:
```
<setting value="" id="wlacztv_login"/>
<setting value="" id="wlacztv_pass"/>
```
Wpisujemy nazwe uzytkownika i haslo do tych pustych cudzysłowiow i gotowe.