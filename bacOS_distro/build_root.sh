#!/bin/bash
cd root
find . | cpio -o -H newc | gzip > ../iso/boot/root.cpio.gz
cd ..