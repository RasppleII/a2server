## A2SERVER

The following steps explain how to prep the A2SERVER virtual machine,
specifically [VirtualBox][1], which has the notable virtue of being free.
However, you can also use other virtual machine products, such as those from
[Parallels][2] and [VMware][3], and the process should be similar.

If you're comfortable doing so, you may also customize the steps below as you
wish, or install Ubuntu Linux natively rather than in a VM.

* Download [VirtualBox 4.2.10][4].

* Download [Ubuntu Server 12.04 LTS][5] (A2SERVER has been tested with the
  32-bit version only).

* Start VirtualBox, and go to Preferences.

* Click Input. Set the host key to right-alt, and uncheck Auto Capture
  Keyboard.

* Click OK.

* Click New to create a new virtual machine.

* Enter *A2SERVER* as the VM name, and select Linux/Ubuntu as the operating
  system.

* Enter 256 MB for memory.

* Under Virtual Hard Disk, leave the defaults (Start-up Disk, and Create new
  hard disk).

* Choose VMDK for hard disk file type.

* Leave the virtual disk file as Dynamically allocated.

* Leave the virtual disk file location as A2SERVER, and set the disk size to
  32 GB.

* Click Create, and then again in the next window.

* Click Settings.

* Click Storage. Click on \"Empty\" under \"IDE Controller\".

* Click on the small CD icon on the far right of the window, select \"Choose a
  virtual CD/DVD disk file...\", and choose the Ubuntu Server file you
  downloaded.

* Click Network.

* Change \"Attached To:\" to \"Bridged Adapter\".

* Change \"Name:\" to a **wired** network interface on your computer.  If you
  don't have one, use a USB-to-Ethernet adapter. (A2SERVER won't work over
  Wi-Fi when running in a VM.)

* Optional but recommended: Under Advanced, change the MAC Address to
  080003F2FF59.

* Click OK.


[1]: http://www.virtualbox.org/
[2]: http://www.parallels.com/
[3]: http://www.vmware.com/
[4]: https://www.virtualbox.org/wiki/Downloads/
[5]: http://www.ubuntu.com/download/server/
