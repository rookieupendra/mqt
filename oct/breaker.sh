#./breaker.sh -i chunk-9997.txt -s 200 -d /home/upendra/DataGlen/out/
#!/bin/bash 
# This script performs the following functions:
# 1. takes a consolidated jplug data file as input and breaks it into chunks
# 2. calls the upload-data.py on each of those chunks
# input params are:
# 1. name of the consolidated file
# 2. number of records in each of the chunks
# 3. output directory into which those chunks must be placed
if [ "$#" -ne 10 ]; then
    echo "Illegal number of parameters"
    printf "Usage: %s: -i input_file -s output_file_size -d output_directory\n" $0
    exit 2
fi

in_file="brawker.awk"
out_dir="/home/upendra/DataGlen/sept/out/"
out_size= "100"
prefix="chunk"
suffix="txt"
slice=0
log_dir="/var/tmp/bulky/logs"
qos=0
while getopts ":i:s:d:x:q:" opt; do
    case $opt in
	i) in_file="$OPTARG"
	    echo "Input file: $in_file"
	    if ! [ -e $in_file ] ; then
		echo "Input file does not exist.";
		exit 2
	    fi
	    ;;

	s) out_size="$OPTARG"
	    echo "Max size of each output file: $out_size"
	    if  ! [[ $out_size =~ ^\+?[[:digit:]]+$ ]]; then
		echo "Output size must be a positive integer";
		exit 2
	    fi
	    ;;

	d) out_dir="$OPTARG"
	    echo "Output directory: $out_dir"
	    if ! [ -d $out_dir ] || ! [ -e $out_dir ] ; then
		echo "must specify a valid output directory";
		exit 2
	    fi
	    ;;
	x) slice="$OPTARG"
	    echo "slice is":$slice
	    ;;
	q) qos="$OPTARG"
	    echo "QoS is ":$qos
	    ;;

	?) printf "Usage: %s: -i input_file -s output_file_size -d output_directory\n" $0
	    exit 2
	    ;;
    esac
done

echo "running the gawk script"
# cleans up the output directory before creating new files
rm -f $out_dir/$prefix"-*."$suffix
# use the awk script to create output chunks
gawk -f /home/upendra/DataGlen/sept/brawker.awk -v directory=$out_dir -v chunk_size=$out_size -v prefix=$prefix -v suffix=$suffix $in_file
# choose one of the following lines and comment out the other :
# call the python script to upload each of the chunks in sequence.
#find $out_dir -maxdepth 1 -type f  -iname "$prefix-*.$suffix" -print | xargs --verbose -n 1 python3 upload-data.py -o $log_dir -s 0 -i
# Execute the python script in parallel using GNU parallel shell utility
#find $out_dir -maxdepth 1 -type f  -iname "$prefix-*.$suffix" -print | parallel -j 5 python /usr/local/lib/python2.7/dist-packages/kernprof.py -l -v upload-data.py -o $log_dir -s 0 -i
find $out_dir -maxdepth 1 -type f  -iname "$prefix-*.$suffix" -print | parallel -j 5 python upload-data.py -o $log_dir -s 0 -x $slice -q $qos -i

# sudo python /usr/local/lib/python2.7/dist-packages/kernprof.py -l -v helloo.py