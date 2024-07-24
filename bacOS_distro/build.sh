#!/bin/bash

# Exit on error
set -e

# Constants
KERNEL_VER="linux-5.10.76.tar.xz"
GLIBC_VER="glibc-2.38.tar.gz"
BUSYBOX_VER="busybox-1.36.1.tar.bz2"
PWD_DIR="$(pwd)"
KERNEL_DIR="$PWD/bacos/$(echo $KERNEL_VER | sed 's/\.tar\.xz//')"
GLIBC_DIR="$PWD/bacos/$(echo $GLIBC_VER | sed 's/\.tar\.gz//')"
BUSYBOX_DIR="$PWD/bacos/$(echo $BUSYBOX_VER | sed 's/\.tar\.bz2//')"
SYSROOT_DIR="$PWD/bacos/sysroot"
bacos_DIR="$PWD/bacos"
ISO_DIR="$PWD/bacos/iso"

# Install dependencies
get_deps() {
  sudo apt-get install   \
    fakeroot             \
    build-essential      \
    ncurses-dev xz-utils \
    libssl-dev           \
    bc                   \
    flex                 \
    libelf-dev           \
    bison
}

# Prepare build directory
build_init() {
  rm -rf $bacos_DIR
  mkdir $bacos_DIR
}

# Build kernel
build_kernel() {
  cd $bacos_DIR
  wget "https://cdn.kernel.org/pub/linux/kernel/v5.x/$KERNEL_VER"
  tar -xvf $KERNEL_VER
  cd $KERNEL_DIR
  make x86_64_defconfig -j $(nproc)
  cp $PWD_DIR/config/kernel.cfg .config
  make bzImage -j $(nproc)
}

# Build glibc
build_glibc() {
  cd $bacos_DIR
  wget http://ftp.gnu.org/gnu/libc/$GLIBC_VER
  tar -xvf $GLIBC_VER
  cd $GLIBC_DIR
  mkdir build
  mkdir GLIBC
  cd build
  ../configure --prefix=
  make -j $(nproc)
  make install DESTDIR=../GLIBC -j 2
}

# Build sysroot
build_sysroot() {
  cd $bacos_DIR
  mkdir -p sysroot/usr
  cp -r $GLIBC_DIR/GLIBC/* sysroot
  cp -r GLIBC/include/* sysroot/include/
  cp -r GLIBC/lib/* sysroot/lib/
  rsync -a /usr/include sysroot
  ln -s ../include sysroot/usr/include
  ln -s ../lib sysroot/usr/lib
}

# Build busybox
build_busybox() {
  cd $bacos_DIR
  wget "https://busybox.net/downloads/busybox-1.36.1.tar.bz2"
  tar -xvjf $BUSYBOX_VER
  cd $BUSYBOX_DIR
  make defconfig
  sed -i "s|.*CONFIG_SYSROOT.*|CONFIG_SYSROOT=\"../sysroot\"|" .config
  sed -i "s|.*CONFIG_EXTRA_CFLAGS.*|CONFIG_EXTRA_CFLAGS=\"-L../sysroot/lib\"|" .config
  make -j $(nproc)
  make CONFIG_PREFIX=$PWD/BUSYBOX install
}

# Install core
build_rootfs() {
  cd $PWD_DIR
  wget https://github.com/nitumario/bacOS_distro/raw/main/root.zip
  unzip root.zip
  cd $bacos_DIR
  rm -rf rootfs
  mkdir rootfs
  cp -r $PWD_DIR/root/* $bacos_DIR/rootfs
  cp -r $BUSYBOX_DIR/BUSYBOX/* $bacos_DIR/rootfs
  cp $SYSROOT_DIR/lib/libm.so.6 $bacos_DIR/rootfs/lib/libm.so.6
  cp $SYSROOT_DIR/lib/libc.so.6 $bacos_DIR/rootfs/lib/libc.so.6
  cp $SYSROOT_DIR/lib/libresolv.so.2 $bacos_DIR/rootfs/lib/libresolv.so.2
  cp $SYSROOT_DIR/lib/ld-linux-x86-64.so.2 $bacos_DIR/rootfs/lib/ld-linux-x86-64.so.2
  cp $SYSROOT_DIR/bin/ldd $bacos_DIR/rootfs/bin/ldd
  sed -i 's/bash/sh/' $bacos_DIR/rootfs/bin/ldd
  cd $bacos_DIR/rootfs && ln -s lib lib64
  rm $bacos_DIR/rootfs/linuxrc
  set +e
  strip -g \
  $bacos_DIR/rootfs/bin/* \
  $bacos_DIR/rootfs/sbin/* \
  $bacos_DIR/rootfs/lib/* \
  2>/dev/null
  set -e
  rm -rf $PWD_DIR/root
  rm $PWD_DIR/root.zip
}

# Create ISO file
build_iso() {
  cd $bacos_DIR
  rm -rf $ISO_DIR
  mkdir -p $ISO_DIR/boot/grub
  cd $bacos_DIR/rootfs
  find . | cpio -o -H newc | gzip > $ISO_DIR/boot/root.cpio.gz
  cp $KERNEL_DIR/arch/x86/boot/bzImage $ISO_DIR/boot/bzImage
  cp $PWD_DIR/config/grub.cfg $ISO_DIR/boot/grub/grub.cfg
  grub-mkrescue -o $PWD_DIR/bacos-linux.iso $ISO_DIR
}

# Main
get_deps
build_init
build_kernel
build_glibc
build_sysroot
build_busybox
build_rootfs
build_iso