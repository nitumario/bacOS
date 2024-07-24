#!/bin/sh

# Suppress kernel messages
dmesg -n 1

# Create directories
mkdir -p home/bacos
mkdir -p usr/local
mkdir -p tmp
mkdir -p mnt
mkdir -p dev/shm
mkdir -p proc
mkdir -p sys

# Mount file systems
mount -t proc none /proc
mount -t sysfs none /sys
mount -t tmpfs none /tmp

# Populate devices, hotplug
/sbin/udevd --daemon 2>&1 >/dev/null
/sbin/udevadm trigger --action=add 2>&1 >/dev/null &

# Set permissions
chown root:root /
chown -R root:root /bin /sbin /lib /lib64 /etc /usr /mnt
chown root:root /init /sbin/sudo
chmod 4755 /sbin/sudo
chown root:root /etc/sudoers
chmod 0440 /etc/sudoers
chown -R bacos:bacos /home /tmp /var
chmod -R a+w /home /tmp /var
chmod -R a+r /home /tmp /var
chmod -R +w /bin /sbin /etc /usr /mnt

# Display logo and wait for devices init
clear && cat /etc/logo.txt
echo "Initializing devices..."
sleep 3

# Start buxybox init as PID 1
exec /sbin/init
