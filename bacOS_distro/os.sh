#installing the dependencies
sudo apt install bc binutils bison dwarves flex gcc git gnupg2 gzip libelf-dev libncurses5-dev libssl-dev make openssl pahole perl-base rsync tar xz-utils

#creating the workspace
mkdir bacOS

#downloading the kernel with its signature
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.9.8.tar.xz
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.9.8.tar.sign

unxz --keep linux-6.9.8.tar.xz

#verifying the signature by importing the keys
gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org
gpg2 --verify linux-6.9.8.tar.sign

#extracting the kernel
tar xf linux-6.9.8.tar
mv linux-6.9.8 bacOS
cd bacOS/linux-6.9.8

#using the config file from the host system(debian 12 in my case) i am going to use a custom config in the future for security reasons
cp /boot/config-"$(uname -r)" .config
make olddefconfig

#since the kernel's signature is not verified, i am going to disable it
./scripts/config --file .config --disable MODULE_SIG

#setting the local version
./scripts/config --file .config --set-str LOCALVERSION "-pratham"

#building the kernel
make -j$(nproc) 2>&1 | tee log
sudo make modules_install -j$(nproc)
sudo make install
