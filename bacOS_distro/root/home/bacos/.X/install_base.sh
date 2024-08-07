#!/bin/sh

#################################
#
#        Install packages
#
#################################

# Download package installer
wget -O /tmp/dipi.zip https://github.com/maksimKorzh/dipi/archive/refs/heads/master.zip
unzip -d /tmp /tmp/dipi.zip
sudo cp /tmp/dipi-main/src/dipi /usr/bin/dipi

# Install packages
for PAC in $(cat /etc/packages.lst); do
  dipi $PAC
  if [ $PAC = "util-linux" ]; then
    sudo cp /usr/local/sbin/fdisk /sbin/fdisk
  elif [ $PAC = "ca-certificates" ]; then
    sudo mkdir /usr/local/etc/ssl/certs
    sudo update-ca-certificates
  fi
done


