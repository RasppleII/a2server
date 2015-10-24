## A2SERVER


To set up A2SERVER, follow these steps:

* Download and install [VirtualBox][1]. It\'s free. (If you prefer different
  virtual machine software, [you can instead use the A2SERVER installer
  script](a2server_installer.md).)

* Download the [A2SERVER virtual machine](files/A2SERVER.ova) (~750 MB), or
  the [A2SERVER+A2CLOUD virtual machine](files/A2SERVER_A2CLOUD.ova) (~1.7
  GB).

* Open VirtualBox, and choose \"Import Appliance...\" from the File menu.
  Select the file you downloaded (A2SERVER.ova).

* Leave the \"Reinitialize the MAC address of all network cards\" box
  unchecked. Click Import.

* When it\'s done importing, click A2SERVER, then click Settings, then click
  Network.

* Ensure that \"Attached To:\" is set to \"Bridged Adapter\".

* Set \"Name:\" to a _wired_ network interface on your computer. If you don\'t
  have one, use a USB-to-Ethernet adapter. (A2SERVER won\'t work over Wi-Fi in
  a virtual machine.)

* Click OK.


You\'re all set up. For next steps, check out the links on the [A2SERVER home
page](index.md).


SHA-1 for A2SERVER VM: d6c60b0ab14f14ddd49b7e5cdac39503db96a903 
SHA-1 for A2SERVER+A2CLOUD VM: 69df7c28fa21e4e4cc01b106398936f23559a64b 
<!--
v1.1.3: a8927d6fba9dfa9c2015918cdc61122bb2c95ea5 
v1.1.0: 63eebfcfe9fbbeb17aa4ab3226e849289072d396
-->


[1]: https://www.virtualbox.org/wiki/Downloads
