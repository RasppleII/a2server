## A2SERVER

A2SERVER\'s central capability, sharing files to an Apple II, is provided by
[Netatalk][1] 2.2.4.

Here\'s the extra sauce that A2SERVER provides:

* available as a ready-to-use [Raspberry Pi][2] operating system installer

  (plus new [Pi Filler][3] and [Pi Copier][3] utilities for easy SD card
  creation and backup)

* available as a ready-to-use [VirtualBox][4] appliance for Mac OS X, Windows,
  Linux, and Solari

* simple downloadable installation script for Ubuntu Linux or Raspbian takes
  care of setting up and configuring *everything*

* enables reliable operation by Asante, Farallon and Dayna bridges on both IIe
  *and* IIgs \[fixes contributed by Steven Hirsch and Geoff Body\]

* easy to configure for network boot, including ProDOS 8 and GS/OS download
  and installation

* can network boot both IIe and IIgs computers on the same network

* new ProDOS 8 tools (NETBOOT.P8 and NETBOOT.GSOS) for setting the IIg network
  boot default

* temporary ProDOS 8 network boot without changing GS/OS default \[contributed
  by Geoff Body\]

* GS/OS installer that can be run from folders rather than disk

* installs ProDOS 8 and GS/OS utilities for working with archive (ShrinkIt and
  GSHK), disk images ([DSK2FILE][5] / [Asimov][6] / [MountIt][7]), and file
  (Apple ProDOS System Utilities)

* supports Wi-Fi when used with Apple AirPort or Time Capsul

* maintains correct dates during GS/OS folder copy \[fix contributed by Steven
  Hirsch\]

* uses randnum authentication for registered user sign-in (which alway works,
  unlike cleartext)

* supports login to shared volumes from latest versions of OS X and Window

* new Linux tool ([afptype](scripts/tools/afptype.txt)) for setting ProDOS or
  classic Mac file types on shared volume

* new Linux tool ([cppo](scripts/tools/cppo.txt)) for cataloging and copying
  files (with optional resource forks) out of ProDOS disk image

* [Linux commands](a2server_commands.md) to ease server maintenanc

* installs Linux tools for working with ShrinkIt and other old and new archive
  formats ([nulib2][8] and [unar/lsar][9])

<!--
* sets up Raspberry Pi for shell login from Apple II via USB-serial cable or
  Raspberry Pi console cable
-->

* blinks Raspberry Pi OK/ACT LED for ten seconds when netatalk has just
  started

* good documentation (or so I hope)


Any content unique to A2SERVER and not covered under a specific license is
licensed under the [WTFPL][10].


[1]: http://netatalk.sourceforge.net
[2]: http://www.raspberrypi.org
[3]: http://ivanx.com/raspberrypi/
[4]: http://www.virtualbox.org
[5]: http://www.dwheeler.com/6502/oneelkruns/dsk2file.html
[6]: http://www.ninjaforce.com/html/products.html
[7]: http://www.brutaldeluxe.fr/products/apple2gs/mountit.html
[8]: http://www.nulib.com
[9]: http://unarchiver.c3.cx
[10]: http://www.wtfpl.net
