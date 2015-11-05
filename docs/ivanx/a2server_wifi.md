## A2SERVER

While wired Ethernet is recommended, it's possible to use A2SERVER with Wi-Fi
if you have an Apple AirPort or Time Capsule. (A2SERVER won't work with most
non-Apple router and access point models, as they are not designed to handle
AppleTalk networking.)

To connect your Apple II via Wi-Fi, read how to [attach your Apple II to your
local network](a2server_lan.md).

If you want your A2SERVER machine (whether virtual, real, or Raspberry Pi) to
connect to your network via Wi-Fi, you first need to configure a Wi-Fi network
adapter via the instructions below. Once you've got that up and running, [log
in](a2server_commands.md) to A2SERVER and type `netatalk-wifi` to tell
A2SERVER to use the Wi-Fi interface (if you get "command not found", type
`a2server-setup` to refresh the command list).


Setting up Wi-Fi on your A2SERVER machine:

### Multiple AirPorts

As an alternative to using a Wi-Fi network adapter, any of the machine types
below can work with Wi-Fi simply by connecting the wired Ethernet interface to
another AirPort and setting up an [extended network][1] (if all AirPorts are
802.11n models), or a [WDS][2] (if any AirPort is an 802.11g model).


### Raspberry Pi

[We got a whole page about that.][3]


### Virtual machine

On a virtual machine, A2SERVER won't work over Wi-Fi with the virtual network
interface, but you may, or may not, be able to use a USB Wi-Fi adapter
attached your VM's emulated USB port, and then follow the instructions below
for a real machine. Some adapters may have issues with specific virtual
machine software; for example, Atheros 9K based adapters [do not work with
VirtualBox][4] or VMWare Fusion, though they do work with Parallels Desktop;
Realtek 81xx based adapters seem to work with VirtualBox (at minimum).


### Real machine (Intel or compatible)

On a standard computer with a native Linux installation, if you can get a
Wi-Fi adapter working, it will probably work with A2SERVER. Instructions will
vary by distribution, but should be similar to [the guide for Raspberry
Pi][3], with a much wider range of usable adapters.

If those steps don't work, type `sudo nano /etc/network/interfaces`, and edit
the file so it contains a sequence of lines that look like this:
`allow-hotplug wlan0 iface wlan0 inet dhcp wpa-ssid MyNetworkName` (substitute
your Wi-Fi network name) `wpa-psk abcdefgh` (substitute your WPA password, or
its 64-character hex equivalent)

If you are using WEP encryption instead of WPA, replace the last two lines
with: 
`wireless-essid MyNetworkName` (substitute your Wi-Fi network name) 
`wireless-key abcde` (substitute your 5 or 13 character, or 10 or 26 hex byte, 
WEP password)

Spaces in the Wi-Fi network name or password may not work.

Remove any other chunks which mention wlan0, and save the file (press
control-w). Then type: `sudo ifdown wlan0; sudo ifup wlan0`

Finally, type `ip addr`. If you see an IP address for wlan0 (next to
"inet"), your Wi-Fi adapter is on your network, and you can disconnect your
Ethernet or serial cable. (If you don't seem to have internet access, type
`sudo shutdown -r now` to restart.)


[1]: http://support.apple.com/kb/HT4259
[2]: http://support.apple.com/kb/HT4262
[3]: http://ivanx.com/raspberrypi/raspberrypi_wifi.html
[4]: https://www.virtualbox.org/ticket/9511
