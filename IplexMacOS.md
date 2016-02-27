# Jak uruchomić IPLEX pod MacOS #
autorem artykułu jest **pawel.poskuta**

Testowane pod MacOSX 10.6 oraz Xcode 3.2.6.
Instrukcja oparta na:
https://raw.github.com/xbmc/xbmc/master/docs/README.osx

# Szczegóły #
Jeśli mamy MacOSX 10.7 lub 10.8 prawdopodobnie musimy zainstalować Xcode 4.X, a z nim współpracuje tylko rozwojowa wersja XBMC.
Kompilujemy XBMC z patchem dla obsługi platformy Iplex:

1. Pobieramy źródła ze strony:
http://xbmc.org/download/

Ja wybrałem stabile 11.0, link bezpośredni:
http://mirrors.xbmc.org/releases/source/xbmc-11.0.tar.gz

2. Przenosimy do wygodnego dla nas katalogu oraz rozpakowujemy klikając dwukrotnie na ściągnięty plik.

3. Pobieramy Xcode 3.2.6 ze strony Apple:
https://developer.apple.com/xcode/
uwaga, do pobrania z tej strony należy posiadać konto w Applu

4. Instalujemy standardowo Xcode (podczas instalacji wybieramy także Mac OSX 10.4 oraz odznaczamy Essentials -> IOS SDK jeśli chcemy zaoszczędzić miejsca a nie będziemy programować niczego dla iPhone'a)

5. otwieramy terminal i przechodzimy do rozpakowanego katalogu XBMC (w moim przypadku rozpakowałem w katalogu domowym, więc:
```
cd xbmc-11.0/
```

6. Pobieramy patch ze strony:
http://sd-xbmc.googlecode.com/files/xbmc-70537d2-500-Vividas-demuxer-ffmpeg-support.patch
i zapisujemy go do katalogu XBMC

7. W terminalu wpisujemy:
```
$ patch -p1 < xbmc-70537d2-500-Vividas-demuxer-ffmpeg-support.patch
```
8. następnie w terminalu wykonujemy następujące polecenia:
```
$ cd tools/darwin/depends
$ ./bootstrap
$ ./configure --with-darwin=osx
$ make
$ cd ..
$ cd ..
$ cd ..
$ make -C tools/darwin/depends/xbmc
$ make clean
$ make xcode_depends
$ make -C lib/addons/script.module.pil
$ xcodebuild -configuration Release ONLY_ACTIVE_ARCH=YES ARCHS=i386 VALID_ARCHS=i386 -target "XBMC.app" -project XBMC.xcodeproj
```
9. I wszystko, jeśli po drodze nie wyskoczyły żadne błędy skompilowane XBMC z patchem powinniśmy mieć w katalogu:
```
/XBMC/build/Release/
```