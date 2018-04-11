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

a2sDevel="$( dirname "${BASH_SOURCE[0]}" )"
if [[ -f "$a2sDevel/.a2server_source" ]]; then
	pushd $a2sDevel >/dev/null
	a2sDevel="$PWD"
	popd >/dev/null
else
	printf "a2server: Cannot find a2server source tree relative to ${BASH_SOURCE[0]}\n\n"
	exit 1
fi

# Run the legacy setup script for anything not yet ported
if [[ -e "${a2sDevel}/setup/index.txt" ]]; then
	source "${a2sDevel}/setup/index.txt" "$@"
fi
