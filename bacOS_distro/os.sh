#!/bin/bash


dependencies(){
    sudo apt-get install \
        fakeroot         \
        build-essential  \
        ncurses-dev xz-utils \
        libssl-dev bc bison flex \
        libelf-dev   \
        xorriso \
        git
}

workdir(){
    mkdir -p $HOME/Desktop/bacOS
    cd $HOME/Desktop/bacOS
}

get_kernel(){
    wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.76.tar.gz
    tar -xvf linux-5.10.76.tar.gz
}

config_kernel(){
    cd linux-5.10.76
    wget https://raw.githubusercontent.com/nitumario/bacOS/main/bacOS_distro/kernel.cfg -O .config
}

build_kernel(){
    make -j$(nproc)
}

get_busybox(){
    cd $HOME/Desktop/bacOS
    wget https://busybox.net/downloads/busybox-1.33.1.tar.bz2
    tar -xvf busybox-1.33.1.tar.bz2
}

config_busybox(){
    cd busybox-1.33.1
    wget  https://raw.githubusercontent.com/nitumario/bacOS/main/bacOS_distro/busybox.cfg -O .config
}   

build_busybox(){
    make -j$(nproc)
    make install
}
