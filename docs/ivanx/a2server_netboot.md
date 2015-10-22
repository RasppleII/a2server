## A2SERVER

You can set up A2SERVER to let your Apple IIgs or IIe boot into GS/OS or
ProDOS 8 over the network, rather than from a local drive. It can even
download and install ProDOS 8 and GS/OS for you, meaning you can get up and
running from \"bare metal\" if you wanted to.

To do this, [log into the a2server console](a2server_commands.md), and type:

```
a2server-setup
```

After confirming that you want to proceed, you will be asked if you want to
set up A2SERVER for network boot. Just follow the prompts. If you elect to
install GS/OS, be prepared to wait for a while. You will also be given the
option to install various utilities (GSHK, Asimov, and MountIt for GS/OS;
ShrinkIt, DSK2FILE, and Apple System Utilities for ProDOS 8.)

For an Apple IIgs, set the startup slot to Slot 7 (ROM 01) or AppleTalk (ROM
3). For an Apple IIe, put the Workstation Card in a slot higher than any other
drive interface card, or type PR#x where x is the slot number; you must hold
down the Open-Apple key when you press return.

When your Apple II boots up, it will try to boot from the network. If it\'s
working, you\'ll see a flashing asterisk on a IIe, or a progression of periods
at the upper left of the screen on a IIgs. You may or may not be asked to
choose \"a2server\" or \"raspberrypi\" as your server.

Log in as Guest and select the A2FILES volume, and also the GSFILES volume if
you\'re using a IIgs. (If you are booting into GS/OS, you can also log in as a
registered user, but it\'s exactly the same.)

ProDOS 8 and GS/OS are stored on the volume /A2FILES; filenames are all caps
and subject to the usual ProDOS restrictions. IIgs users can store files on
the volume /GSFILES with mixed case, punctuated names of up to 31 characters.

If you installed GS/OS, you\'ll see a folder called GSOS.INSTALLER. In there,
IMAGES contains all the GS/OS floppies, which can be turned back into disks by
using Asimov in the IMAGE.TOOLS folder. You can also use run the GS/OS
installer from the NET.INSTALL folder instead of using disks.

A IIgs can network boot into either GS/OS or ProDOS 8 by default, which you
specify in the Network control panel of GS/OS, or within ProDOS 8 by running
NETBOOT.GSOS or NETBOOT.P8, which you\'ll find in A2FILES (both reboot the
computer immediately). You can temporarily network boot into ProDOS 8, without
changing the GS/OS default, by pressing \"8\" while the dots are filling in
during the first phase of the network boot (thanks to Geoff Body for this).
