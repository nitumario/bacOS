#!/bin/sh

#stop kernel messages
dmesg -n 1
clear


# mount virtual filesystems
mount -t devtmpfs none /dev
mount -t proc none /proc
mount -t sysfs none /sys

# setup networking
for NETDEV in /sys/class/net/* ; do
  echo "Found network device ${NETDEV##*/}"
  ip link set ${NETDEV##*/} up  
  [ "${NETDEV##*/}" != "lo" ] && udhcpc -b -i ${NETDEV##*/} -s /etc/network.sh
done


# start BusyBox init
exec /sbin/init
