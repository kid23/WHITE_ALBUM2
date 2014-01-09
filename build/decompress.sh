#!/bin/sh

if [ -z $1 ]; then
	echo "Bad argv."
	echo "$0 <dir>"
	exit
fi

EXTNAME=".elzma"
find $1 -name "*$EXTNAME" 2>/dev/null | while read fname
do
	wname=${fname/$EXTNAME/}
	echo decompress $fname to $wname
	python wa2_eboot_tool.py -d $fname $wname
done
