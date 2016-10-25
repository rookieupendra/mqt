#!/bin/gawk

BEGIN {
    i = 0;
    
    print "awesome"
    print "Directory: ", directory; 
    print "Chunk size: ", chunk_size;
    print "Prefix: ", prefix;
    print "Suffix: ", suffix;
    print "Input file: ", ARGV[1], "\n";
}

{
    # print NR, " : ", $0;
    # if the number records exceeds the specified chunk size, create a new chunk file
    if (NR % chunk_size == 1)  {
       x = directory"/"prefix"-"++i"."suffix;
    }
    # write the new record into either the current chunk file or the one created by the above lines
    print $0 > x;
}

END { 
    print "\n";
    print FILENAME, "broken into ", i, prefix"-*."suffix " files in directory: ", directory".\n";
}
 


