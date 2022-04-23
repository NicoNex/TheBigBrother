#!/bin/bash

function install {
	sudo pip install -r requirements.txt
	chmod +x bigbrother
	mkdir -p $HOME/.local/bin
	cp bigbrother $HOME/.local/bin/
	mkdir -p $HOME/.local/share/bigbrother
	cp police.mp3 $HOME/.local/share/bigbrother
	echo ok
}

function uninstall {
	rm -rf $HOME/.local/bin/bigbrother $HOME/.local/share/bigbrother
	echo ok
}

function usage {
	cat << EOF
Usage: $0 OPTIONS
This script installs or uninstalls The Big Brother.
OPTIONS:
	-i            Install The Big Brother.
	-r            Uninstall The Big Brother.
	-h, --help    Print this help message.
EOF
}

case $1 in
	-h | --help)
		usage
		;;
	-i)
		install
		;;
	-r)
		uninstall
		;;
	*)
		usage
		;;
esac

