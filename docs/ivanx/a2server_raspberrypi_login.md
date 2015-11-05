## A2SERVER

You need to access the Raspberry Pi's command prompt in order set up A2SERVER
for network boot, and [do other stuff](a2server_commands.md).

The default username is "pi" and default password is "apple2". If you
don't have a screen and keyboard attached, you can:


### Log in via SSH from another computer

On a Mac, open Terminal (in the Utilities folder of the Applications folder),
and type `ssh pi@raspberrypi.local` to connect. If you have Windows, you can
install [Bonjour Print Services][1], and then use [PuTTY][2] to connect to the
address "raspberrypi.local".

If that doesn't work, or you don't want to install Bonjour Print Services
for Windows, you will need to find your Pi's IP address and use that instead.
If you have a Mac, you can use [Pi Finder][3] to help with this; if you have
Windows, you can use [Advanced IP Scanner][4]. Once logged in, you can type
`showmac` to see your Pi's MAC (Ethernet) address, and you can use this to
reserve an IP address in your router so the Pi gets the same IP address every
time.


### Log in from an Apple II

There are a few different options for logging in from an Apple II. They are:

* Apple II serial: With the appropriate cables, you can use a terminal
  communications program such as [ProTERM][5], [Spectrum][6], or Z-Link
  to log into and control your Raspberry Pi. All this is set up
  automatically with [A2CLOUD][7], so head over there to read about how
  to install it and find out what cables you need to get.


* Apple II Ethernet: If you have an [Uthernet Card][8] in an Apple IIgs, you
  can log into your Raspberry Pi with [Spectrum][6] using VT100 emulation
  (once logged in, type `TERM=vt100`). To make this work you will need to
  first log into your Pi by one of the above methods, and type `sudo apt-get
  -y install telnetd` (you may not wish to do this if your Pi is on a network
  with any untrusted users, as Telnet is unencrypted). Also, note your Pi's
  IP address (you can type `showip` once logged in) so you can provide it to
  Spectrum Internet Suite; you might want to put a DHCP reservation into your
  router (type `showmac` to get your Pi's MAC address) so you don't have to
  figure it out again.


[1]: http://support.apple.com/kb/dl999
[2]: http://www.chiark.greenend.org.uk/~sgtatham/putty/
[3]: http://ivanx.com/raspberrypi/files/PiFinder.zip
[4]: http://www.advanced-ip-scanner.com
[5]: http://lostclassics.apple2.info/downloads/?dl_cat=11
[6]: http://www.wannop.info/speccie/Site/Speccies_Home_Pages.html
[7]: http://appleii.ivanx.com/a2cloud/
[8]: http://a2retrosystems.com
