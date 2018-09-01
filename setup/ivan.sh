#! /bin/bash
# vim: set tabstop=4 shiftwidth=4 noexpandtab filetype=sh:

# A2SERVER master setup script, last update 17-Nov-15
# it downloads and executes several scripts related to the setup of
# netatalk configured for Apple II use on Debian or Raspbian.
# more info is at http://ivanx.com/a2server

a2serverVersion="1.9.0"
a2sScriptURL="https://raw.githubusercontent.com/RasppleII/a2server/master"

# Find the path of our source directory
a2sSource="$( dirname "${BASH_SOURCE[0]}" )/.."
pushd $a2sSource >/dev/null
a2sSource="$PWD"
popd >/dev/null
if [[ ! -f "$a2sSource/.a2server_source" ]]; then
	printf "\na2server: cannot find a2server source directory in $a2sSource.\n\n"
	exit 1
fi

compare_version="$a2sSource/scripts/compare_version"

isRpi=
[[ -f /usr/bin/raspi-config ]] && isRpi=1

isDebian=
if [[ "$(lsb_release -ds)" = Debian* ]]; then
	debianVersion="$(lsb_release -rs)"
	if [[ "$debianVersion" -ge 7 || $debianVersion == [a-z]* ]]; then
		isDebian=1
	fi
fi

if [[ -f /usr/local/etc/A2SERVER-version ]]; then
	read installedVersion </usr/local/etc/A2SERVER-version
    if [[ $installedVersion != *.*.* ]]; then
		# Deal with old three-digit version
        installedVersion="${installedVersion:0:1}.${installedVersion:1:1}.${installedVersion:2}"
    fi
fi
echo "A2SERVER version available: $a2serverVersion"
echo "A2SERVER version installed: ${installedVersion:=None}"
if [[ $installedVersion == "None" ]]; then
	installedVersion=0
fi

skipRepoUpdate=
autoAnswerYes=
installAll=
setupNetBoot=
setupWindowsSharing=
compileAlways=
rm -rf /tmp/a2server-install
rm /tmp/a2server-* 2> /dev/null
while [[ $1 ]]; do
	if [[ $1 == "-r" ]]; then
		shift
		skipRepoUpdate="-r"
		touch /tmp/a2server-packageReposUpdated
	elif [[ $1 == "-i" ]]; then
		shift
		installAll="-i"
	elif [[ $1 == "-y" ]]; then
		shift
		autoAnswerYes="-y"
		touch /tmp/a2server-autoAnswerYes
	elif [[ $1 == "-b" ]]; then
		shift
		setupNetBoot="-b"
		touch /tmp/a2server-setupNetBoot
	elif [[ $1 == "-w" ]]; then
		shift
		setupWindowsSharing="-w"
		touch /tmp/a2server-setupWindowsSharing
	elif [[ $1 == "-c" ]]; then
		shift
		compileAlways="-c"
		touch /tmp/a2server-compileAlways
	elif [[ $1 == "-v" ]]; then
		shift
		# Version was already printed
		if [[ $0 == "-bash" ]]; then
			return 1
		else
			exit 1
		fi
	elif [[ $1 ]]; then
		echo "options:"
		echo "-v: display installed and available versions, then exit"
		echo "-i: reinstall A2SERVER software (but not Apple II software)"
		echo "-y: auto-answer yes to all prompts"
		echo "-r: don't update package repositories"
		echo "-b: auto-setup network boot (use with -y)"
		echo "-w: auto-setup Windows file sharing (use with -y)"
		echo "-c: compile non-package items, rather than downloading binaries"
		if [[ $0 == "-bash" ]]; then
			return 1
		else
			exit 1
		fi
	fi
done

if "$compare_version" $installedVersion lt 1.1.0; then
	echo
	echo "WARNING: The current A2SERVER installer scripts haven't been tested for"
	echo "updating the earlier version of A2SERVER that you have. A fresh install"
	echo "is suggested. Continuing is not recommended and could make A2SERVER"
	echo "no longer work properly, or cause data to be lost."
fi

a2server_update=0
doSetup=1

if "$compare_version" $installedVersion lt 1.5.2; then
	a2server_update=1
fi

unsupportedOS=1
if [[ $isRpi ]]; then #supported Raspbian? (16-Feb-15, 20-Jun-14, 09-Jan-14, etc)
	fwhash=$(zcat /usr/share/doc/raspberrypi-bootloader/changelog.Debian.gz | grep -m 1 'as of' | awk '{print $NF}')
	fwsupported="-8aca5762- -462f3e3f476f7b6- -c32bc633039cd9- -9d34d0475f9-
			-d4f5315cfac4e- -6f4a90c8cb8817f- -5dd9b4962e- -17c8799375-
			-960832a6c2590635216c296b6ee0bebf67b21d50-
			-2a329e0c7d8ea19c085bac5633aa4fccee0f21be-
			-b2420fc150ae4616f5d9ec24bdaedc630586a529-"
	if [[ "$fwsupported" == *-$fwhash-* ]]; then
		unsupportedOS=
	fi
elif [[ $isDebian ]]; then # supported Debian?
	 debianVersion=$(cat /etc/debian_version)
	 debianSupported="-9.2- -8.2- -7.9- -7.8- -7.6- -7.3-"
	 [[ $debianSupported == *-$debianVersion-* ]] && unsupportedOS=
fi

if [[ $unsupportedOS && $isRpi ]]; then
	echo
	echo "A2SERVER and its installer scripts have been tested on Raspbian Wheezy,"
	echo "Jessie, and Stretch though not this specific firmware version"
	echo "(${fwhash:0:7}). Just FYI."
	unsupportedOS=
elif [[ $unsupportedOS && $isDebian ]]; then
	echo
	echo "A2SERVER and its installer scripts have been tested on Debian 7/8/9,"
	echo "though not this specific point release ($debianVersion). Just FYI."
	unsupportedOS=
fi

if [[ $unsupportedOS ]]; then
	echo
	echo "WARNING: A2SERVER and its installer scripts have only been tested on"
	echo "Debian and Raspbian. Continuing is probably fine, but might not be."
	echo "Theoretical worst case would be your operating system no longer works"
	echo "properly or data is lost, so consider backing up first."
fi

doSetup=1
if [[ $installAll || ! -f /usr/local/etc/a2server-help.txt ]] || (( $a2server_update )); then
	echo
	echo "Setting up A2SERVER will take up to 60 minutes, during which"
	echo "you'll see a bunch of stuff spit out across the screen."
	echo
	if [[ ! $autoAnswerYes ]]; then
		echo -n "Ready to set up A2SERVER? "
		read
		[[ ${REPLY:0:1} == "y" || ${REPLY:0:1} == "Y" ]]; doSetup=$(( 1 - $? ))
	fi
fi

if (( $doSetup )); then

	echo
	echo "a2server-setup modifies files and performs actions as the root user."
	echo "For details, visit http://ivanx.com/a2server."
	echo
	if [[ ! $autoAnswerYes ]]; then
		echo -n "Continue? "
		read
		[[ ${REPLY:0:1} == "y" || ${REPLY:0:1} == "Y" ]]; doSetup=$(( 1 - $? ))
	fi

	if (( $doSetup )); then

		origDir="$PWD"
		rm -rf /tmp/a2server-install &>/dev/null
		mkdir -p /tmp/a2server-install

		read -d '' a2sSubScripts <<-EOF
			a2server-1-storage.txt
			a2server-2-tools.txt
			a2server-3-sharing.txt
			a2server-5-netboot.txt
			a2server-6-samba.txt
			a2server-7-console.txt
		EOF

		if [[ $installAll ]]; then
			sudo rm -f /usr/local/etc/A2SERVER-version
			sudo rm -f /usr/local/bin/nulib2
			sudo rm -f /usr/local/bin/unar
			sudo rm -f /usr/local/sbin/macipgw
			sudo rm -f /usr/local/bin/ciopfs
			sudo rm -f /usr/local/etc/netatalk/afppasswd
			sudo rm -f /usr/local/etc/netatalk/a2boot/p8
			sudo rm -f /usr/local/etc/netatalk/a2boot/ProDOS16\ Image
		fi

		for _script in $a2sSubScripts; do
			"$a2sSource/scripts/$_script"
		done

		rm -f /tmp/a2server-packageReposUpdated

		echo "$a2serverVersion" | sudo tee /usr/local/etc/A2SERVER-version &> /dev/null

		source /usr/local/etc/a2serverrc

		# get Kernel release (e.g. 3.6.11+) and version (e.g. #557)
		kernelRelease=$(uname -r)
		kernelMajorRelease=$(cut -d '.' -f 1 <<< $kernelRelease)
		kernelMinorRelease=$(cut -d '.' -f 2 <<< $kernelRelease | sed 's/\(^[0-9]*\)[^0-9].*$/\1/')

		echo
		# all done, see if AppleTalk is available and notify either way
		if [[ $(ps aux | grep [a]talkd) ]]; then
			echo "You now have a fully functional file server for Apple II clients."
			echo "On an Apple IIe, it should be accessible via \"Log In\" on the"
			echo "Workstation Card software. For IIgs users, it should be accessible"
			echo "via the AppleShare control panel."
			if [[ -f /srv/A2SERVER/A2FILES/System/Start.GS.OS ]]; then
				echo
				echo "You can network boot GS/OS."
				echo "On a ROM 01 IIgs, set slot 1 (printer port), or slot 2 (modem port)"
				echo "to Your Card, and slot 7 to AppleTalk, and Startup Slot to 7 or Scan."
				echo "On a ROM 3 IIgs, set slot 1 or 2, and Startup Slot, to AppleTalk."
			fi
			if [[ -f /srv/A2SERVER/A2FILES/BASIC.System ]]; then
				echo
				echo "You can network boot ProDOS 8. On an Apple IIe, put your Workstation Card"
				echo "in a slot above your disk controller card, or type PR#X with open-apple"
				echo "held down, with X being the slot of your Workstation Card."
				echo 'On a IIgs, press "8" during the initial procession of periods.'
			fi
			echo
			echo "A2SERVER setup is complete! Go connect from your Apple II!"
			echo
		elif [[ -f /tmp/rpiUpdate ]]; then
			echo "A2SERVER is now configured, but Apple II clients will not be able"
			echo "to connect until you restart your Raspberry Pi."
			echo
			if [[ ! $autoAnswerYes ]]; then
				echo -n "Restart now? "
				read
			fi
			if [[ $autoAnswerYes || ${REPLY:0:1} == "Y" || ${REPLY:0:1} == "y" ]]; then
				sudo shutdown -r now
				echo
				echo "A2SERVER: Preparing to restart..."
				while :; do sleep 60; done
			fi
			rm /tmp/rpiUpdate
			echo
		elif [[ $kernelMajorRelease -eq 3 && $kernelMinorRelease -ge 12 && $kernelMinorRelease -le 15 ]]; then
			echo "A2SERVER is now configured, but Apple II clients cannot connect"
			echo "because of a kernel-crashing bug in Linux kernel 3.12 through 3.15."
			echo "You have kernel version $kernelMajorRelease.$kernelMinorRelease."
			echo "A2SERVER has disabled AppleTalk networking to prevent crashes."
			echo "Please use kernel 3.11 or earlier, or kernel 3.16 or later."
			echo
		else
			echo "A2SERVER is now configured, but Apple II clients cannot connect because"
			echo "AppleTalk networking is unavailable. Please make sure that"
			echo "your Linux distribution has a loadable AppleTalk kernel module or"
			echo "has AppleTalk built into the kernel, and restart your server."
			echo "Or, if you previously disabled AppleTalk in A2SERVER, re-enable it"
			echo "by typing 'appletalk-on'."
			echo
		fi

		if [[ -f /tmp/noMacIP ]]; then
			echo
			echo "MacIP connections may be unavailable. If you know how, try"
			echo "recompiling the AppleTalk kernel module with IPDDP options disabled."
			echo
			rm /tmp/noMacIP
		fi

		if [[ -f /tmp/singleUser ]]; then
			if [[ ! $autoAnswerYes ]]; then
				echo
				echo "Your Raspberry Pi was started in single-user mode in order to"
				echo -n "fix a problem. You should restart to operate normally. Restart now? "
				read
			fi
			if [[ $autoAnswerYes || ${REPLY:0:1} == "Y" || ${REPLY:0:1} == "y" ]]; then
				sudo shutdown -r now
				echo
				echo "A2SERVER: Preparing to restart..."
				while :; do sleep 60; done
			fi
			rm /tmp/singleUser
			echo
		fi

		echo
		echo "Type 'system-shutdown' to turn off A2SERVER."
		echo "Type 'a2server-setup' to configure network boot."
		echo "Type 'a2server-help' for a list of other commands."
	fi
fi

unset a2server_update 2> /dev/null
unset doSetup 2> /dev/null
rm -rf /tmp/a2server-install &>/dev/null
rm -f /tmp/a2server-* 2> /dev/null
rm -f setup &> /dev/null
