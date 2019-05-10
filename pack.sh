if [ ! -d dist ]; then
  mkdir dist
fi

dpkg-deb -b src dist/tuxedo-backlight-control.deb
