if [ ! -d dist ]; then
  mkdir dist
else
  rm -rf dist/*
fi

pkg='tuxedo-backlight-control'
ver='0.3'
maintainer='Kevin Van Lierde <kevin.van.lierde@gmail.com>'
url='https://github.com/webketje/tuxedo-backlight-control'
prerm='../build/DEBIAN/prerm'
postinst='../build/DEBIAN/postinst'
category='contrib/utils'
desc='GUI utility built on top of TUXEDO Kernel module for keyboard backlighting
 (https://github.com/tuxedocomputers/tuxedo-keyboard).
 Provides a bash CLI (backlight) and a minimal Python UI.'

cd src

fpm -s dir\
  -t deb\
  -f\
  -n "$pkg"\
  -v "$ver"\
  --iteration 1\
  --maintainer "$maintainer"\
  --url "$url"\
  --description "Tuxedo Backlight Ctrl
  $desc"\
  --category "$category"\
  --license MIT\
  --depends python3\
  --depends python3-tk\
  --depends policykit-1\
  --after-install "$postinst"\
  --before-remove "$prerm"\
  usr

mv "${pkg}_$ver-1_amd64.deb" "../dist/${pkg}_$ver-1_amd64.deb"

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