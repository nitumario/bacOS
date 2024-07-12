#!/bin/sh

#stop kernel messages
dmesg -n 1
clear


# mount virtual filesystems
mount -t devtmpfs none /dev
mount -t proc none /proc
mount -t sysfs none /sys

# start BusyBox init
exec /sbin/init




