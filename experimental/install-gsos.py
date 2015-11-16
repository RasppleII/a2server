#! /usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab filetype=python:

from __future__ import print_function


import os, sys, subprocess
import tempfile
import hashlib
import shutil
import xml.etree.cElementTree as ET

quiet = False
verbose = True

disk7_sources = {
    "file"    : "Disk_7_of_7-Apple_II_Setup.sea.bin",
    "digest"  : "43fbc296ab66da84aadc275b80fd51ec4f7fe986",
    "type"    : "sea.bin",
    "sources" : [
        ( "Apple", "http://download.info.apple.com/Apple_Support_Area/Apple_Software_Updates/English-North_American/Apple_II/Apple_IIGS_System_6.0.1/Disk_7_of_7-Apple_II_Setup.sea.bin" ),
        ( "archive.org", "http://archive.org/download/download.info.apple.com.2012.11/download.info.apple.com.2012.11.zip/download.info.apple.com%2FApple_Support_Area%2FApple_Software_Updates%2FEnglish-North_American%2FApple_II%2FApple_IIGS_System_6.0.1%2FDisk_7_of_7-Apple_II_Setup.sea.bin" )
    ]
}

a2boot_files = [
    {
        "unix"     : "Apple ::e Boot Blocks",
        "hfsutils" : "Apple_--e_Boot_Blocks.bin",
        "netatalk" : "Apple :2f:2fe Boot Blocks",
        "digest"   : "cada362ac2eca3ffa506e9b4e76650ba031e0035",
        "patches"  : (
            [
                "Cleartext password login bug",
                (0x4d43, b"\xA8\xA2\x01\xBD\x80\x38\x99\xA0\x38\xC8\xE8\xE0\x09\x90\xF4"),

                "ProDOS 8 patch: year table, splash date (6.0.3)",
                (0x004f, b"\xb0\xb2\xad\xc1\xf5\xe7\xad\xb1\xb5"),
                (0x1b9f, b"\x12\x11\x0b\x10\x0f\x0e\x0d"),
            ],
            "8cff6ef453533423b34b5b4fefd642441e2ee374",
        ),
    },
    {
        "unix"     : "Basic.System",
        "hfsutils" : "Basic.System.bin",
        "netatalk" : "Basic.System",
        "digest"   : "4d53424f1451cd2e874cf792dbdc8cc6735dcd36",
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
        "patches"  : (
            [
                "Cleartext password login bug",
                (0x5837, b"\xA8\xA2\x01\xBD\x80\x10\x99\xA0\x10\xC8\xE8\xE0\x09\x90\xF4"),

                "Enable pressing \"8\" during GS/OS netboot to load ProDOS 8",
                (0x0100, b"\x92"),
                (0x0360, b"\x20\x7d\x14"),
                (0x067d, b"\xad\x00\xc0\x29\xff\x00\xc9\xb8\x00\xd0\x06\xa9\x02\x00\x8d\x53\x14\xa9\x10\x0f\x60"),

                "ProDOS 8 patch: year table, splash date (6.0.3)",
                (0x0c26, b"\xb0\xb2\xad\xc1\xf5\xe7\xad\xb1\xb5"),
                (0x1b76, b"\x12\x11\x0b\x10\x0f\x0e\x0d"),
            ],
            "1f0477030b7e9c809b0a2282896ca66033e7ca9f",
        ),
    },
    {
        "unix"     : "p8",
        "hfsutils" : "p8.bin",
        "netatalk" : "p8",
        # 36c288a5272cf01e0a64eed16786258959118e0e  P8 (02-Apr-93, a2setup)
        # c99f69c8dbfe79f02c715162fb409aedf52d378a  P8 (06-May-93, 6.0.1)
        # Only splash date differs.
        "digest"   : "36c288a5272cf01e0a64eed16786258959118e0e",
        "patches"  : (
            [
                # May as well patch the splash as well.  *shrug*
                "ProDOS 8 patch: year table, splash date (6.0.3)",
                (0x0026, b"\xb0\xb2\xad\xc1\xf5\xe7\xad\xb1\xb5"),
                (0x0f76, b"\x12\x11\x0b\x10\x0f\x0e\x0d"),
            ],
            "ad1e6c8f653df428d13cb8ae5ce4f8425a52016b",
        ),
    },
]

# True for Python 3.0 and later
PY3 = sys.version_info >= (3, 0)

if PY3:
    stdin_input = input
    import urllib.request as urlrequest
else:
    stdin_input = raw_input
    import urllib2 as urlrequest


def sha1sum_file (filename, blocksize=65536):
    f = open(filename, "rb")
    digest = hashlib.sha1()
    buf = f.read(blocksize)
    while len(buf) > 0:
        digest.update(buf)
        buf = f.read(blocksize)
    f.close()
    return digest.hexdigest()


def download_from_sources(fileinfo, output_dir):
    output_path = os.path.join(output_dir, fileinfo["file"])
    if not quiet:
        print("Downloading %s" % (fileinfo["file"]))
    for (source, url) in fileinfo["sources"]:
        if not quiet:
            print("   From %s..." % (source), end="")

        try:
            html = urlrequest.urlopen(url)
            data = html.read()
            f = open(output_path, "wb")
            f.write(data)
            f.close()
        except:
            if not quiet:
                print("  download failed.")
            if 'f' in locals():
                if not f.isclosed():
                    f.close()
            continue

        digest = sha1sum_file(output_path)
        if digest == fileinfo["digest"]:
            if not quiet:
                print("  successfully downloaded.")
            return True
        else:
            if not quiet:
                print("  failed (digest mismatch).")
            if verbose:
                print("      Expected: %s\n      Received: %s"
                        % (fileinfo["digest"], digest))

    return False


# Apple's GS/OS 6.0.1 images are stored in MacBinary-wrapped
# self-extracting disk image files.  The Unarchiver's unar is able
# to unwrap the MacBinary wrapper for us, but we have to extract the
# disk image oursselves.  Fortunately, it's uncompressed.
def extract_800k_sea_bin(archive_name, image_name, archive_dir):
    if not quiet:
        print("Extracting %s..." % (archive_name), end="")

    archive_path = os.path.join(archive_dir, archive_name)
    image_path = os.path.join(archive_dir, image_name)

    if not os.path.isfile(archive_path):
        if not quiet:
            print("  not found.")
            return False

    # Extract the original filename from the file
    # MacBinary II header is 128 bytes.  The first byte is NUL, followed by a
    # Pascal string of length 63 (so 64 bytes total) containing the encoded
    # filename.
    #
    # Source: http://files.stairways.com/other/macbinaryii-standard-info.txt
    # FIXME: We should eventually implement a full MacBinary reader.

    try:
        f = open(archive_path, "rb")
        sea_name = f.read(65)
        f.close()

        if len(sea_name) < 65:
            if not quiet:
                print("  file too short.")
            return False

        if PY3:
            sea_name = sea_name[2:2 + sea_name[1]].decode("mac_roman")
        else:
            sea_name = sea_name[2:2 + ord(sea_name[1])]
    except:
        if not quiet:
            print("  error: cannot read expanded name")
        if 'f' in locals():
            if not f.isclosed():
                f.close()
        return False

    try:
        cmdline = ["unar", "-q", "-o", archive_dir, "-k", "skip", archive_path]
        ret = subprocess.call(cmdline)
        if ret != 0:
            if not quiet:
                print("  error: unar returned error %i" % (ret))
            return False
    except OSError as e:
        if not quiet:
            print("  error: running unar: %s" % (e))
        return False

    sea_path = os.path.join(archive_dir, sea_name)
    if not os.path.isfile(sea_path):
        if not quiet:
            print("  error: \"%s\" was not extracted." % (sea_name))
        return False

    try:
        # The image starts 84 bytes in, and is exactly 819200 bytes long
        with open(sea_path, "rb") as src, open(image_path, "wb") as dst:
            src.seek(84)
            dst.write(src.read(819200))
            if dst.tell() != 819200:
                raise IOError()
            extracted = True
    except:
        if not quiet:
            print("  error: \"%s\" is not an 800k floppy image"
                    % (sea_name))
        extracted = False
    finally:
        if not quiet:
            print("  done.")
        os.unlink(sea_path)
        os.unlink(archive_path)

    return extracted


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

a2setup_platform = None

def a2setup_set_platform():
    global a2setup_platform
    
    a2setup_platform = os.uname()[0]
    if a2setup_platform not in ["Linux", "Darwin"]:
        a2setup_platform = "hfsutils"
    elif a2setup_platform == "Linux":
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
                a2setup_platform = "hfsutils"


def a2setup_mount(image_path):
    mountpoint = None
    if a2setup_platform == "Linux":
        mountpoint = tempfile.mkdtemp(prefix = "tmp-hfsmount.")
        mount_cmd = ["mount", "-t", "hfs", "-o", "ro,loop", image_path, mountpoint]
        if use_sudo:
            mount_cmd = ["sudo"] + mount_cmd
        subprocess.call(mount_cmd)
    elif a2setup_platform == "Darwin":
        xmlstr = subprocess.check_output(["hdiutil", "attach", "-plist",
                image_path])
        mountpoint = find_mountpoint(xmlstr)
    elif a2setup_platform == "hfsutils":
        mountpoint = tempfile.mkdtemp(prefix = "tmp-hfsmount.")
        sys_folder = os.path.join(mountpoint, "System Folder")
        os.mkdir(sys_folder)
        devnull = open(os.devnull, "wb")
        subprocess.call(["hmount", image_path], stdout=devnull)
        devnull.close()
        subprocess.call(["hcopy", "Apple II Setup:System Folder:*", sys_folder])
        subprocess.call(["humount", "Apple II Setup"])

    return mountpoint


def a2setup_copyfile(bootfile, mountpoint, dest_dir, dest_fmt):
    src_dir = os.path.join(mountpoint, "System Folder")
    if a2setup_platform == "Linux" or a2setup_platform == "Darwin":
        src_path = os.path.join(src_dir, bootfile["unix"])
    elif a2setup_platform == "hfsutils":
        src_path = os.path.join(src_dir, bootfile["hfsutils"])
    dest_path = os.path.join(dest_dir, bootfile[dest_fmt])
    try:
        shutil.copyfile(src_path, dest_path)
    except:
        return False

    return True


def a2setup_umount(mountpoint):
    if a2setup_platform == "Linux":
        umount_cmd = ["umount", mountpoint]
        if use_sudo:
            umount_cmd = ["sudo"] + umount_cmd
        subprocess.call(umount_cmd)
        os.rmdir(mountpoint)
    elif a2setup_platform == "Darwin":
        devnull = open(os.devnull, "wb")
        subprocess.call(["hdiutil", "eject", mountpoint], stdout=devnull)
        devnull.close()
    elif a2setup_platform == "hfsutils":
        sys_folder = os.path.join(mountpoint, "System Folder")
        for f in os.listdir(sys_folder):
            os.unlink(os.path.join(sys_folder, f))
        os.rmdir(sys_folder)
        os.rmdir(mountpoint)


def apply_patches(bootfile, dest_dir, dest_fmt):
    if "patches" in bootfile:
        (patches, digest) = bootfile["patches"]
        patch_path = os.path.join(dest_dir, bootfile[dest_fmt])
        dest_digest = sha1sum_file(patch_path)
        if dest_digest == digest:
            if not quiet:
                print("  \"%s\" is already patched." % (bootfile[dest_fmt]))
                return True
        else:
            if verbose:
                print("  Patching %s..." % (bootfile[dest_fmt]))
            elif not quiet:
                print("  Patching %s..." % (bootfile[dest_fmt]), end="")
            f = open(patch_path, "r+b")
            for patch in patches:
                if isinstance(patch, str):
                    if verbose:
                        print("    %s" % (patch))
                else:
                    (offset, data) = patch
                    f.seek(offset)
                    f.write(data)
            f.close()

            # Verify...
            dest_digest = sha1sum_file(patch_path)
            if dest_digest == digest:
                print("  patched.")
            else:
                print("  patch failed.\n      Expected: %s\n      Received: %s"
                        % (bootfile["patches"][1], dest_digest))
                return False

    return True


def install_bootblocks(dest_dir, dest_fmt):
    if dest_fmt not in ["unix", "netatalk"]:
        raise ValueError("Only basic UNIX and netatalk formats are supported for now")

    if not quiet:
        print("Installing Apple // boot blocks...")

    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir, mode=0o0755)

    work_dir = tempfile.mkdtemp(prefix = "tmp-a2sv-bootblocks.")
    a2setup_name = "A2SETUP.img"
    if verbose:
        print("   dest_fmt : %s\n   dest_dir : %s\n   work_dir : %s\n"
                % (dest_fmt, dest_dir, work_dir))

    a2setup_set_platform()

    a2boot_needed = False
    a2setup_extracted = False
    a2boot_installed = False

    for bootfile in a2boot_files:
        dest_path = os.path.join(dest_dir, bootfile[dest_fmt])
        if not os.path.isfile(dest_path):
            a2boot_needed = True
            break
        else:
            dest_digest = sha1sum_file(dest_path)
            if dest_digest != bootfile["digest"]:
                if "patches" not in bootfile or dest_digest != bootfile["patches"][1]:
                    a2boot_needed = True
                    break

    if not a2boot_needed:
        if not quiet:
            print("Files already copied.")
        a2boot_installed = True
    else:
        if download_from_sources(disk7_sources, work_dir):
            if disk7_sources["type"] == "sea.bin":
                a2setup_extracted = extract_800k_sea_bin(disk7_sources["file"],
                        a2setup_name, work_dir)
            else:
                # Placeholder for 6.0.4+ files packed some other way
                pass

            if a2setup_extracted:
                a2setup_path = os.path.join(work_dir, a2setup_name)
                mountpoint = a2setup_mount(a2setup_path)
                src_dir = os.path.join(mountpoint, "System Folder")

                if not quiet:
                    print("Copying files...", end="")
                a2boot_installed = True
                for bootfile in a2boot_files:
                    if not a2setup_copyfile(bootfile, mountpoint, dest_dir, dest_fmt):
                        a2boot_installed = False

                if not quiet:
                    if a2boot_installed:
                        print("  success.")
                    else:
                        print("  error copying files")

                a2setup_umount(mountpoint)
                os.unlink(a2setup_path)

    os.rmdir(work_dir)

    if not a2boot_installed and not quiet:
        print("Installation failed.")
        return False

    for bootfile in a2boot_files:
        apply_patches(bootfile, dest_dir, dest_fmt)

    return True


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

    install_bootblocks(os.path.join(os.getcwd(), "a2boot"), "netatalk")
    #reply = stdin_input("""\nDo you want to set up A2SERVER to be able to boot Apple II\ncomputers over the network? [y] """)
    #if reply.startswith("y") or reply.startswith("Y") or reply == "":
    #    do_install()
