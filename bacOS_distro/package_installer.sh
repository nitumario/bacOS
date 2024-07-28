#!/bin/sh

PKG_REPO="http://tinycorelinux.net/14.x/x86_64/tcz"
DL_DIR="/tmp/pkg_dl"
INST_DIR="/usr/local"
CUR_DIR="$(pwd)"

download_pkg() {
  cd $CUR_DIR
  if [ -n "$1" ]; then
    mkdir -p $DL_DIR/$1
    if [ -f $DL_DIR/$1/$1.tcz ]; then
      echo "Package $1 is already downloaded."
    else
      wget -O $DL_DIR/$1/$1.tcz $PKG_REPO/$1.tcz
      wget -O $DL_DIR/$1/$1.dep $PKG_REPO/$1.tcz.dep
      wget -O $DL_DIR/$1/$1.md5 $PKG_REPO/$1.tcz.md5.txt
      cd $DL_DIR/$1 && md5sum -c $1.md5
      if [ $? -ne 0 ]; then exit 1; fi
      REQS=$(cat $DL_DIR/$1/$1.dep 2> /dev/null)
      if [ $? -ne 0 ]; then return; fi
      for REQ in $REQS; do
        download_pkg $(echo $REQ | sed 's/KERNEL/6.1.2-tinycore64/' | sed 's:\.tcz::')
      done
    fi
  else
    echo "Usage: ~$ script_name package_name"
  fi
}

install_pkgs() {
  sudo mkdir -p $INST_DIR
  PKG_LIST=$(ls $DL_DIR 2> /dev/null)
  for PKG in $PKG_LIST; do
    sudo mount $DL_DIR/$PKG/$PKG.tcz $DL_DIR/$PKG
    sudo cp -r $DL_DIR/$PKG/usr/local/* $INST_DIR
    sudo umount $DL_DIR/$PKG
  done
}

rm -rf $DL_DIR
download_pkg $1
install_pkgs
