## A2SERVER

 These steps cover how to install Ubuntu Server Linux into your empty virtual or real machine. (The instructions are similar, but may vary somewhat, for Debian Linux.)

* Download [Ubuntu Server 12.04 LTS][1], and burn it to a CD if
  installing on a real machine; otherwise, attach the download to your
  virtual machine's CD/DVD drive.

* Click Start.

* Answer all the region related questions and choose to Install Ubuntu
  Server.

* For hostname, enter *a2server*

* Under Partition Disks, choose "Guided - use entire disk" (no LVM).

* Choose SCSI1 (or whatever other disk appears), and (two screens later)
  confirm "Write the changes to disks."

* If you are installing Debian, and are prompted for a domain name or
  the root user password, leave them blank.

* Enter *user1* as the full name for the new user, and as the username
  for your account

* Choose *apple2* as the password, verify by retyping, and then confirm
  weak password

* Choose not to encrypt your home directory

* If you require an HTTP proxy, enter it, or leave it blank if not.

* Choose yes to Install the GRUB boot loader to the master boot record

* Choose no automatic updates

* Choose OpenSSH under Software Selection (and, for Debian, Standard
  System Utilities)

* Click Continue to reboot

* When prompted, log in with username *user1* and password *apple2*.

* If you installed Debian rather than Ubuntu, type:
  
  ~~~ bash
  sudo sed -i '0,/-eq 0/s/-eq 0/-ge 0/' /etc/profile
  ~~~

* When you're back at the prompt, type `sudo shutdown -h now` which
  will turn off the (virtual) machine.

* Recommended: If you are using a virtual machine, take a snapshot you
  can return to this point if necessary.


[1]: http://www.ubuntu.com/download/server/download
