## A2SERVER

To connect to A2SERVER from your Apple II:

(An alternative to the below is to [boot your Apple II over the
network](a2server_netboot.md) -- check that out too.)

Start up A2SERVER and wait (potentially up to a minute) until you get to the
login prompt. You do not need to log in. On a Raspberry Pi, you can see that
it's ready when the the normally irregular ACT or OK LED blinks steadily and
rapidly for ten seconds.

If you are on a IIe, boot from the [Workstation Card disk](#wsdisks), and
choose "Log On".

If you are on a IIgs, open the AppleShare control panel. If you don't have
it, use the GS/OS installer disks to custom install the script called
"Network: AppleShare" to your startup disk. If you are on a floppy-only
system, you can instead use the script "Network: AppleShare, 3.5" disk" to
make a bootable disk, or consider setting up
[network boot](a2server_netboot.md).

(There is also an obsolete [IIgs Workstation Disk](#wsdisks) that boots into
ProDOS 16 rather than GS/OS, and has the same ProDOS 8 applications for server
access as the IIe disk. You probably don't want to use it.)

"a2server" or "raspberrypi" should appear in the list of server names. Log
in as Guest and select the A2FILES volume, for ProDOS 8 storage, and/or the
GSFILES volume, for GS/OS storage. (You can also log in as a registered user,
but it's exactly the same.)

On the A2FILES volume, filenames need to be all caps and are subject to the
usual ProDOS restrictions (letters/numbers/periods only, first character must
be a letter, 15 characters max). IIgs users can store files on GSFILES with
mixed case, punctuated names of up to 31 characters (same as a classic Mac).

The network volumes hosted by A2SERVER will appear on the Finder desktop in
GS/OS; in ProDOS 8, you can type `PREFIX /A2FILES`.

### Workstation Software: ###  {#wsdisk}

<!--
FIXME: These disk images are not (at present) contained within this archive.
Moreover, they cannot be directly included in properly "Open Source" packages
of A2SERVER which ought to include this archive.  They'll have to be external
links, but I'm not fixing that right now.  -tjcarter,2015-10-22
-->

* IIe Workstation Card, 800K:
  [raw image](files/a2ws/A2E.WS.FULL.HDV)
  [ShrinkIt image](files/a2ws/A2E.WS.FULL.BXY)

* IIe Workstation Card, Logon/Logoff/BASIC only, 140K:
  [raw image](files/a2ws/A2E.WS.LITE.DSK)
  [ShrinkIt image](files/a2ws/A2E.WS.LITE.BXY)

* IIe Workstation Card, System Utilities/BASIC only, 140K:
  [raw image](files/a2ws/A2E.WS.UTIL.DSK)
  [ShrinkIt image](files/a2ws/A2E.WS.UTIL.BXY)

* IIgs Workstation, 800K \[superseded by GS/OS AppleShare software\]:
  [raw image](files/a2ws/A2GS.WS.HDV)
  [ShrinkIt image](files/a2ws/A2E.WS.BXY)
