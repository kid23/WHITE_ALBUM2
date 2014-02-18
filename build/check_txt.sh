#!/bin/sh

if [ -z $1 ] || [ -z $2 ]; then
	echo "Bad argv."
	echo "$0 <dir> <dir>"
	exit
fi

find $1 -name "*.txt" 2>/dev/null | while read filename1
do
F1=`grep -o "," "$filename1" | wc -l`
filename2=${filename1/$1/$2/}
#echo $filename1 $filename2
F2=`grep -o "," "$filename2" | wc -l`
if [ $F1 != $F2 ]; then
	echo "$filename1 error. $F1 $F2"
#else
	#echo "$filename1 ok."
fi
done

