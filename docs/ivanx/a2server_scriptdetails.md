## A2SERVER

When you type A2SERVER-setup, a series of scripts are downloaded from
appleii.ivanx.com and executed, some with root privileges. They are run from
the /tmp folder, and deleted upon completion.

Here is what they do, in the order shown (click the links to view the scripts
themselves):

[Master setup script](setup/index.txt)

* checks for supported OS and warns if it isn't

* offers to change user password (Raspberry Pi only)

* runs all of the scripts below

* offers to download a replacement kernel with AppleTalk support (Raspberry Pi
  only)


[Storage setup](scripts/a2server-1-storage.txt) (runs during initial setup, skipped on subsequent runs)

* Make the /srv/A2SERVER directory


[A2SERVER tools install](scripts/a2server-2-tools.txt) (always runs)

<!--
* update package list and upgrade packages (apt-get update/upgrade)
-->

* download, compile, and install nulib2 (ShrinkIt archive utility), into
  /usr/local/bin

* install libraries required for compiling [The Unarchiver][1]

* download, compile, and install unar/lsar (The Unarchiver), into
  /usr/local/bin

* install A2SERVER tools into /usr/local/bin and /usr/local/etc:
  [afpsync](scripts/tools/afpsync.txt),
  [afptype](scripts/tools/afptype.txt),
  [cppo](scripts/tools/cppo.txt),
  [mkatinit](scripts/tools/mkatinit.txt),
  [volnifo](scripts/tools/mkvolinfo.txt),
  [aliases](scripts/tools/a2server-aliases.txt) (described at the bottom of
  [this page](a2server_commands.html))

* set up aliases file to be read at each login (/etc/profile)

* customize pre-login message on Ubuntu (/etc/issue), or post-login message on
  non-Ubuntu (/etc/motd)


[Netatalk install and configure](scripts/a2server-3-sharing.txt) (runs during
initial setup and if upgrade to Netatalk is required; otherwise skipped)

* stop Netatalk service if it is running

* update package list and upgrade packages

* download and install libraries required for compiling Netatalk

* download Netatalk source code

* modify source code to make dates work correctly

* compile and install Netatalk

* set up Netatalk configuration files for Apple II use

* start Netatalk service


[Network boot setup](scripts/a2server-5-netboot.txt) (always runs)

* ask whether user wants network boot (skips to the last step in this section
  if not)

* download boot blocks disk from Apple and convert it to raw block dump file

* copy boot blocks files and BASIC.SYSTEM

* use mkatinit to enable Apple II network boot

* patch boot block files to support cleartext passwords, and typing "8"
  during IIGS network startup to force ProDOS 8 boot

* ask user whether to download and install GS/OS

* ask whether user wants to download disk image and file utilities

* ask whether user wants to install Farallon bridge patch


[Windows file sharing](scripts/a2server-6-samba.txt) (always runs)

* ask whether user wants Windows file sharing, and if so:

* download and install samba, and start the service

* set up samba configuration files

* if user doesn't want Windows file sharing, stop the samba service


[Console optimizing](scripts/a2server-7-console.txt) (runs during initial
setup, skipped on subsequent runs)

* disable default Ubuntu Server login message

* make console clear boot messages before initial login prompt

* eliminate piix4\_smbus error message before initial login prompt

* prevent console from going blank after ten minutes of inactivity (after
  login)

* resolve a slow-scrolling problem in Ubuntu Server 10.04 (only)


[1]: http://wakaba.c3.cx/s/apps/unarchiver.html
