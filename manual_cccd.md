# Replication Package for Concolic Code Clone Detection (CCCD)

## Overview
This replication package provides scripts and instructions for using **Concolic Code Clone Detection (CCCD)**, a tool designed to detect clones in C source code using concolic execution. The package automates **code preprocessing, injection, execution, and post-processing analysis**, allowing systematic evaluation of CCCD for detecting code clones.

## Contents of the Package

### 1. Shell Script (`run_cccd.sh`)
This script automates the execution of **CCCD** on a given dataset. It performs the following tasks:
- Navigates to the `Concolic-Code-Clone-Detection/` directory
- Runs CCCD on the folder
- Generates a **comparison report**

#### **Usage**
To execute the script, run:

```bash
bash run_cccd.sh
```

Ensure that **CCCD is installed and properly configured** before running the script.

---

### 2. Python Script
This script automates **clone injection, execution, and result validation**.

#### **How to Run**
Execute the Python script as follows:

```bash
python run_cccd.py
```

---

## Dependencies
Ensure the following dependencies are installed before running the scripts:

**CCCD requires a C compiler and appropriate concolic execution environment**.

---

