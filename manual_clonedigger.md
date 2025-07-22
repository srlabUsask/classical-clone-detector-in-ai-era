# Replication Package for Clone Detection using CloneDigger

## Overview
This replication package provides scripts and instructions for using **CloneDigger**, a classical **Code Clone Detection (CCD)** tool, to detect duplicate code fragments in Python projects. The package automates **code preprocessing, injection, execution, and post-processing analysis**, enabling systematic evaluation of CloneDigger’s performance on detecting clones.

## Contents of the Package

### 1. Shell Script (`run_clonedigger.sh`)
This script automates the execution of **CloneDigger** on a given dataset. It performs the following tasks:
- Navigates to the `clonedigger-svn-r211-trunk/` directory
- Runs CloneDigger on the project
- Outputs clone detection results in `output.html`

#### **Usage**
To execute the script, run:

```bash
bash run_clonedigger.sh
``` 

Ensure that **CloneDigger is installed and properly configured** before running the script.

---

### 2. Python Script 
This script automates **clone injection, execution, and result validation**.


#### **How to Run**
Execute the Python script as follows:

```bash
python run_clonedigger.py
```

---

## Dependencies
Ensure the following dependencies are installed before running the scripts:

**CloneDigger requires Python 2.7** and dependencies from its official package.

---
