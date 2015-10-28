## A2SERVER

So you got a [Raspberry Pi][1]. Congratulations!
 Are you ready to turn it into a file server for your Apple II? Here's how.

<!--
*Important: As of 11-Aug-14, A2SERVER 1.2.0 is now compatible with the latest
version of Raspbian (NOOBS 1.3.9/2014-Jun-20), and the Raspberry Pi Model B+.
Type `a2server-setup` to update. If you are already running A2SERVER, and it
stopped working after a Raspbian update, see the
[recovery page](a2server_recovery.md).*
-->



_Starting fresh:_
If you haven't already started working with a Raspberry Pi, then [download
Raspple II][2], a distribution of the Raspbian operating system which includes
A2SERVER, [A2CLOUD][3], and David Schmenk's [Apple II Pi][4].

Expand the RasppleII.zip file, and copy all of its files to a 4 GB or larger
SD card. Then put the SD card in your Pi, and attach power. The operating
system will automatically install, which will take about 20 minutes.

When it's done, your Pi will reboot into Raspbian. If you don't have a
screen attached, you'll know when it's done when the ACT/OK lamp on the
Raspberry Pi board stops flickering.

(If you are starting over with the same SD card, or want to ensure the card is
formatted correctly, you can use the official [SD Formatter][5] utility --
carefully! -- before copying the files.)

If you wish to log in (you don't need to to use A2SERVER), the username is
"pi" and password "apple2". (If you do not have a screen and keyboard
attached to your Raspberry Pi, read about [logging into a Raspberry Pi from
another computer](a2server_raspberrypi_login.md), including an Apple II.) If
you wish to change any configuration options, type `raspi-config`.

For next steps, check out the links on the [A2SERVER home page](index.md).


_Already using a Raspberry Pi?_ If you're already using Raspbian, you can
install A2SERVER by typing at a Linux prompt:

`wget appleii.ivanx.com/a2server/setup; source setup`

The process is straightforward -- just respond to the prompts.

For next steps, check out the links on the [A2SERVER home page](index.md).


<!--
(If you wish, you can read detailed technical information about the [AppleTalk
networking support on the Raspberry Pi](a2server_raspberrypi_kernel.md) that
A2SERVER installs.)
-->


[1]: http://www.raspberrypi.org
[2]: http://appleii.ivanx.com/rasppleii/
[3]: http://appleii.ivanx.com/a2cloud
[4]: http://schmenk.is-a-geek.com/wordpress
[5]: https://www.sdcard.org/downloads/formatter_4/
