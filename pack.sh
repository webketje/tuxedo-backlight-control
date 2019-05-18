if [ ! -d dist ]; then
  mkdir dist
else
  rm -rf dist/*
fi

find src -type d -exec chmod 755 {} \;
find src -type f -exec chmod 644 {} \;
find build/DEBIAN -type f -exec chmod 755 {} \;

pkg='tuxedo-backlight-control'
ver='0.3'
maintainer='Kevin Van Lierde <kevin.van.lierde@gmail.com>'
url='https://github.com/webketje/tuxedo-backlight-control'
prerm='../build/DEBIAN/prerm'
postinst='../build/DEBIAN/postinst'
category='contrib/utils'
desc='Utility built on top of TUXEDO Kernel module for keyboard backlighting
 (https://github.com/tuxedocomputers/tuxedo-keyboard) for Debian-based systems.
 It provides a bash CLI and a minimal Python UI.'

cd src

fpm -s dir\
  -t pacman\
  -f\
  -n "$pkg"\
  -v "$ver"\
  -a any\
  --iteration 1\
  --maintainer "$maintainer"\
  --url "$url"\
  --description "$desc"\
  --category "$category"\
  --license MIT\
  --depends python\
  --depends tk\
  --depends polkit\
  --after-install "$postinst"\
  --before-remove "$prerm"\
  usr

mv "$pkg-$ver-1-any.pkg.tar.xz" "../dist/$pkg-$ver-1-any.pkg.tar.xz"

fpm -s dir\
  -t rpm\
  -f\
  -n "$pkg"\
  -v "$ver"\
  -a any\
  --iteration 1\
  --maintainer "$maintainer"\
  --url "$url"\
  --description "$desc"\
  --category "$category"\
  --license MIT\
  --depends python\
  --depends tk\
  --depends polkit\
  --after-install "$postinst"\
  --before-remove "$prerm"\
  usr

mv "$pkg-$ver-1.any.rpm" "../dist/$pkg-$ver-1.any.rpm"

# Debian & derivatives
cd ..

cp -r build/DEBIAN src
dpkg-deb -b src "dist/$pkg-$ver-1.any.deb"
rm -rf src/DEBIAN
