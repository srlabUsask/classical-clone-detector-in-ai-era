#!/bin/bash

cd CloneWorks

./cwbuild -i example/SmoothStream -f example/SmoothStream.files -b example/SmoothStream.fragments -l python -g function -c type3_conservative

./cwdetect -i example/SmoothStream.fragments -o example/SmoothStream.clones -s 0.7 -mil 4