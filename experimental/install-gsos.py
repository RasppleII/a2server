#! /usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab filetype=python:

import os, sys, subprocess
import tempfile
import hashlib
import shutil
import xml.etree.cElementTree as ET

gsosDir = "/media/A2SHARED/FILES"
imagesDir = gsosDir + "/GSOS.INSTALLER/IMAGES"
imageToolsDir = gsosDir + "/GSOS.INSTALLER/IMAGE.TOOLS"
netInstallDir = gsosDir + "/GSOS.INSTALLER/NET.INSTALL"

p8Dir = "/media/A2SHARED/A2FILES"
diskToolsP8Dir = p8Dir + "/DISK.TOOLS.P8"

commDir = "/media/A2SHARED/A2FILES/COMM"
spectrumDir = commDir + "/SPECTRUM"
protermDir = commDir + "/PROTERM"
zlinkDir = commDir + "/Z.LINK"
adtproDir = commDir + "/ADTPRO"

quiet = False
verbose = False

disk7_sources = [
    {
        "src"   : "Apple",
        "type"  : "sea.bin",
        "url"   : "http://download.info.apple.com/Apple_Support_Area/Apple_Software_Updates/English-North_American/Apple_II/Apple_IIGS_System_6.0.1/Disk_7_of_7-Apple_II_Setup.sea.bin",
        "file"  : "Disk_7_of_7-Apple_II_Setup.sea.bin"
    },
    {
        "src"   : "archive.org",
        "type"  : "sea.bin",
        "url"   : "http://archive.org/download/download.info.apple.com.2012.11/download.info.apple.com.2012.11.zip/download.info.apple.com%2FApple_Support_Area%2FApple_Software_Updates%2FEnglish-North_American%2FApple_II%2FApple_IIGS_System_6.0.1%2FDisk_7_of_7-Apple_II_Setup.sea.bin",
        "file"  : "Disk_7_of_7-Apple_II_Setup.sea.bin"
    }
]

a2boot_files = [
    {
        "unix"     : "Apple ::e Boot Blocks",
        "hfsutils" : "Apple_--e_Boot_Blocks.bin",
        "netatalk" : "Apple :2f:2fe Boot Blocks",
        "digest"   : "cada362ac2eca3ffa506e9b4e76650ba031e0035",
        "patches"  : {
            "6.0.1" : (
                [
                    "Cleartext password login bug",
                    (0x4d43, "\xA8\xA2\x01\xBD\x80\x38\x99\xA0\x38\xC8\xE8\xE0\x09\x90\xF4")
                ],
                "6b7fc12fd118e1cb9e39c7a2b8cc870c844a3bac"
            )
        }
    },
    {
        "unix"     : "Basic.System",
        "hfsutils" : "Basic.System.bin",
        "netatalk" : "Basic.System",
        "digest"   : "4d53424f1451cd2e874cf792dbdc8cc6735dcd36"
    },
    {
        "unix"     : "ProDOS16 Boot Blocks",
        "hfsutils" : "ProDOS16_Boot_Blocks.bin",
        "netatalk" : "ProDOS16 Boot Blocks",
        "digest"   : "fab829e82e6662ed6aab119ad18e16ded7d43cda",
    },
    {
        "unix"     : "ProDOS16 Image",
        "hfsutils" : "ProDOS16_Image.bin",
        "netatalk" : "ProDOS16 Image",
        "digest"   : "db4608067b9e7877f45eb557971c4d8c45b46be5",
        "patches"  : {
            "6.0.1" : (
                [
                    "Cleartext password login bug",
                    (0x5837, "\xA8\xA2\x01\xBD\x80\x38\x99\xA0\x38\xC8\xE8\xE0\x09\x90\xF4"),

                    "Enable pressing \"8\" during GS/OS netboot to load ProDOS 8",
                    (0x0100, "\x92"),
                    (0x0360, "\x20\x7d\x14"),
                    (0x067d, "\xad\x00\xc0\x29\xff\x00\xc9\xb8\x00\xd0\x06\xa9\x02\x00\x8d\x53\x14\xa9\x10\x0f\x60")
                ],
                "5c35d5533901b292ab7c2f5a3c76cb3113f66085"
            )
        }
    },
    {
        "unix"     : "p8",
        "hfsutils" : "p8.bin",
        "netatalk" : "p8",
        "digest"   : "36c288a5272cf01e0a64eed16786258959118e0e"
    }
]

# True for Python 3.0 and later
PY3 = sys.version_info >= (3, 0)

if PY3:
    stdin_input = input
    import urllib.request as urlrequest
else:
    stdin_input = raw_input
    import urllib2 as urlrequest


# Differing from the shell script in that we explicitly strip the / here
if "A2SERVER_SCRIPT_URL" in os.environ:
    scriptURL = os.environ["A2SERVER_SCRIPT_URL"]
    # Strip trailing slash
    if scriptURL.endswith("/"):
        scriptURL = scriptURL[:-1]
else:
    scriptURL = "http://appleii.ivanx.com/a2server"

def sha1file (filename, blocksize=65536):
    f = open(filename, "rb")
    digest = hashlib.sha1()
    buf = f.read(blocksize)
    while len(buf) > 0:
        digest.update(buf)
        buf = f.read(blocksize)
    f.close()
    if verbose:
        print("SHA-1: %s  %s" % (digest.hexdigest(), filename))
    return digest.hexdigest()

def download_url(url, filename, output_dir = None):
    try:
        if output_dir != None:
            dest = os.path.join(output_dir, filename)
        else:
            dest = filename

        if verbose:
            print("""   URL  : %s
   Dest : %s""" % (url, dest))

        html = urlrequest.urlopen(url)
        data = html.read()
        f = open(dest, "wb")
        f.write(data)
        f.close
        if verbose:
            print("File downloaded.\n")
        return True

    except:
        if verbose:
            print("Download failed.")
        return False

# Apple's GS/OS 6.0.1 images are stored in MacBinary-wrapped
# self-extracting disk image files.  The Unarchiver's unar is able
# to unwrap the MacBinary wrapper for us, but we have to extract the
# disk image oursselves.  Fortunately, it's uncompressed.
def extract_800k_sea_bin(archive_name, image_name, archive_dir):
    if not quiet:
        print("Extracting %s from %s..." % (image_name, archive_name))

    if archive_dir != None:
        archive_path = os.path.join(archive_dir, archive_name)
        image_path = os.path.join(archive_dir, image_name)
    else:
        archive_path = archive_name
        impage_path = image_name

    if not os.path.isfile(archive_path):
        raise IOError("Archive file \"" + archive_path + "\" does not exist")

    # Extract the original filename from the file
    # MacBinary II header is 128 bytes.  The first byte is NUL, followed by a
    # Pascal string of length 63 (so 64 bytes total) containing the encoded
    # filename.
    #
    # Source: http://files.stairways.com/other/macbinaryii-standard-info.txt
    # FIXME: We should eventually implement a full MacBinary reader.

    f = open(archive_path, "rb")
    sea_name = f.read(65)
    f.close()
    if PY3:
        sea_name = sea_name[2:2 + sea_name[1]].decode("mac_roman")
    else:
        sea_name = sea_name[2:2 + ord(sea_name[1])]

    if verbose:
        print("Running unar on \"%s\" to extract %s..." % (archive_name, sea_name))

    cmdline = ["unar", "-q", "-o", archive_dir, "-k", "skip", archive_path]
    ret = subprocess.call(cmdline)
    if ret != 0:
        raise IOError("unar returned with status %i" % (ret))
    # Do we have the right file?
    sea_path = os.path.join(archive_dir, sea_name)
    if not os.path.isfile(sea_path):
        raise IOError("Expected image archive \"" + sea_name + "\" does not exist")

    if verbose:
        print("Extracting disk image from %s..." % (sea_name))

    # Cowardly refuse to overwrite image_path
    if os.path.exists(image_path):
        raise IOError("\"" + image_path + "\" already exists")

    # The image starts 84 bytes in, and is exactly 819200 bytes long
    with open(sea_path, "rb") as src, open(image_path, "wb") as dst:
        src.seek(84)
        dst.write(src.read(819200))
        if dst.tell() != 819200:
            raise IOError(archive_name + " did not contain an 800k floppy image")

    # Now just clean up the archive files and we're done
    os.unlink(sea_path)
    os.unlink(archive_path)

    if verbose:
        print("%s extracted." % (image_name))


def plist_keyvalue(plist_dict, key):
    if plist_dict.tag != "dict":
        raise ValueError("not a plist dict")
    found = False
    for elem in plist_dict:
        if found:
            return elem
        if elem.tag == "key" and elem.text == key:
            found = True
    return None

def find_mountpoint(xmlstr):
    plistroot = ET.fromstring(xmlstr)
    if plistroot.tag != "plist":
        raise ValueError("xmlstr is not an XML-format plist")
    if plistroot[0].tag == "dict":
        sys_entities = plist_keyvalue(plistroot[0], "system-entities")
        if sys_entities.tag != "array":
            raise ValueError("expected dict to contain an array")
        for child in sys_entities:
            if child.tag == "dict":
                mountpoint = plist_keyvalue(child, "mount-point")
                return mountpoint.text
            else:
                raise ValueError("system-entities should be an array of dict objects")
    else:
        raise ValueError("Root element is not a dict")


def install_bootblocks(dest_dir, dest_fmt, gsos_version):
    if dest_fmt not in ["unix", "netatalk"]:
        raise ValueError("Only basic UNIX and netatalk formats are supported for now")

    if not quiet:
        print("Installing Apple // boot blocks (GS/OS version %s)..." % (gsos_version))

    devnull = open(os.devnull, "wb")
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir, mode=0o0755)

    work_dir = tempfile.mkdtemp(prefix = "tmp-a2sv-bootblocks.")
    a2setup_name = "A2SETUP.img"
    if verbose:
        print("   dest_fmt : %s\n   dest_dir : %s\n   work_dir : %s\n"
                % (dest_fmt, dest_dir, work_dir))

    platform = os.uname()[0]
    if platform not in ["Linux", "Darwin"]:
        platform = "hfsutils"
    elif platform == "Linux":
        use_sudo = False
        if os.geteuid() != 0:
            reply = stdin_input("""
You must have either root access or the hfsutils package to
access the disk image containing Apple // boot blocks.  Do
you want to mount the image using the sudo command? [y] """)
            if reply.startswith("y") or reply.startswith("Y") or reply == "":
                use_sudo = True
                print("""
Okay, if asked for a password, type your user password.  It
will not be echoed when you type.""")
            else:
                platform = "hfsutils"

    unpacked_a2boot = False
    for bootfile in a2boot_files:
        if dest_fmt == "unix":
            dst_name = bootfile["unix"]
        elif dest_fmt == "netatalk":
            if "netatalk" in bootfile:
                dst_name = bootfile["netatalk"]
            else:
                dst_name = bootfile["unix"]
        dst_path = os.path.join(dest_dir, dst_name)

        if not os.path.isfile(dst_path):
            # We need to fetch it
            if not unpacked_a2boot:
                a2setup_path = os.path.join(work_dir, a2setup_name)
                disk7_downloaded = False
                for disk7_source in disk7_sources:
                    if not quiet:
                        print("Downloading %s from %s..." 
                                % (disk7_source["file"], disk7_source["src"]))

                    if download_url(disk7_source["url"], disk7_source["file"], work_dir):
                        disk7_downloaded = True
                    else:
                        continue

                    if disk7_source["type"] == "sea.bin":
                        extract_800k_sea_bin(disk7_source["file"], a2setup_name, work_dir)
                    else:
                        # Placeholder for 6.0.4+ files packed some other way
                        pass
                    break

                if not disk7_downloaded:
                    raise IOError("Could not download disk7")

                if platform == "Linux":
                    mountpoint = os.path.join(work_dir, "a2boot")
                    os.mkdir(mountpoint)
                    mount_cmd = ["mount", "-t", "hfs", "-o", "ro,loop", a2setup_path, mountpoint]
                    if use_sudo:
                        mount_cmd = ["sudo"] + mount_cmd
                    subprocess.call(mount_cmd)
                    src_dir = os.path.join(mountpoint, "System Folder")
                elif platform == "Darwin":
                    xmlstr = subprocess.check_output(["hdiutil", "attach", "-plist",
                            a2setup_path])
                    mountpoint = find_mountpoint(xmlstr)
                    src_dir = os.path.join(mountpoint, "System Folder")
                elif platform == "hfsutils":
                    src_dir = os.path.join(work_dir, "a2boot")
                    os.mkdir(src_dir)
                    subprocess.call(["hmount", a2setup_path], stdout=devnull)
                    subprocess.call(["hcopy", "Apple II Setup:System Folder:*",
                            src_dir], stdout=devnull)
                    subprocess.call(["humount", "Apple II Setup"], stdout=devnull)

                unpacked_a2boot = True

            # Copy the file
            if platform == "Linux" or platform == "Darwin":
                src_path = os.path.join(src_dir, bootfile["unix"])
            elif platform == "hfsutils":
                src_path = os.path.join(src_dir, bootfile["hfsutils"])
            shutil.copyfile(src_path, dst_path)
        else:
            if verbose:
                print("\"%s\" already exists." % (dst_name))

    # Clean up the mounted/unpacked image
    if unpacked_a2boot:
        if platform == "Linux":
            umount_cmd = ["umount", mountpoint]
            if use_sudo:
                umount_cmd = ["sudo"] + umount_cmd
            subprocess.call(umount_cmd)
            os.rmdir(mountpoint)
        elif platform == "Darwin":
            subprocess.call(["hdiutil", "eject", mountpoint], stdout=devnull)
        elif platform == "hfsutils":
            for bootfile in a2boot_files:
                name = os.path.join(src_dir, bootfile["hfsutils"])
                if os.path.isfile(name):
                    os.unlink(name)
            os.rmdir(src_dir)
        os.unlink(a2setup_path)

    devnull.close()
    os.rmdir(work_dir)

def do_install():
    netboot_tmp = tempfile.mkdtemp(suffix = ".a2server-netboot")
    print("You'll want to go and delete this directory:")
    print(netboot_tmp)
    os.chdir(netboot_tmp)

    #   If we need boot files:
    #       Download a disk image
    #       If it is one we need to unpack (.sea.bin):
    #           unar it
    #           extract the embedded image
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
    autoAnswerYes = os.path.isfile("/tmp/a2server-autoAnswerYes")
    if autoAnswerYes and not os.path.isfile("/tmp/a2server-setupNetBoot"):
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
        args.insert(0, "sudo")
        # At the very least, we should print the command line we"re running here
        print ("Rerunning with sudo...")
        ret = subprocess.call(args)
        sys.exit(ret)
    """

    install_bootblocks(os.path.join(os.getcwd(), "a2boot"), "netatalk", "6.0.1")
    #reply = stdin_input("""\nDo you want to set up A2SERVER to be able to boot Apple II\ncomputers over the network? [y] """)
    #if reply.startswith("y") or reply.startswith("Y") or reply == "":
    #    do_install()
