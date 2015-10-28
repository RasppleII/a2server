## A2SERVER


The A2SERVER Odyssey

A2SERVER has been a multi-year labor of love.

Way back in 2010, my primary Apple II was a Mac Color Classic with an Apple
IIe compatibility card.

One of the things this card could do was emulate something called a
Workstation Card, which appeared to let Apple II computers access files on a
Mac file server. This was intriguing; I hadn't imagined it was possible.

And it was also potentially valuable as a way of providing mass storage for an
Apple II, with the bonus that other computers could easily access it as a
means of getting stuff to and from an otherwise isolated machine.

After some experimenting, I discovered that was exactly what it did, and I
bought an actual Workstation Card for my IIe, because that would be much, much
cooler. And it appeared that you could even *boot* the Apple II into ProDOS
from the network, which blew my mind. Using AppleShare 3.0 on another Mac as a
host, I made this happen, and there was much rejoicing.

Then, I got an idea into my head: this is great and everything, but you still
need an old Mac around. How great would it be if you could just have an
always-on network drive for an Apple II, with all the storage you might ever
need, and accessible from other computers on the LAN?

(It's true that there were Compact Flash storage cards at the time, and I
actually bought CFFA #16, but these didn't appeal to me quite as much because
of their relative lack of accessibility on other platforms. I'd need some
sort of CF extender to get the card outside the machine, then run CiderPress
in a Windows emulator...)

It so happens that I had purchased a Western Digital My Book World Edition,
which was one of the first popular NAS products available. It was basically a
small Linux computer in a drive enclosure, and it was widely hacked to make it
do all kinds of tricks, one of which was providing native file sharing for
Macs.

This was possible by installing Netatalk, an open-source implentation of AFP
(AppleShare). I immediately wondered if it would be possible to somehow get my
IIe to talk to it. So I looked into it, and it appeared that Netatalk running
on Linux still supported the older AppleTalk networking protocol required by
an Apple II, and it even supported network boot into ProDOS.

There was the issue of how to actually interface my Apple II to the network;
this turned out to be relatively easy, by using an Apple-provide control panel
for classic Macs called LocalTalk Bridge, which indeed bridged AppleTalk from
its LocalTalk port (connected to an Apple II) to its Ethernet port (connected
to my network, which was connected to the NAS). But this was clumsy, so I
invested in an AsanteTalk, which is a dedicated (if finicky)
LocalTalk-to-Ethernet bridge.

What I discovered, after some time, was that a) the version of Linux that
shipped on that NAS did not include support for AppleTalk networking, and b)
the easily-installed Netatalk package didn't include the components required
for network boot, which I absolutely wanted.

I wasn't terribly Linux-savvy at the time, but I eventually figured out that
to get network boot support, I would need to download Netatalk and compile it
myself, from source. Ok. But once I learned that adding AppleTalk support
overall would require recompiling a kernel for the drive, I kind of put the
idea aside, figuring I'd bring it to KFest and hack on it with someone there
who knows what they're doing.

In the meantime, I decided to see if I could make things work exactly as I
wanted with a "proper" Linux installation. Ubuntu Linux was well-known for
its relative ease of use, so I installed that into VMWare Fusion running on my
(modern) Mac. I installed the Netatalk package, and that worked -- though it
was still missing the network boot component, and there were other issues like
password login not working correctly.

So I had to figure out how to recompile Netatalk to make it do what I needed.
I managed to figure this out after much effort and studying of posts and
contributions to comp.sys.apple2, but wasn't able to get it to actually
netboot to ProDOS.

So this led me to comp.sys.apple2, and there met two people who turned out to
be two enormous contributors to A2SERVER: Steven Hirsch, who wrote much of the
actual network boot support in Netatalk, and Geoff Body, who knows everything
about the "boot blocks" that get transferred to the Apple IIe or IIgs during
network startup. Both Steven and Geoff have also helped figure out and work
around the idiosyncracies of many of the dedicated LocalTalk-to-Ethernet
bridges, and have been essential contributors to the execution of A2SERVER.

The initial conversation is chronicled in perpetuity here:
https://groups.google.com/forum/#!topic/comp.sys.apple2/b\_TzESci6Kg

With their help, I finally succeeded in network booting my Apple IIe from my
Linux virtual machine. The first proto-version of A2SERVER was a step-by-step
guide to manually set it up, as posted here:
https://groups.google.com/forum/#!topic/comp.sys.apple2/lkh4hXqmJbE

I could have left it at that, but I didn't like it. It wasn't all THAT easy
for a non-Linux person, network boot relied on Apple software from a "secret
archive" and hand-hacked binary code from within the guide itself, and the
final setup was hard-coded to a specific user name. I wanted a version that
was general-purpose, easy for anyone to install, and which obtained any
copyrighted software from 100% public, authorized sources.

And which, in a perfect world, could be configured to netboot from "bare
metal" -- that is, a bare computer with nothing but Linux would be able to
boot an Apple IIe or IIgs with no operating system, software, or even any
drives at all.

I hadn't forgotten about wanting it to run on a NAS, either, but I figured
I'd circle back to that, since it was so much easier working in a VM. For the
time being, what I'd ship would be both a premade VM, and a complete
installer script for actual Linux installations. And that would be A2SERVER.

Then it was a matter of locating what I could, from anyone I could, to make it
work. I discovered that the boot blocks and BASIC.SYSTEM -- the essential
pieces for netbooting ProDOS 8 -- were ensconced with the GSOS "Disk 7"
image available from Apple's Older Software downloads page. But that disk
image was a DiskDoubler self-extracting archive. Fortunately, The Unarchiver
could uncompress it, and is open-source, and builds on Linux. The disk image
was actually an HFS disk, which Linux has support for, so I was able to mount
it and copy the files out.

Steven contributed a huge fix to the Netatalk source code so ProDOS dates get
handled correctly. Geoff gave me patches to the Boot Blocks to fix a cleartext
login bug and allow an on-demand startup option to boot into ProDOS 8 on a
IIgs.

Then I had to hack a bunch of stuff together. I wrote mkatinit to create the
very specific user login files required for netboot; afpsync to simplify
Netatalk's handling of new shared files introduced from Linux; afptype to
allow setting the ProDOS (or classic Mac) file type of a file shared by
Netatalk.

These tools, plus a properly-compiled-and-configured Netatalk, made it
possible for a Linux server to entirely download ProDOS 8 and set it up for
network boot by an Apple II. Nothing had to be done on the Apple II side. Bare
metal!

I then shaped my guide into an actual executable script which could be
downloaded from my web site and executed on any Ubuntu installation. I
expanded the script to download and install the necessary tools, apply the
necessary patches, and everything else I felt was needed for click-and-go
server Apple II server setup, such as optional Windows file sharing (since one
of the goals was easy file interchange with modern computers).

And that was kinda that -- almost. I'd conquered the IIe, but the real Mt.
Everest was bare metal GS/OS netboot. This was much more challenging: it meant
I'd have to get the files out of the ProDOS-formatted GSOS installer disk
images, with resource forks intact and made usable by Netatalk. This is what I
wanted to show off when I introduced A2SERVER at KansasFest 2011.

There was no off-the-shelf solution for this, so I spent pretty much every
waking hour in Kansas City furiously creating cppo, which would copy files out
of a ProDOS disk image. And...I failed. I just ran out of time before my
presentation.

So I installed a Network Startup instalation of GS/OS the conventional way --
using the IIgs installer disks running on a IIgs, with the Netatalk shared
volume as the target. (The CFFA3000, which was also introduced that same
KansasFest, was absolutely invaluable for this.)

And it worked. In my presentation, I was able to network boot Peter
Neubauer's Apple IIe with nothing but the Workstation Card; and my IIgs with
nothing but a RAM card.

Then I came back home. I completed cppo, and it worked, mostly; with that
done, I then set about writing something to interpret the GS/OS installer
scripts and cppo the right pieces to the right places. And...it worked too.
Except that it didn't. It all started up, but the Finder had random
filenames, the Trash was full when there was nothing in it. It was corrupt.
Who knows why. I gave up.

I wasn't satisfied with not being able to start up a IIgs at all if you
didn't have the installer disks; so I made it netboot into ProDOS 8, from
where you could use DSK2FILE (which the A2SERVER installer script offers to
download) to convert the disk images to actual disks, which you could then use
to make an AppleShare startup floppy, which you could THEN use to mount the
shared volume and use it as a target for a full Network Startup install. Icky,
and of possible benefit to no one (really, who doesn't have GS/OS install
disks and a drive?), but it was some kind of solution. I packaged up the VM,
put up these web pages, and decided it was Done.

But the NAS thing itched at me. I wanted to be able to suggest an easily
obtained product. By now, WD had replaced my NAS with the My Book Live, which
featured a much faster processor, and was based on Debian Linux, which is what
Ubuntu is derived from. This was a promising starting point. I figured out how
to compile an AppleTalk kernel module for it. And then I already had these
turnkey scripts ready to go, so I hacked, and hacked, and...I couldn't get it
to work. I'd sometimes get gibberish for volume names, and network boot would
load the boot blocks, and then never stop loading, filling the Apple II's
memory with zeroes until it crashed. (My suspicion is that the big-endianness
of the PowerPC CPU in the newer NAS may have been a factor.) Fixing that would
have taken me deep into the packetized heart of Netatalk, which is beyond my
pay grade. I gave up, and decided A2SERVER was Done. Again.

Until I went to KansasFest 2012, and Eric Rucker showed me something I had
never heard of: a Raspberry Pi. Somewhere, the gears started turning, and
months later I checked it out, and saw that its primary operating system
was...a Debian derivative. Could this be my long-sought-after NAS?

It was. The install scripts ran with only a little tweaking. I did have to
compile AppleTalk in the kernel, but eventually I had what I wanted. And it
was only $35!

I revisited the corrupted GS/OS installation. I couldn't put my finger on
what was wrong. But I noticed that the Finder showed a different length on its
source disk and after copying. So I followed its index blocks, and discovered
that contained in those were 0000's. ProDOS knew to fill blocks with zeros,
but cppo was dutifully copying Block 0, the ProDOS boot block, thereby
corrupting the Finder. I fixed this, and then I HAD IT: Bare metal install
GS/OS from Linux. Yeah, man.

And, so, then it was just tweaking and refining and tweaking and refining. The
big bummer as far as general use goes was that all the common
LocalTalk-to-Ethernet bridges (Dayna, AsanteTalk, and Farallon) were partially
or completely inoperable with a IIgs, and the Workstation Card required for a
IIe is hardly in great abundance. But Geoff Body came up with a fix for the
Farallon, I came up with a workaround for the AsanteTalk, and Steven Hirsch
came up with an actual fix for both the AsanteTalk and the Dayna, meaning
*all* of those bridges are now options for a IIgs owner!

So this was it: bare IIgs (even without memory card, if you're OK with ProDOS
8) + Raspberry Pi + readily available bridge = Apple II file server. Yeah!

And I discovered that with a USB cable or RPi console cable, you could
actually log in and control it with ProTERM. With Hugh Hood's clever ProTERM
patch for 115,200 bps on a IIgs, I could actually see my Raspberry Pi start
up...on my Apple II. I can't explain how joyous this made me.

And, I wrote ProDOS 8 utilities to switch the IIgs boot mode, which is
normally only possible under GS/OS.

I could go on and on, but basically the ideas kept coming, and I think I was
able I was able to polish most of A2SERVER's rough edges so that it could be
fun and/or useful for a few people. I hope you enjoy it!
