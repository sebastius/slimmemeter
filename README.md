# slimmemeter
Slimme meter uitlezen (ik heb een oudje)

udev rules
* lsusb
* sudo -s
* echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK="ttyMetertrekker"' >> /etc/udev/rules.d/99-serialmeuk.rules
* udevadm trigger
