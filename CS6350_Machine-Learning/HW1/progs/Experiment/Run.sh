#!/bin/bash

echo "*************************************************"
echo "  Running ID3 over the data                      "
echo "*************************************************"
./RunID3.py


echo ""
echo "*************************************************"
echo "  Running K-nearest neighbors over the data      "
echo "*************************************************"
./k-NN.py
