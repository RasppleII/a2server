## A2SERVER

Sometimes you need to access the A2SERVER command line to set up network boot
or do other stuff. A list of commands is below.

If you are running A2SERVER on a Raspberry Pi without a screen and keyboard
attached, see how to
[log in to a Raspberry Pi](a2server_raspberrypi_login.md).

Otherwise, log in on your local console or virtual machine window, or via SSH
on another computer. On Mac OS X, or Windows with [Bonjour Print Services][1]
installed, you can use "raspberrypi.local" for your SSH address, or
"a2server.local" if not on a Pi. If that doesn't work, try updating
A2SERVER by typing `a2server-setup`.

If it still doesn't work, or you don't want to install Bonjour Print
services for Windows, you will need to use A2SERVER's IP address instead,
which you can see by typing `showip`. You can create a DHCP reservation in
your router to give A2SERVER the same IP address every time. To do this,
you'll need the MAC (Ethernet) address of the machine (or virtual machine)
running A2SERVER, which you can see by typing `showmac`. If you are using the
premade virtual machine, the MAC is 08:00:03:F2:FF:59 .

The default username is either "pi" for Raspberry Pi, and otherwise
"user1". The password is "apple2". (The password is "raspberry" for an
standard installation of Raspbian; you can use the
[installer script](a2server_installer.md) to install A2SERVER.)

Shared volumes can be found at /srv/A2SERVER. Netatalk configuration files
are in /usr/local/etc/netatalk.

Once logged in, you can enter the following commands.

(If any of these yield "command not found", refresh the command list by
typing `a2server-setup`, answering "no" to all prompts if you like.)


~~~
A2SERVER commands:
  (note: new commands may be added; use a2server-setup to refresh)

a2server-help: show this list of commands
a2server-setup: set up network boot, Windows access, Farallon fix,
    refresh command list
a2server-version: see installed version of A2SERVER
a2server-update: check for update to A2SERVER

system-shutdown: shut down the server
system-restart: shut down and restart the server

 Raspberry Pi commands, if you're using one:
raspi-config: utilize all space on RPi SD card & other options
raspbian-update : update Raspbian operating system
rasppleii-update : update Raspbian OS, A2CLOUD, A2SERVER, Apple II Pi

welcome-message-edit: change the welcome message

showip: show the current ethernet IP address of the server
showmac: show the MAC (Ethernet hardware) address of the server
showip-wifi: show the current wifi IP address of the server
showmac-wifi: show the MAC (wifi hardware) address of the server
ifreset: reset all network interfaces (requires restart)

netatalk-stop: stop the netatalk service until reboot
netatalk-start: start the netatalk service
netatalk-restart: restart the netatalk service
netatalk-off: disable the netatalk service (even after reboot)
netatalk-on: enable the netatalk service

bonjour-off: disable advertisement of shared folders to OS X
bonjour-on : enable advertisement of shared folders to OS X
  (these are automatically set by the netatalk commands above)

netatalk-router-on: use netatalk in router mode (default)
netatalk-router-off: use netatalk in node mode
  (use if there is an AppleTalk router such as a GatorBox present)

netatalk-eth: use wired ethernet interface for netatalk (default)
netatalk-wifi: use wifi interface for netatalk
    note: if an interface isn't available, netatalk will be reset with
    router mode off; use "netatalk-router-on" to correct this if needed

appletalk-off: disable AppleTalk networking (even after reboot)
appletalk-on : enable AppleTalk networking

environment variables:
$NETATALK: directory containing netatalk configuration files
$A2FILES : directory containing A2FILES shared volume
$GSFILES : directory containing GSFILES shared volume

netboot-gsos: set the current user to netboot into GS/OS (default)
netboot-gsos-guest: set guests to netboot into GS/OS
netboot-p8: set the current user to netboot into ProDOS 8
netboot-p8-guest: set guests to netboot into ProDOS 8 (default)
  note: when a IIgs is set to network boot into GS/OS, using the Network
  control panel or the NETBOOT.GSOS utility, guests will behave like
  registered users, and ignore the netboot setting of the guest user

guest-off: disallow guest access to A2SERVER
guest-on: allow guest access to A2SERVER (default)
  note: by default, Guest access is the only way to network boot into
  ProDOS 8. For registered user boot into ProDOS 8, type "netboot-p8"

samba-off: disable Windows file sharing (even after reboot)
samba-on: enable Windows file Sharing
samba-stop: stop Windows file sharing until reboot
samba-start: start Windows file sharing
samba-restart: stop and restart Windows file sharing

gsfiles-share: disable the GSFILES shared volume
gsfiles-unshare: enable the GSFILES shared volume
a2files-share: disable the A2FILES shared volume
a2files-unshare: enable the A2FILES shared volume

nulib2: create, extract, and work with NuFX (ShrinkIt) archive files
unar: extract other archive files (multiformat)
lsar: list contents of other archive files (multiformat)

afptype: set the ProDOS type/auxtype or Mac OS type/creator of a file
afpsync: register files introduced outside of AFP with netatalk
mkatinit: set up network boot configuration files
cppo: catalog and copy files from ProDOS image file (slow, but works)
  (add -h to show help for the above four commands, e.g. "afptype -h")

~~~


[1]: http://support.apple.com/kb/dl999
