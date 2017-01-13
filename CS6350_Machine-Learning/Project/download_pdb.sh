#!/bin/bash

base_folder="Protein_Data/"
base_url="http://www.rcsb.org/pdb/files/"
extension=".pdb"
file="pdb_proteins.dat"

protein="4ear"
total=`wc -l $file | grep -Eo '[0-9]*'`

url=$base_url$protein$extension

i=1
while read protein; do
    out_path=$base_folder$protein
    url=$base_url$protein$extension
    echo "Downloading $protein ($i/$total)"
    wget -q $url -P $out_path
    ((i++))
done < $file
