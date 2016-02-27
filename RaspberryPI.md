# plugin.video.polishtv.live na RaspberryPI #

---

## Słowem wstępu ##
Postaram się tutaj opisać same spostrzeżenia oraz po części instrukcje jak działa wtyczka plugin.video.polishtv.live pod kontrolą XBMC na RaspberryPI. Nie będę tutaj natomiast opisywać samego procesu instalacji systemu operacyjnego na tym urządzeniu. Jest ich trochę do wyboru i każdy ma dobrze opisany ten proces. Osobiście za najbardziej użyteczny system uznałem XBian'a:<br />
https://github.com/xbianonpi/wiki/wiki <br />
Natomiast za najbardziej stabilny/szybki OpenElec: <br />
http://wiki.openelec.tv/index.php?title=Building_and_Installing_OpenELEC_for_Raspberry_Pi <br />
OpenElec jest oparty na systemie SquashFS, a więc jeśli chcemy cokolwiek dodać do samego systemu (nie dotyczy to wtyczek XBMC) musimy się trochę natrudzić. Dlatego wybrałem XBian'a, który prócz funkcji multimedialnej pełni dodatkowo rolę mini-serwera.

## Instalacja ##

Ponieważ wtyczka jest napisana bezpośrednio dla XBMC, a więc instalacja nie różni się tutaj wiele od przeciętnej instalacji opisanej tutaj: <br />
http://code.google.com/p/sd-xbmc/wiki/InstalacjaPluginu<br />
O ile użytkownicy Linux'a bez problemu sobie poradzą, dla użytkowników Windows może być problemem umieszczenie samego pliku na dysku.

Możemy to zrobić na dwa sposoby:
  * Ściągnąć wtyczkę z adresu: http://sd-xbmc.googlecode.com/files/repository.sd-addons.eu.zip zapisać ją lokalnie oraz użyć _WinSCP_, aby przenieść ją na Raspberry
  * Zalogować się do Raspberry korzystając z _Putty_ i wykorzystać protokół SSH, i zdalnie wywołać komendę
```
wget http://sd-xbmc.googlecode.com/files/repository.sd-addons.eu.zip
```
W obydwu przypadkach należy pamiętać, aby zalogować się na użytkownika, na którym działa XBMC, w większości będzie to _root_, ale np. w XBian'ie jest to użytkownik _xbian_. W przeciwnym razie XBMC nie będzie w stanie odczytać umieszczonego pliku.

Po umieszczeniu pliku na dysku, dalej postępujemy jak ze standardową instalacją w XBMC.

Po tym zabiegu możemy się cieszyć pełnią funkcjonalności wtyczki plugin.video.polishtv.live z zastrzeżeniami opisanymi poniżej nie zależnymi od jej twórców.

## Korzystanie ##

Serwisy, które przetestowałem to:
  * Anyfiles
  * BestPlayer
  * Ekino.tv
  * Kino.pecetowiec.pl
  * Seriale.net
  * TVNPlayer
  * TVP VOD
  * TVP Info
  * Włącz.tv
  * Weeb.tv

Wszystkie działają poprawnie w temacie odtwarzania (aby uruchomić, niektóre z nich musiałem dokonać pewnych poprawek w samej obsłudze API, błędy te zapewne zostaną poprawione w najbliższej aktualizacji).

Dodatkowo również nie miałem problemu ze skorzystanie źródeł wideo z:
  * MaxVideo
  * AnyFiles
  * Putlocker
  * Nowvideo.eu - Niestety strasznie wolny przesył danych
  * parę innych, których nazwy w tym momencie nie pamiętam

## Problemy ##

Niestety jako, że Raspberry Pi nie jest demonem prędkości (CPU 700MHz), a więc jest zdane w praktyce tylko na sprzętowe kodeki H264, oraz po wykupieniu dodatkowych licencji MPEG2 oraz VC-1. Pozwala to na skorzystanie wbrew pozorom z naprawdę dużej liczby serwisów. Nie ma też najmniejszego problemu, aby odtwarzać materiały zapisane w FullHD, to akurat bardziej ograniczają serwisy udostępniające.

Na razie zauważyłem jedynie brak wsparcia dla:
  * IPLEX - Standardowo nie obsługiwane, ale nawet po prze-kompilowaniu _ffmpeg_ nie będziecie w stanie nic obejrzeć, a jedynie posłuchać
  * HD3D.CC - Nie natrafiłem na materiał, który dałby się odtworzyć
  * Niektóre materiały video z innych serwisów w zależności od tego jak je zakodowano

## Podsumowanie ##
Podsumowywując połączenie Raspberry z XBMC i wtyczką plugin.video.polishtv.live pozwala na stworzenie całkiem niezłego zamiennika standardowej telewizji.