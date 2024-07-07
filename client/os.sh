sudo apt install bc binutils bison dwarves flex gcc git gnupg2 gzip libelf-dev libncurses5-dev libssl-dev make openssl pahole perl-base rsync tar xz-utils
mkdir bacOS
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.9.8.tar.xz
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.9.8.tar.sign
unxz --keep linux-6.9.8.tar.xz
gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org
gpg2 --verify linux-6.9.8.tar.sign
tar xf linux-6.9.8.tar
mv linux-6.9.8 bacOS
cd bacOS/linux-6.9.8
cp /boot/config-"$(uname -r)" .config
make olddefconfig
./scripts/config --file .config --disable MODULE_SIG
./scripts/config --file .config --set-str LOCALVERSION "-pratham"
make -j$(nproc) 2>&1 | tee log
