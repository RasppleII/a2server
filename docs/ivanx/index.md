## A2SERVER

A2SERVER lets you use a [Raspberry Pi][1], or almost any other computer, to
serve files to Apple IIgs and enhanced IIe computers on your network. You'll
also be able to boot into GS/OS or ProDOS 8 directly from tne network (no
drives needed). A2SERVER has been designed to be as easy to set up and use as
possible, and it's free.

<!--
A2SERVER is available as a Raspberry Pi installer, or a virtual machine which
runs on Mac OS X, Windows, Linux, or Solaris computers, or as an easy-to-use
installer for Ubuntu or Debian Linux.
-->

 A2SERVER is based on open-source software, primarily [Netatalk][2] 2.2.4,
 with [many utilities and enhancements](a2server_features.md) to make
 everything as easy as possible. (If you like A2SERVER, you might also want to
 check out [A2CLOUD][3].)

<!--
If you haven't checked out A2SERVER in a while: it now runs on something
small, cheap, and silent, and every common LocalTalk-to-Ethernet bridge now
works easily with a IIgs (as opposed to none previously). And A2SERVER
supports Wi-Fi, and can download and install GS/OS on your network drive for
you. Cool stuff!
-->

 _Update 19-Mar-15: A2SERVER 1.2.2 is available. It has support for Raspberry
 Pi 2 Model B and every other Raspberry Pi, and new command line options for
 the installer script. To update, type `a2server-setup`._

Choose how you'd like to use A2SERVER, and you'll be up and running shortly.

 * [Raspberry Pi](a2server_raspberrypi.md)
 * [Virtual Machine](a2server_virtualbox.md) (for Mac OS X, Windows, Linux,
   Solaris)
 * [Installer for Ubuntu or Debian Linux](a2server_installer.md)


Once you've got it set up, here are next steps:

[Attach your Apple II to your local network](a2server_lan.md)

[Connect to A2SERVER from your Apple II](a2server_howtouse.md)

[Boot into ProDOS 8 or GS/OS over the network](a2server_netboot.md)

[Log into, shut down, and do stuff in the A2SERVER
console](a2server_commands.md)

[Access A2SERVER files from a Mac or Windows computer](a2server_access.md)

[Use A2SERVER with Wi-Fi](a2server_wifi.md)


And some other stuff that might (or might not) be helpful or interesting:

[A2SERVER feature list](a2server_features.md)

[A2SERVER version history](update/versionhistory.txt)

[Recover from a crashed A2SERVER](a2server_recovery.md)

[Details of what the "a2server-setup" script
does](a2server_scriptdetails.md)

[See the March 2013 cover of Juiced.GS][4], featuring A2SERVER

[Watch me introduce A2SERVER at KansasFest 2011][5] (note: this contains some
outdated information)

[The A2SERVER odyssey](a2server_story.md) (warning: long)


Buckets of thanks to Steven Hirsch and Geoff Body, whose invaluable assistance
and contributions have made A2SERVER exist, along with Tony Diaz, Antoine
Vignau, Peter Wong, Martin Haye, Ken Gagne, Peter Neubauer, Anthony Martino,
James Littlejohn, and others at comp.sys.apple2 and KansasFest. (As well as
the creators, past and present, of Netatalk and Raspberry Pi.) Apple II
Forever!

Questions? Comments? email [ivan@ivanx.com](mailto:ivan@ivanx.com)

[Apple II Extravaganza home page](http://appleii.ivanx.com/)


[1]: http://www.raspberrypi.org
[2]: http://netatalk.sourceforge.net
[3]: http://ivanx.com/a2cloud
[4]: http://juiced.gs/2013/03/v18i1-now-shipping/
[5]: http://www.youtube.com/watch?v=w88NjWRK7Kk
