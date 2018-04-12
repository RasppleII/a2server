#! /bin/bash
# vim: set tabstop=4 shiftwidth=4 noexpandtab filetype=sh:

# install.sh - a2server main installation script
#
# To the extent possible under law, T. Joseph Carter and Ivan Drucker have
# waived all copyright and related or neighboring rights to the a2server
# scripts themselves.  Software used or installed by these scripts is subject
# to other licenses.  This work is published from the United States.

a2serverVersion="1.9.0"
a2sScriptURL="https://raw.githubusercontent.com/RasppleII/a2server/master"

# Find the path of our source directory
a2sSource="$( dirname "${BASH_SOURCE[0]}" )"
echo $a2source
pushd $a2sSource >/dev/null
a2sSource="$PWD"
popd >/dev/null
if [[ ! -f "$a2sSource/.a2server_source" ]]; then
	printf "\na2server: cannot find a2server source directory in $a2sSource.\n\n"
	exit 1
fi

# Run the legacy setup script for anything not yet ported
if [[ -e "${a2sSource}/setup/ivan.sh" ]]; then
	"${a2sSource}/setup/ivan.sh" "$@"
fi
