## A2SERVER

In order to connect your Apple II to the network, you need a LocalTalk to
Ethernet bridge. (Unfortunately, the [Uthernet card][1] will not work, as
Apple's network drivers don't know what it is.)

If you have an enhanced Apple IIe, you will also need an [Apple II Workstation
Card][2], and, if you're not booting over the network, the [Workstation Card
software](a2server_howtouse.html#wsdisks). Make sure you buy one with the
dongle. \[ <!-- [Blujay][3] --> [eBay][4] \]

These are the commonly available bridges; be sure you read below about their
idiosyncracies before you buy one.

* Asante [AsanteTalk][5] and AsantePrint \[ [Asante][6] [eBay][7] \]

* Dayna EtherPrint and Mini EtherPrint (any model with an Ethernet port)   
  \[ [eBay][8] \]

* Farallon EtherWave/EtherMac/iPrint LT with LocalTalk (PN842, PN848 or
  PN559) \[ [eBay][9] \]

* A pre-USB Mac with any kind of Ethernet, and the [LocalTalk Bridge][10]
  control panel installed \[ [eBay][11] \]

You'll also need an ImageWriter II printer cable (or any other 8-pin mini-DIN
null-modem serial cable), or two LocalTalk transceivers joined by either a
LocalTalk cable or four-wire phone cord, depending on whether you have Apple
or PhoneNet transceivers. (PhoneNet transceivers also require a terminator at
both ends; it looks like a phone plug with a resistor sticking out of it.)
Connect each end to your Apple II and the bridge, and an Ethernet cable
between the bridge and your router.

For an Apple IIgs, go to the Slots control panel by pressing ctrl-Apple-ESC,
and set slot 1 or 2, depending on whether you are using the printer or modem
port for networking, to "Your Card" (ROM 01 machines) or "AppleTalk" (ROM
3 machines), and set slot 7 to "AppleTalk" (ROM 01 machines only). For an
Apple IIe, install the Workstation Card in any slot, and be sure to connect
your LocalTalk cable to the port with the double-arrow icon.

If you have multiple Apple II's you'd like to network, you can use a bridge
for each, or a single bridge attached to daisy-chained LocalTalk transceivers.

Wired ethernet is recommended, but if you have an Apple AirPort or Time
Capsule, you can use Wi-Fi by attaching your LocalTalk-to-Ethernet bridge to a
another AirPort, and setting up an [extended network][12] (if all AirPorts are
802.11n models), or a [WDS][13] (if any AirPort is an 802.11g model). (Most
non-Apple routers and access points will not work because they are not
designed to handle AppleTalk networking.)


Caveat emptor:

* The AsanteTalk must be powered on while A2SERVER is up and running, or it
  will enter a mode where it won't operate correctly. (On the AsanteTalk, you
  will know it entered the right mode if the TX light blinks a lot during
  power-up. If it instead pulses only two or three times, then goes dark for a
  little while, and then pulses very rapidly for about three seconds, you'll
  need to remove power, make sure A2SERVER is running, and try again.)

* At least some of the Dayna bridges must be attached to a 10Base-T Ethernet
  port; they won't work if attached to an autosensing 10/100 or Gigabit
  Ethernet port such as those found on modern routers and switches. You can
  [buy a 10Base-T hub on eBay][14] for around $10 to go between your router
  and the bridge.

* Farallon bridges work fine with an Apple IIe. To prevent them from freezing
  a IIgs after a couple of minutes, you can download a fix for GS/OS ([disk
  image][15] or [ShrinkIt][16] format) and put it into SYSTEM/SYSTEM.SETUP, or
  you can [log in to the A2SERVER console](a2server_commands.html) and type
  `a2server-setup` and you will be asked if you want to install it. Because
  the fix is for GS/OS only, Farallon bridges will *not* work with a IIgs
  booted directly into ProDOS 8. (Also note: the PN842 has a built-in 8-pin
  cable, and the PN848 and PN559 have a built-in PhoneNet terminated
  transceiver, so you might not need all the cabling described above.)

* Using a classic Mac as a bridge works perfectly in all cases. Set AppleTalk
  to use the Ethernet port, attach the LocalTalk tranceiver or serial cable to
  the printer port (or printer/modem port), and install [LocalTalk
  Bridge][10]. (Recommended models: PowerBook 3400 with Ethernet, PowerBook G3
  with black keyboard. Any model with both a round serial port and any kind of
  Ethernet, including via expansion card, AAUI adapter, or SCSI adapter,
  should work.)

And finally:

* The Cayman GatorBox CS and the Shiva FastPath IV and V have been reported to
  work, but it's hard to find these, so I have been unable to test. If you
  have one of these and it doesn't work, [log in](a2server_commands.html) to
  A2SERVER and type `netatalk-router-off` (if you get "command not found",
  type `a2server-setup` to refresh the command list).

* Other LocalTalk-to-Ethernet routers and bridges may work too, but haven't
  been tested by me.


Thank you:

Many thanks to Steven Hirsch, who fixed the Netatalk code in A2SERVER to make
the Asante bridges start up reliably, and prevent the Dayna bridges from
crashing the computer in GS/OS; and many thanks to Geoff Body, who contributed
the patch to GS/OS to make Farallon bridges work reliably without freezing a
IIgs after a few minutes. Also, thanks to all who have tested and sent reports
on using A2SERVER with their bridges.


[1]: http://a2retrosystems.com/
[2]: http://www.apple2info.net/hardware/a2ews/a2ews.htm
[3]: http://www.blujay.com/?keywords=workstation+card&Search.x=0&Search.y=0&Search=Search&page=search
[4]: http://www.ebay.com/sch/i.html?_nkw=apple+workstation+card+-portrait
[5]: http://www.asante.com/products/Asantetalk/Asantetalk.asp
[6]: http://www.asante.com/shop/shopdisplayproducts.asp?id=16&cat=+AsanteTalk
[7]: http://www.ebay.com/sch/i.html?_nkw=%28asantetalk%2C+asanteprint%29
[8]: http://www.ebay.com/sch/i.html?_nkw=etherprint
[9]: http://www.ebay.com/sch/i.html?_nkw=farallon+%28etherwave%2Cethermac%2Ciprint%29+-sl+-aui+-aaui+-pci+-nubus+-pds+-card
[10]: http://archive.org/download/download.info.apple.com.2012.11/download.info.apple.com.2012.11.zip/download.info.apple.com%2FApple_Support_Area%2FApple_Software_Updates%2FEnglish-North_American%2FMacintosh%2FNetworking-Communications%2FOther_N-C%2FLocalTalk_Bridge_2.1.smi.bin
[11]: http://www.ebay.com/sch/i.html?_nkw=powerbook%20(3400c%2Cg3)%20-adapter%20-pismo%20-lombard%20-bronze%20-ibook%20-g4%20-333%20-333mhz%20-400%20-400mhz%20-500%20-500mhz
[12]: http://support.apple.com/kb/HT4259
[13]: http://support.apple.com/kb/HT4262
[14]: http://www.ebay.com/sch/i.html?_odkw=10base-t+%28hub%2Cswitch%29+-fast+-100+-1000+-gigabit
[15]: http://appleii.ivanx.com/a2server/files/FARALLON.B1.PO
[16]: http://appleii.ivanx.com/a2server/files/FARALLON.B1.BXY
