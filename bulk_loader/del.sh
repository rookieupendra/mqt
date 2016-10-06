#!/bin/sh
file="outputfile.txt"

if [ -f $file ] ; then
    rm $file
else 
	echo "outputfile.txt not found"
fi
file="log_file"

if [ -f $file ] ; then
    rm $file
else 
	echo "log_file not found"
fi
file="out/*"

if [ -f $file ] ; then
    rm $file
else 
	echo "no chunk files found"
fi
