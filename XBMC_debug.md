# Generowanie pliku _log_ #

## Sposób 1: Włączenie logowania bezpośrednio z XBMC ##

Logowanie możemy włączyć bezpośrednio z XBMC, korzystając z opcji menu: `System->Ustawienia->System->Debugowanie` i zaznaczenie opcji `Włącz logowanie (debug)`.
![https://lh4.googleusercontent.com/-KMtm9PYOu6Y/UL_Iihjy6TI/AAAAAAAAA5w/Uqh-tlX-TjA/s912/screenshot013.png](https://lh4.googleusercontent.com/-KMtm9PYOu6Y/UL_Iihjy6TI/AAAAAAAAA5w/Uqh-tlX-TjA/s912/screenshot013.png)
Standardowo o fakcie generowania logu zawiadamia Cię informacja w lewym górnym rogu ekranu podająca lokalizacje pliku logu, zużycie pamięci (MEM) i procesora (CPU) oraz ilości wyświetlanych ramek na sekundę (FPS).
![https://lh5.googleusercontent.com/-lZwmVq0_zP0/UL_Iila3EzI/AAAAAAAAA5s/a43Z_7uuj7Q/s912/screenshot014.png](https://lh5.googleusercontent.com/-lZwmVq0_zP0/UL_Iila3EzI/AAAAAAAAA5s/a43Z_7uuj7Q/s912/screenshot014.png)

## Sposób 2: Włączenie logowania za pomocą pliku konfiguracyjnego ##

Logowanie można również włączyć poprzez edycję pliku konfiguracyjnego `advancedsettings.xml` i ustawienie parametru `loglevel`.
Opcja włączania logu w ten sposób jest niezwykle przydatna gdy XBMC nie startuje prawidłowo i nie mamy szansy wejść do jego menu ustawień.

Plik konfiguracyjny `advancedsettings.xml`  znajduje się w folderze z danymi aplikacji (np. dla Windows będzie to `%appdata% \XBMC)`. Edytujemy go dowolnym edytorem (ja używam Geany).

W przypadku braku pliku `advancedsettings.xml` we wskazanym folderze należy go samemu utworzyć.

Wartością dodaną, w stosunku do włączania logowania bezpośrednio z XBMC, jest możliwość decydowania jak szczegółowe dane powinien nasz log zawierać. I tak poprzez parametr `loglevel` można ustawić jedną z wartości:
|-1|brak logowania|
|:-|:-------------|
|0 |normalne logowanie (ustawienie domyślne)|
|1 |logowanie szczegółowe (debug)|
|2 |jak (1) + informacja na ekranie o użyciu procesora, pamięci itp.|
|3 |jak (2) + inormacja szczegółowa o zasobach SMB|


Dodatkowo możliwe jest ustawienie atrybutu `hidden`, który decyduje czy opcja włączania / wyłączania logowania będzie widoczna w XBMC (_false_) czy też nie (_true_).Przykładowo, chcąc włączyć szczegółowe logowanie, bez wyświetlania  informacji na ekranie, oraz ukryć opcję logowania z menu XBMC, należałoby wpisać:



&lt;loglevel hide=true&gt;1loglevel&gt;



Po wszystkim zapisujemy plik ustawień i restartujemy XBMC.

## Inne rozwiązania / dodatki ##
Możesz również chcieć użyć pluginu `XBMC Log Uploader`, który automatyzuje proces współdzielenia logu.

## Lokalizacja ##
Pliki logu znajdziesz w katalogu z zainstalowanym XBMC - typowo (w zależności od Systemu Operacyjnego) będzie to:
| Linux |`/home/user/.xbmc/temp/ `|
|:------|:------------------------|
| Crystalbuntu |`/root/.xbmc/temp/`      |
| Windows |`%APPDATA%\XBMC\ `       |
| iOS (ATV2/iPad/iPhone) |`/private/var/mobile/Library/Preferences/ `|
| OSX/ATV |`/Users//Library/Logs/ ` |
| Android |`/data/data/org.xbmc.xbmc/cache/temp/`|

Otwierając podaną lokalizację znajdziesz zwykle w niej dwa pliki:
  * **xbmc.log** – ostatni plik logu (to właśnie ten plik w zwykle Cię interesuje!),
  * **xbmc.old.log** – kopia poprzedniego pliku logu,

## Format ##
Log jest zwykłym plikiem tekstowym, a każde zdarzenie jest logowane przez XBMC w podanym niżej formacie:

[TIMESTAMP](TIMESTAMP.md) T:[THREADID](THREADID.md) M:[FREEMEM](FREEMEM.md) [LEVEL](LEVEL.md): [MESSAGE](MESSAGE.md)
  * TIMESTAMP - czas,
  * THREADID – identyfikator wątku zdarzenia,
  * FREEMEM – ilość wolnej pamięci (w bajtach),
  * LEVEL – poziom logowania,
  * MESSAGE – krótki opis i/lub ważne informacje o zdarzeniu.

## Poziomy logowania ##
W XBMC istnieją dwa różne poziomy logowania. Pierwszy jest to poziom szczegółowości zdarzenia, drugi kontroluje który poziom szczegółowości jest faktycznie zapisywany do logu.

Poziomy szczegółowości zdarzeń:
  * DEBUG – Szczegółowa informacja o statusie XBMC. Ta informacja jest w zwykle użyteczna dla programistów  lub doświadczonych użytkownikom XBMC.
  * INFO – Zdarzenie nie będące problemem. Logowane informacyjnie.
  * NOTICE – Podobne do INFO ale o większym znaczeniu. Ten poziom logowania i wcześniejsze są używane domyślnie.
  * WARNING – Potencjalny problem. Jeżeli XBMC wykonało akcję, której nie oczekiwałeś, tutaj zajdziesz prawdopodobnie informację dlaczego tak się stało.
  * ERROR – Wystąpił błąd. Typowo informowany jesteś o błędach skóry, odtwarzania itp.
  * FATAL – Błąd krytyczny. XBMC nieoczekiwanie zakończy pracę.

## Poziomy kontroli szczegółowości zapisu logu: ##
Poziomy posortowano w kolejności zależnej od ilości dostarczanej informacji:
  * None – Brak logowania. Plik xbmc.log może zostać utworzony, lecz pozostanie pusty.
  * Normal – Poziom domyślny. Logowane będą darzenia poziomu NOTICE lub wyższe.
  * Debug – Wszystkie zdarzenia będą logowane. Ten poziom lub wyższy jest zwykle oczekiwany w przypadku szukania pomocy innych (np. na Forum).
  * Debug w/ Visuals – Wyświetla te same informacje jak poziom Debug, lecz dodatkowo ilość wolnej pamięci i użycie procesora będą wyświetlanie na ekranie.
  * SMB Debug – To samo co Debug w/ Visuals, dodatkowo z masą szczegółowych informacji dotyczących protokołu Samba. Używaj tylko gdy to niezbędne / zostaniesz o to poproszony.