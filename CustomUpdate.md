# Wprowadzenie #
Jak wiele osob zauwazylo, od kilku miesiacy wtyczka **plugin.video.polishtv.live** pozostawala w wersji v0.0.4. choc plugin byl regularnie aktualizowany. W tym czasie doszlo kilka nowych serwisow, wprowadzane byly poprawki, lecz numer wersji pozastawal nie zmieniony. Bylo to celowe z naszej strony a powody byly dwa: Auto Update i IPLA.

**Auto Update** to feature w XBMC, ktory automatycznie uaktualnie pluginy na podstawie ich wersji. Sprawdzana jest wersja zainstalowanego pluginu i porownywana z ta w repozytorium. Jezeli wersje sie roznia, to nowa wtyczka jest sciagana, a obecna zostaje **NADPISANA**.

**IPLA** to jeden z serwisow, ktory bylo obslugiwany przez wtyczke **plugin.video.polishtv.live** od prawie samego poczatku. To wlasnie dzieki tej wtyczce jako pierwsi moglismy sie cieszyc IPLA pod XBMC. Ze wzgledow "pseudo-prawnych", bylismy zmuszeni usunac serwis z projektu (usnac plik ipla.py i wykomentowac kilka linijek w default.py). Jak kazdy dobrze wie, w internecie nic nie ginie, tak i plik ipla.py :) Plik ten zostal przeniesiony na kilka roznych serwerow, a wielu z nas wciaz ma jego lokalne kopie. Wystarczylo tylko odkomentowac kilka linijek w `default.py` i wciaz sie cieszyc IPLA.

_Uaktualnienie:_ **IPLA na nowo jest znow we wtyczce. Nie potrzeba jej "wlaczac" za pomoca CustomUpdate.**

## Auto Update i IPLA - sprawy sie komplikuja ##
Jak juz wiemy Auto Update nadpisuje istniejaca wtyczke, wiec gdy wersja sie zmienia, nasz zmodyfikowany `default.py` (ten z wlaczona IPLA) zostaje nadpisany i musimy znow recznie modyfikowac `default.py` by ja wlaczyc. A co jesli mamy dolozone dodatkowe stacje w pliku `stations.py`? One tez bede nadpisany przez Auto Update. Jesli wtyczka jest uaktualniana kilka razy w tygodniu, to takie modyfikacje sa delikatnie uciazliwe. Wlasnie z tego powodu wersja wtyczki pozostala nie zmianiona przez ostatnie kilka miesiecy.

## Custom Update - Rozwiazanie problemu ##
Skoro Auto Update nadpisuje nasze pliki to, my musimy zrobic dokladnie to samo, nadpisac uaktualnione pliki naszymi, "zmodyfikowanymi", ale to musi byc zrobione automatycznie. Tak zrodzil sie feature **Custom Update**. Dzieki tej funkcji, mozemy w latwy sposob dodac/zmodyfikowac pliki pluginu.

W ponizszym WIKI postaram sie wytlumaczyc jak skonfigurowac **Custom Update** ~~tak by moc ogladac IPLA i dodac zagraniczne kanaly do stations.py,~~ w naszej ulubionej wtyczce **plugin.video.polishtv.live**.

# Szczegoly #
Zasada dzialania jest stosunkowo prosta. **Custom Update** uzywa pliku XML, w ktorym zdefiniowane sa lokacje: naszego zmodyfikowanego pliku _(source)_ jak i pliku ktory chcemy nadpisac _(destination)_.

~~**ipla.py**~~
  * ~~_(source)_ plik znajduje sie tutaj: http://jatrn.com/xbmc/sd-xbmc/ipla.py,~~
  * ~~_(destination)_ ma byc skopiowany do `hosts/ipla.py`~~
~~**stations.py**~~
  * ~~_(source)_ kopiujemy pliki z katalogu wtyczki `plugin.video.polishtv.live/hosts/stations.py` do `c:\sd-xbmc\stations.py`. Z linij 54 i 55 usuwamy hash (#) aby je odkomentowac, zapisujemy plik i zamykamy.~~
  * ~~_(destination)_ ma byc skopiowany do `hosts/stations.py`~~
~~**default.py**~~
  * ~~_(source)_ plik znajduje sie tutaj: http://jatrn.com/xbmc/sd-xbmc/default.py,~~
  * ~~_(destination)_ ma byc skopiowany do `default.py`~~


Wiedzac gdzie znajduja sie nasze "zmodyfikowane" pliki, jak rowniez gdzie maja byc skopiowane, jestesmy gotowi do swtorzenia plik XML. Struktura jest bardzo prosta i wyglada nastepujaco:
```
<custom id="plugin.video.polishtv.live">`
  <file>
    <source>http://jatrn.com/xbmc/sd-xbmc/default.py</source>
    <destination>default.py</destination>
  </file>
  <file>
    <source>http://jatrn.com/xbmc/sd-xbmc/ipla.py</source>
    <destination>hosts/ipla.py</destination>
  </file>
</custom>
```
Tworzymy plik i zapisujemy go w jakiejs dogodnej lokacji, np. `c:\sd-xbmc\custom.xml`. Nastepnie wchodzimy do Ustawien wtyczki, w `Default/Custom Update` w polu `XML file path` wpisujemy lokalizacje naszego wczesniej stworzonego pliku XML, czyli: `c:\sd-xbmc\custom.xml`
Naciskamy `OK` by zaakceptowac zmiany. Wchodzimy do `Ustawien` jeszcze raz i naciskamy `Run Custom Update` i to tyle.

~~A tak na koniec. Jesli nie chce wam sie bawic w tworzenie XML czy modyfikacje `stations.py`, a zalezy wam by miec IPLE, to pod adresem http://jatrn.com/xbmc/sd-xbmc/custom.xml znajduje sie gotowy XML. Nalezy wpisac ten adres w `Ustawieniach` wtyczki, nacisnac `OK` i `Run Custom Update` i po sprawie. Powodzenia!~~