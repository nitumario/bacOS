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
