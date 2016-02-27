# Patchowanie i kompilacja XBMC + Iplex + ffmpeg #
podziękowania dla **dziorki**, bo to z jego blogu **[/dev/null](http://dziorki.wordpress.com/2012/04/04/patchowanie-i-kompilacja-xbmc-iplex/#more-173)** został zaczerpnięty poniższy artykuł.


# Szczegóły #
Do działania Iplexu na platformie XBMC niezbędne jest spatchowanie ffmpeg. Aby to zrobić należy wykonać poniższe czynności.

Ściągamy źródła XBMC (niezbędny jest na w tym przypadku git)
```
git clone https://github.com/opdenkamp/xbmc.git
```

wchodzimy do katalogu z xbmc
```
cd xbmc
```

Ściągamy patcha
```
wget http://sd-xbmc.googlecode.com/files/xbmc-70537d2-500-Vividas-demuxer-ffmpeg-support.patch
```

patchujemy
```
patch -p1 < xbmc-70537d2-500-Vividas-demuxer-ffmpeg-support.patch
```

instalujemy wszystkie niezbędne biblioteki
```
sudo apt-get install git-core make g++ gcc gawk pmount libtool nasm yasm automake cmake gperf zip unzip bison libsdl-dev libsdl-image1.2-dev libsdl-gfx1.2-dev libsdl-mixer1.2-dev libfribidi-dev liblzo2-dev libfreetype6-dev libsqlite3-dev libogg-dev libasound2-dev python-sqlite libglew-dev libcurl3 libcurl4-gnutls-dev libxrandr-dev libxrender-dev libmad0-dev libogg-dev libvorbisenc2 libsmbclient-dev libmysqlclient-dev libpcre3-dev libdbus-1-dev libhal-dev libhal-storage-dev libjasper-dev libfontconfig-dev libbz2-dev libboost-dev libenca-dev libxt-dev libxmu-dev libpng-dev libjpeg-dev libpulse-dev mesa-utils libcdio-dev libsamplerate-dev libmpeg3-dev libflac-dev libiso9660-dev libass-dev libssl-dev fp-compiler gdc libmpeg2-4-dev libmicrohttpd-dev libmodplug-dev libssh-dev gettext cvs python-dev libyajl-dev libboost-thread-dev libplist-dev libusb-dev libudev-dev
```

dla pewności dajemy wcześniej
```
export MAKE=make
```

następnie uruchamiamy
```
./bootstrap
```

pózniej
```
./configure --enable-rtmp
make -j2
```

gdzie _-j2_ to 2 rdzenie. sam proces kompilacji może potrwać.

następnie dajemy
```
make install
```