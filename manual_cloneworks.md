# Replication Package for Clone Detection using CloneWorks

## Overview
This replication package provides scripts and instructions for using **CloneWorks**, a classical **Code Clone Detection (CCD)** tool. The package automates **code preprocessing, injection, execution, and post-processing analysis**, allowing systematic evaluation of CloneWorks for detecting different types of clones.

## Contents of the Package

### 1. Shell Script (`run_cloneworks.sh`)
This script automates the execution of **CloneWorks** on a given dataset. It performs the following tasks:
- Navigates to the `CloneWorks/` directory
- **Builds clone representations** from input files
- **Detects clones** using **conservative normalization**
- Stores detected clone results

#### **Usage**
To execute the script, run:

```bash
bash run_cloneworks.sh
``` 

Ensure that **CloneWorks is installed and properly configured** before running the script.

---

### 2. Python Script 
This script automates **clone injection, execution, and result validation**.

#### **How to Run**
Execute the Python script as follows:

```bash
python run_cloneworks.py
```

---

## Dependencies
Ensure the following dependencies are installed before running the scripts:

**CloneWorks requires a C++ compiler and proper environment setup**.

