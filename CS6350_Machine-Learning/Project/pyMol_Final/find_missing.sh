#!/bin/bash
# This script is to simply check to make sure that all the protein directories
# contain all the files needed. This only checks for the very last file that
# is created in the script as the other files *must* be created before it.
# Therefore, if it doens't exist, then there's a chance there's something wrong
# with the others and the whole protein needs to be redone. 

FILE="*aminos.dat"

for D in `find /uusoc/scratch/mir/cmertin/Project/Protein_Data/ -type d`; do
    FILE_LOOKUP="$D/$FILE"
    if [ ! -f $FILE_LOOKUP ]; then
	echo $FILE_LOOKUP
    fi
done
