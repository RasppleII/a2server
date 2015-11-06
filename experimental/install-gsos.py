#! /usr/bin/env python

import os, sys, subprocess

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

# Python 3.x replaced (useless) input() with raw_input()
try:
    stdin_input = raw_input
except NameError:
    stdin_input = input

# Differing from the shell script in that we explicitly strip the / here
if os.environ.has_key('A2SERVER_SCRIPT_URL'):
    scriptURL = os.environ['A2SERVER_SCRIPT_URL']
    # Strip trailing slash
    if scriptURL.endsWith('/'):
        scriptURL = scriptURL[:-1]
else:
    scriptURL = "http://appleii.ivanx.com/a2server"

def do_install():
    pass

if __name__ == "__main__":
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
    if os.geteuid() != 0:
        args = sys.argv
        args.insert(0, 'sudo')
        # At the very least, we should print the command line we're running here
        print ("Rerunning with sudo...")
        ret = subprocess.call(args)
        sys.exit(ret)

    reply = stdin_input("""
Do you want to set up A2SERVER to be able to boot Apple II
computers over the network? [y] """)
    if reply.startswith("y") or reply.startswith("Y") or reply == "":
        do_install
