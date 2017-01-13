#!/bin/bash

if [ $# -ne 1 ]; then
   echo ""
   echo "Script needs only one parameter, the file to append the line to."
   echo "Exiting..."
   echo ""
   exit
fi

if [ ! -f "$1" ]; then
   echo ""
   echo "File \"$1\" does not exist."
   echo "Exiting..."
   echo ""
   exit
fi

STRING="1,2,3,4,5,6,7,8,9,Win"

sed -i "1s/^/$STRING\n/" $1

echo "$STRING"
echo "added to the top of $1"
