#! /bin/bash
# vim: set tabstop=4 shiftwidth=4 noexpandtab filetype=sh:

# install.sh - a2server main installation script
#
# To the extent possible under law, T. Joseph Carter and Ivan Drucker have
# waived all copyright and related or neighboring rights to the a2server
# scripts themselves.  Software used or installed by these scripts is subject
# to other licenses.  This work is published from the United States.

a2serverVersion="1.9.0"  # Leave this quoted!

if test "x$BASH" = "x"; then
	printf "This script requires bash. Please run\nit as ./install.sh from the source\ndirectory.\n"
	exit 1
fi

# Find the path of our source directory
top_src="$( dirname "${BASH_SOURCE[0]}" )"
pushd $top_src >/dev/null
top_src="$PWD"
popd >/dev/null
if [[ ! -f "$top_src/.a2server_source" ]]; then
	printf "\na2server: cannot find a2server source directory in $top_src.\n\n"
	exit 1
fi

noPicoPkg=
autoAnswerYes=

process_args() {
	while [[ $1 ]]; do
		if [[ $1 == "-c" ]]; then
			shift
			noPicoPkg="-c"
		elif [[ $1 == "-y" ]]; then
			shift
			autoAnswerYes="-y"
		else
			shift
		fi
	done
}

process_args "$@"

# FIXME: Show version, changes, config, allow reconfig, etc…
"$top_src/scripts/show_changes"
cat <<EOF

Your system will be set up for a2server, providing you with
AppleTalk for your Apple IIgs/IIe and Macintosh systems using
netatalk, as well as SMB via Samba.

If a2server is already installed, it will be upgraded to the
latest version.  It would sure be handy if we had an up to
date website to send you to for details.  You should harass
iKarith about that if you haven't recently.

A full installation could take quite awhile on very low-end
systems like the Raspberry Pi Zero.

Also, some actions will need to be performed as the root
(administrator) user.  We are assuming you have access to the
sudo command for that.
EOF
if [[ ! $autoAnswerYes ]]; then
	printf "\nContinue? "
	read
	if [[ ${REPLY:0:1} != "Y" && ${REPLY:0:1} != "y" ]]; then
		[[ $0 == "-bash" ]] && return 2 || exit 2
	fi
fi

# Fix any mistakes we've made in previous versions
. "$top_src/scripts/fixup"

# Run the legacy setup script for anything not yet ported
if [[ -e "${top_src}/setup/ivan.sh" ]]; then
	"${top_src}/setup/ivan.sh" "$@"
fi
