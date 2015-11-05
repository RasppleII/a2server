## A2SERVER

If you had A2SERVER running, and you typed either `apt-get update` or
`rpi-update`, you may have received Linux kernel version 3.12 through 3.15.
These, unfortunately, include a defective AppleTalk kernel module which will
kernel panic (crash) your system on startup when A2SERVER tries to activate
AppleTalk networking.

If you have a screen or console cable attached, you will see some debugging
information that concludes with "Kernel panic." If you don't have a screen
attached, there will be no visible signs other than that you simply can't
connect from another computer on your network.

To prevent this from happening, type `a2server-setup` *before* updating the
software on your computer. If it's too late, and you need to recover from
this situation, you could [start over][1]. Or, if you want to keep your
current installation, you have a few options, depending on your setup:


### A2SERVER virtual machine, or on other non-Raspberry Pi Linux computer

* Start up the virtual or real machine.

* On the GRUB startup screen, choose the Recovery kernel.

* At the Linux prompt, type `a2server-setup`


### A2SERVER on Raspberry Pi with screen/keyboard/mouse attached

* Press the shift key rapidly and repeatedly while your Pi starts up. If you
  have an HDMI monitor, you can stop when you see the installer screen. If you
  have a composite monitor, stop after about a minute, and then press 3 (PAL,
  e.g. Europe) or 4 (NTSC, e.g. North America and Japan), and you should see
  the installer screen.

* Press E for Edit, then click the *cmdline.txt* tab.

* At the end of the line, append `single` (preceded by a space).

* Press OK to save, then ESC to reboot.

* Log in with username "pi" and password "apple2".

* At the Linux prompt, type `a2server-setup`


### A2SERVER on Raspberry Pi without screen/keyboard mouse, and a Mac

* Remove the SD card from your Pi and insert it in your Mac.

* Look for a volume named BOOT to appear.

* Within it, open *cmdline.txt* in a text editor (the default is TextEdit).

* At the end of the line, append `single` (preceded by a space), then save it.

* Eject the SD card and put it back in your Pi, then start up your Pi.

* [Log in to your Pi](a2server_raspberrypi_login.md) and type `a2server-setup`


### A2SERVER on Raspberry Pi without screen/keyboard mouse, and a Linux computer

* Remove the SD card from your Pi.

* On your Linux computer, type:
  
  ~~~ bash
  wget ivanx.com/a2server/fix; source fix
  ~~~

* Follow the on-screen instructions.

* If after using the fix tool, you still can't connect from your Apple II,
  [log in to your Pi][2], and type `a2server-setup`

* (Alternative approach: Follow the Mac method above, though the volume may
  not appear as BOOT.)


### A2SERVER on Raspberry Pi without screen/keyboard/mouse, and a Windows computer

* Remove the SD card from your Pi.

* Install the [A2SERVER virtual machine](a2server_virtualbox.md) on your
  Windows computer.

* Start the virtual machine, and log in with user name "user1" and
  password "apple2".

* In the virtual machine window, type:

  ~~~ bash
  wget ivanx.com/a2server/fix;source fix
  ~~~

* Follow the on-screen instructions.

* Type `system-shutdown` in the virtual machine window.

* Quit VirtualBox.

* If after using the fix tool, you still can't connect from your Apple
  II, [Log in to your Pi](a2server_raspberrypi_login.md) and type
  `a2server-setup`


[1]: http://ivanx.com/a2server/
