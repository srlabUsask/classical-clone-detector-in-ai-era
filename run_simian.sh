#!/bin/bash

cd simian-4.0.0

java -jar simian-4.0.0.jar  -threshold=6 "v2rayn_simian/*.cs" > simian_result.txt
