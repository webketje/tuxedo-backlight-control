if [ ! -d dist ]; then
  mkdir dist
else
  rm -rf dist/*
fi

# Debian & derivatives
dpkg-deb -b src dist/tuxedo-backlight-control.deb

# Arch Linux - unfortunately makepkg doesn't work properly on debian
# we need to manually create the tar

export PACKAGER='Kevin Van Lierde <kevin.van.lierde@gmail.com>'
cd build/ARCH
makepkg -f --nodeps --skipinteg
cd ../..
mv -T build/ARCH/pkg/tuxedo-backlight-control dist/pkg
cp -r -T src/usr dist/pkg/usr
cd dist
find pkg/ -printf "%P\n" -type f -o -type l -o -type d | tar -czf tuxedo-backlight-control.pkg.tar.gz --no-recursion -C pkg/ -T -

# Cleanup
rm -rf pkg/
cd ../build/ARCH
rm -rf pkg/
rm -rf src/
unlink *.tar.gz