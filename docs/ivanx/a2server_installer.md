## A2SERVER

You can easily install A2SERVER on Debian, Ubuntu, or Raspbian Linux by using
the A2SERVER install scripts.

While these are the only Linux distributions the scripts have been tested on,
other Debian-derived distributions may work as well, provided they're not
based on Debian 8, don't use kernel 3.12 through 3.15, have AppleTalk
networking support available as a kernel module or compiled into the kernel
itself, and their repositories contain the packages the scripts require. The
user running the scripts needs a bash shell, sudo privileges, and a search
path containing all the "bin" and "sbin" directories.


### Debian or Ubuntu Linux

(Tested on Debian 7.8.0 and Ubuntu Server 12.04 LTS. Note that Ubuntu 14.04
LTS includes kernel 3.13, which is *not* compatible with A2SERVER; you will
need to upgrade it to 3.16 or later. Debian 8 and Ubuntu 15 *cannot* be used
at this time.)

1. [Create a new virtual machine](a2server_prepvm.md) (skip if installing on a
   real machine)
2. [Install Debian](a2server_installubuntu.md) (or Ubuntu) on the virtual or
   real machine


### Raspberry Pi

1. [Download Raspbian][1]
2. [Perform Raspberry Pi setup](a2server_raspberrypi.md)


Once you are up and running in Linux, you can execute the automated setup
scripts to download, install, and configure the A2SERVER software. To use
these, [log in to Linux](a2server_commands.md), and type:

~~~ bash
wget appleii.ivanx.com/a2server/setup; source setup
~~~

Confirm that you want to proceed, enter the password again, and go get a
sandwich, but come back so you can answer questions when prompted.

Once it's done, check out the links on the [A2SERVER home page](index.md) for
next steps.

If you'd like to set things up manually, or are curious as to what's
happening, you can
[view the contents of the setup scripts](a2server_scriptdetails.md).


[1]: http://www.raspberrypi.org/downloads
