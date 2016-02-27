# Szczegółowy opis jak automatycznie ściągać plik EPG dla TVGuide na MacOS #
Autorem jest **kamol**

## Szczegóły ##

1. Pobieramy skrypt: https://www.dropbox.com/sh/sk5sy3fbl7w6jhc/uCLmrg0Bu8/AutodownloadEPG.zip

2. Skrypt odwołuje się do katalogu `"EPG"`, który należy utworzyć w `/users/shared/`.
W tym celu otwieramy `"Finder"` przechodzimy do zakładki `"Idź"` i wybieramy `"Idź do katalogu"` w oknie które się pojawi wpisujemy  `/users/shared/`
Tam tworzymy katalog o nazwie `"EPG"`.

3. Do katalogu `/users/shared/EPG/` wypakowujemy skrypt i plik `"sciezka.txt"`

4. Działanie skryptu polega na pobraniu z pliku `sciezka.txt` linka do EPG np. https://dl.dropbox.com/s/u6aqn3cdaqzku6d/epgPL.xml następnie ściągniecie pliku EPG i zapisanie go w katalogu `users/shared/EPG`, wszystkie istniejące dotychczas w tym katalogu pliki z rozszerzeniem xml są przenoszone do kosza.

5. Skrypt będzie się uruchamiał automatycznie jeśli umieścimy go w rzeczach automatycznie uruchamianych podczas logowania. W tym celu należy otworzyć `"Preferencje Systemowe"` znaleźć ikonę `"Użytkownicy i grupy"` kliknąć na kłódce i wpisać hasło administratora, a następnie przejść do zakładki `"Logowanie"` i dodać program skrypt do tej listy
![http://www.jatrn.com/xbmc/wiki/auto_macos.png](http://www.jatrn.com/xbmc/wiki/auto_macos.png)

6. Skrypt można także (preferowane) uruchamiać w jakimkolwiek schedulerze np. Task Till Down http://www.oliver-matuschin.de/en/Projects/Detail/Task_Till_Dawn-85. W tym celu otwieramy program, przenosimy tam skrypt, a następnie precyzujemy o której godzinie lub co ile godzin, dni ma być uruchamiany.

7. Następnie w XBMC w pluginie TVGuide podajemy ścieżkę do pliku xml  `/users/shared/EPG` i nazwa pliku EPG zakończoną rozszerzeniem `".xml"`

Skrypt nie jest zablokowany można go otworzyć w Automatorze i dowolnie zmienić ścieżki np. gdzie zapisywane jest EPG.