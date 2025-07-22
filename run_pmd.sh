#!/bin/bash

pmd-bin-7.0.0-rc3/bin/pmd cpd --minimum-tokens 50 --dir pmd/django --language py > pmd_results.txt
