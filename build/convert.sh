#!/bin/sh

if [ $? < 3 ]; then
	exit
fi

find $1 -name "*.txt" 2>/dev/null | while read fname
do
	wname=${fname/$1/$2}
	echo $fname $wname
	piconv -f cp932 -t cp936 $fname > $wname
done
