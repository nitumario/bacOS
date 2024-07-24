#!/bin/sh

# Install alsa
dipi alsa
dipi alsa-config
sudo sed -i 's:\bstaff\b:msmd:g' /usr/local/etc/alsa/alsa.conf

# Update .asoundrc
echo "pcm.!default {" > .asoundrc
echo "  type hw" >> .asoundrc
echo "  card 2" >> .asoundrc
echo "  device 0" >> .asoundrc
echo "  channels 2" >> .asoundrc
echo "}" >> .asoundrc
echo "ctl.!default {" >> .asoundrc
echo "  type hw" >> .asoundrc
echo "  card 2" >> .asoundrc
echo "  device 0" >> .asoundrc
echo "  channels 2" >> .asoundrc
echo "}" >> .asoundrc

# Reset dbuse
echo "Resetting dbus..."
/usr/local/etc/init.d/dbus stop
/usr/local/etc/init.d/dbus status

# Install pulseaudio
dipi pulseaudio
mkdir -p .config/pulse
sudo cp /usr/local/share/pulseaudio/files/daemon.conf .config/pulse/
sudo cp /usr/local/share/pulseaudio/files/default.pa .config/pulse/
sudo sed -i '38s/#//' .config/pulse/default.pa
sudo sed -i '46,67s/^/#/' .config/pulse/default.pa
sudo sed -i '91,95s/^/#/' .config/pulse/default.pa
sudo sed -i '119,137s/^/#/' .config/pulse/default.pa
sudo sed -i '39s/#//' .config/pulse/default.pa
sudo sed -i '39s/hw:1,0/hw:2,0/' .config/pulse/default.pa

# Setup system bus
sudo sed -i 's:\btc\b:msmd:g' /usr/local/share/dbus-1/system.conf
sudo sed -i 's:\bpulse\b:msmd:g' /usr/local/etc/dbus-1/system.d/pulseaudio-system.conf

# Test pulseaudio & dbus
#/usr/local/etc/init.d/dbus start
#/usr/local/etc/init.d/dbus status
#eval $(dbus-launch --sh-syntax) pulseaudio -v
