#! /usr/bin/env python

import os, sys, subprocess
import tempfile

gsosDir = '/media/A2SHARED/FILES'
imagesDir = gsosDir + '/GSOS.INSTALLER/IMAGES'
imageToolsDir = gsosDir + '/GSOS.INSTALLER/IMAGE.TOOLS'
netInstallDir = gsosDir + '/GSOS.INSTALLER/NET.INSTALL'

p8Dir = '/media/A2SHARED/A2FILES'
diskToolsP8Dir = p8Dir + '/DISK.TOOLS.P8'

commDir = '/media/A2SHARED/A2FILES/COMM'
spectrumDir = commDir + '/SPECTRUM'
protermDir = commDir + '/PROTERM'
zlinkDir = commDir + '/Z.LINK'
adtproDir = commDir + '/ADTPRO'

disk7_filename = 'Disk_7_of_7-Apple_II_Setup.sea.bin'
disk7_url = 'http://archive.org/download/download.info.apple.com.2012.11/download.info.apple.com.2012.11.zip/download.info.apple.com%2FApple_Support_Area%2FApple_Software_Updates%2FEnglish-North_American%2FApple_II%2FApple_IIGS_System_6.0.1%2F' + disk7_filename

try:
    stdin_input = raw_input     # Python 2
except NameError:
    stdin_input = input         # Python 3

try:
    import urllib.request as urlrequest     # Python 3
except ImportError:
    import urllib2 as urlrequest            # Python 2


# Differing from the shell script in that we explicitly strip the / here
if 'A2SERVER_SCRIPT_URL' in os.environ:
    scriptURL = os.environ['A2SERVER_SCRIPT_URL']
    # Strip trailing slash
    if scriptURL.endsWith('/'):
        scriptURL = scriptURL[:-1]
else:
    scriptURL = 'http://appleii.ivanx.com/a2server'

def download_url(url, filename):
    html = urlrequest.urlopen(url)
    data = html.read()
    f = open(filename, 'wb')
    f.write(data)
    f.close

# Apple's GS/OS 6.0.1 images are stored in MacBinary-wrapped
# self-extracting disk image files.  The Unarchiver's unar is able
# to unwrap the MacBinary wrapper for us, but we have to extract the
# disk image oursselves.  Fortunately, it's uncompressed.
def extract_800k_sea_bin(wrapper_name, image_name, sea_name = None):
    # First we need to get rid of the MacBinary wrapper
    # FIXME: Can we learn to read MacBinary?  I bet we can!
    cmdline = ['unar', '-q', '-k', 'skip', wrapper_name]
    ret = subprocess.call(cmdline)
    if ret != 0:
        raise IOError('unar returned with status ' + ret)

    # MAYBE we can guess the name?
    if sea_name == None:
        if wrapper_name.endswith('.bin'):
            sea_name = wrapper_name[:-4]
        else:
            raise ValueError('sea_name is None, but "' + wrapper_name +
                    '" doesn\'t end with .sea.bin')

    # Do we have the right file?
    if not os.path.isfile(sea_name):
        raise IOError('Expected image archive "' + sea_name + '" does not exist')

    # The image starts 84 bytes in, and is exactly 819200 bytes long
    with open(sea_name, 'rb') as src, open(image_name, 'wb') as dst:
        src.seek(84)
        dst.write(src.read(819200))
        if dst.tell() != 819200:
            raise IOError(wrapper_name + ' did not contain an 800k floppy image')

    # Now just clean up the archive files and we're done
    os.unlink(sea_name)
    os.unlink(wrapper_name)

def install_bootblocks(dir):
    pass

def do_install():
    netboot_tmp = tempfile.mkdtemp(suffix = '.a2server-netboot')
    print('You\'ll want to go and delete this directory:')
    print(netboot_tmp)
    os.chdir(netboot_tmp)

    #   If we need boot files:
    #       Download a disk image
    #       If it is one we need to unpack (.sea.bin):
    #           unar it
    #           extract the embedded image

    # You commonly see GS/OS 6.0.1 as six floppies for the Apple IIgs, but
    # there's actually a seventh HFS-formatted floppy containing AFP network
    # boot files the Apple //e and IIgs.  We need those.

    disk7_file = os.path.join(netboot_tmp, disk7_filename)
    download_url(disk7_url, disk7_file)

    # If file is wrapped as .sea.bin (always true for now)
    if True:
        sea_name = 'Disk 7 of 7-Apple II Setup.sea'
        a2setup_hdv_name = 'A2SETUP.HDV'
        extract_800k_sea_bin(disk7_filename, a2setup_hdv_name, sea_name)

    #       If we need to apply boot block patches:
    #           fix cleartext password bug in //e boot block
    #           fix cleartext password bug in IIgs boot block
    #           patch IIgs boot block to allow booting ProDOS 8
    #   If we don't have A2SERVER tools:
    #       Download the installer script
    #       Run the installer script
    #   Copy Basic.System to A2FILES for ProDOS 8
    #   If NETBOOT.P8 (battery ram set to boot into ProDOS 8) doesn't exist:
    #       Create it
    #   If NETBOOT.GSOS (battery ram set to boot into GSOS) doesn't exist:
    #       Create it
    #   Set GS/OS to boot SYSTEM/FINDER (registered user or guest)
    #   Set ProDOS 8 to boot BASIC.SYSTEM (guest)
    #   If SYSTEM/START.GS.OS doesn't exist in A2FILES:
    #       Ask if user wants to install GS/OS 6.0.1
    #       If they answer yes:
    #           create imagesDir
    #           create netInstallDir
    #           For each disk:
    #               Download the disk
    #               If it is one we need to unpack (.sea.bin):
    #                   extract_800k_sea_bin it
    #               unpack the disk to netInstallDir


    # XXX Re-enable this
    #os.rmdir(netboot_tmp)

if __name__ == '__main__':
    # bail out on automated netboot setup unless -b is also specified
    # FIXME: This logic belongs in a2server-setup, not here
    autoAnswerYes = os.path.isfile('/tmp/a2server-autoAnswerYes')
    if autoAnswerYes and not os.path.isfile('/tmp/a2server-setupNetBoot'):
        sys.exit(0)

    # We need root to do this.  If we don't have it, just rerun the command with
    # sudo and be done with it.
    #
    # FIXME: Should we be doing this?  A generic installer should not assume it's
    # writing to a root-owned dir, nor care.  Probably the reason to do it this way
    # is as a proof of concept that it can be done this way in the main
    # a2server-setup script, which of course means we don't actually need to change
    # the password for the user.
    #
    # XXX Disabling this for development
    """
    if os.geteuid() != 0:
        args = sys.argv
        args.insert(0, 'sudo')
        # At the very least, we should print the command line we're running here
        print ('Rerunning with sudo...')
        ret = subprocess.call(args)
        sys.exit(ret)
    """

    reply = stdin_input("""
Do you want to set up A2SERVER to be able to boot Apple II
computers over the network? [y] """)
    if reply.startswith('y') or reply.startswith('Y') or reply == '':
        do_install()
