#!/bin/sh
#need perl

if [ -z $1 ] || [ -z $2 ]; then
        echo "Bad argv."
        echo "$0 <form_dir> <to_dir>"
	exit
fi

find $1 -name "*.txt" 2>/dev/null | while read fname
do
	wname=${fname/$1/$2\/}
	echo $fname $wname
	piconv -f cp932 -t cp936 $fname > $wname
done
