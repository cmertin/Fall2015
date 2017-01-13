#!/bin/bash

base_url="http://www.rcsb.org/pdb/files/"
extension=".pdb"

protein="4ear"

url=$base_url$protein$extension
echo $url
wget $url
