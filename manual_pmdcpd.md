# Replication Package for PMD Clone Detection

## Overview
This replication package provides scripts and instructions for running **PMD's Copy-Paste Detector (CPD)** to identify code clones in Python source code. The package automates **clone injection, execution, and analysis**, allowing for systematic evaluation of PMD’s performance on both AI-generated and human-authored code clones.

## Contents of the Package

### 1. Shell Script (`run_pmd.sh`)
This script automates the execution of **PMD CPD** on a given dataset. It performs the following tasks:
- Runs **PMD CPD** with a **minimum token threshold** on the directory
- Detects duplicate code fragments
- Stores clone detection results in `pmd_results.txt`

#### **Usage**
To execute the script, run:

```bash
bash run_pmd.sh
``` 

Ensure that **PMD is installed and properly configured** before running the script.

---

### 2. Python Script
This script automates **clone injection, execution, and result validation** for evaluating PMD’s detection capabilities. 

#### **How to Run**
Execute the Python script as follows:

```bash
python run_pmd.py
``` 

---

## Dependencies
Ensure the following dependencies are installed before running the scripts:

**Java 8+** is required to run **PMD CPD**.


