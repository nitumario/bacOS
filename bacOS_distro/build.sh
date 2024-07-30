#!/bin/bash

# Exit on error
set -e

# Constants
KERNEL_VERSION="linux-5.10.76.tar.xz"
GLIBC_VERSION="glibc-2.38.tar.gz"
BUSYBOX_VERSION="busybox-1.36.1.tar.bz2"
CURRENT_DIR="$(pwd)"
KERNEL_PATH="$CURRENT_DIR/bacos/$(basename $KERNEL_VERSION .tar.xz)"
GLIBC_PATH="$CURRENT_DIR/bacos/$(basename $GLIBC_VERSION .tar.gz)"
BUSYBOX_PATH="$CURRENT_DIR/bacos/$(basename $BUSYBOX_VERSION .tar.bz2)"
SYSROOT_PATH="$CURRENT_DIR/bacos/sysroot"
BACOS_PATH="$CURRENT_DIR/bacos"
ISO_PATH="$CURRENT_DIR/bacos/iso"

# Install dependencies
install_dependencies() {
  sudo apt-get install -y \
    fakeroot \
    build-essential \
    ncurses-dev xz-utils \
    libssl-dev \
    bc \
    flex \
    libelf-dev \
    bison
}

# Prepare build directory
prepare_build() {
  rm -rf $BACOS_PATH
  mkdir $BACOS_PATH
}

# Build kernel
build_kernel() {
  cd $BACOS_PATH
  wget "https://cdn.kernel.org/pub/linux/kernel/v5.x/$KERNEL_VERSION"
  tar -xvf $KERNEL_VERSION
  cd $KERNEL_PATH
  make x86_64_defconfig -j $(nproc)
  cp $CURRENT_DIR/config/kernel.cfg .config
  make bzImage -j $(nproc)
}

# Build glibc
build_glibc() {
  cd $BACOS_PATH
  wget "http://ftp.gnu.org/gnu/libc/$GLIBC_VERSION"
  tar -xvf $GLIBC_VERSION
  cd $GLIBC_PATH
  mkdir build
  mkdir GLIBC
  cd build
  ../configure --prefix=
  make -j $(nproc)
  make install DESTDIR=../GLIBC -j 2
}

# Build sysroot
build_sysroot() {
  cd $BACOS_PATH
  mkdir -p sysroot/usr
  cp -r $GLIBC_PATH/GLIBC/* sysroot
  cp -r GLIBC/include/* sysroot/include/
  cp -r GLIBC/lib/* sysroot/lib/
  rsync -a /usr/include sysroot
  ln -s ../include sysroot/usr/include
  ln -s ../lib sysroot/usr/lib
}

# Build busybox
build_busybox() {
  cd $BACOS_PATH
  wget "https://busybox.net/downloads/busybox-1.36.1.tar.bz2"
  tar -xvjf $BUSYBOX_VERSION
  cd $BUSYBOX_PATH
  make defconfig
  sed -i "s|.*CONFIG_SYSROOT.*|CONFIG_SYSROOT=\"../sysroot\"|" .config
  sed -i "s|.*CONFIG_EXTRA_CFLAGS.*|CONFIG_EXTRA_CFLAGS=\"-L../sysroot/lib\"|" .config
  make -j $(nproc)
  make CONFIG_PREFIX=$PWD/BUSYBOX install
}

# Install core
install_rootfs() {
  cd $CURRENT_DIR
  wget "https://github.com/nitumario/bacOS_/raw/main/root.zip"
  unzip root.zip
  cd $BACOS_PATH
  rm -rf rootfs
  mkdir rootfs
  cp -r $CURRENT_DIR/root/* $BACOS_PATH/rootfs
  cp -r $BUSYBOX_PATH/BUSYBOX/* $BACOS_PATH/rootfs
  cp $SYSROOT_PATH/lib/libm.so.6 $BACOS_PATH/rootfs/lib/libm.so.6
  cp $SYSROOT_PATH/lib/libc.so.6 $BACOS_PATH/rootfs/lib/libc.so.6
  cp $SYSROOT_PATH/lib/libresolv.so.2 $BACOS_PATH/rootfs/lib/libresolv.so.2
  cp $SYSROOT_PATH/lib/ld-linux-x86-64.so.2 $BACOS_PATH/rootfs/lib/ld-linux-x86-64.so.2
  cp $SYSROOT_PATH/bin/ldd $BACOS_PATH/rootfs/bin/ldd
  sed -i 's/bash/sh/' $BACOS_PATH/rootfs/bin/ldd
  cd $BACOS_PATH/rootfs && ln -s lib lib64
  rm $BACOS_PATH/rootfs/linuxrc
  set +e
  strip -g \
    $BACOS_PATH/rootfs/bin/* \
    $BACOS_PATH/rootfs/sbin/* \
    $BACOS_PATH/rootfs/lib/* \
    2>/dev/null
  set -e
  rm -rf $CURRENT_DIR/root
  rm $CURRENT_DIR/root.zip
}

# Create ISO file
create_iso() {
  cd $BACOS_PATH
  rm -rf $ISO_PATH
  mkdir -p $ISO_PATH/boot/grub
  cd $BACOS_PATH/rootfs
  find . | cpio -o -H newc | gzip > $ISO_PATH/boot/root.cpio.gz
  cp $KERNEL_PATH/arch/x86/boot/bzImage $ISO_PATH/boot/bzImage
  cp $CURRENT_DIR/config/grub.cfg $ISO_PATH/boot/grub/grub.cfg
  grub-mkrescue -o $CURRENT_DIR/bacos-linux.iso $ISO_PATH
}

# Main
install_dependencies
prepare_build
build_kernel
build_glibc
build_sysroot
build_busybox
install_rootfs
create_iso
