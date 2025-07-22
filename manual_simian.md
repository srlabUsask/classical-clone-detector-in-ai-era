# Replication Package for Simian Clone Detection

## Overview
This replication package provides scripts and instructions for running **Simian**, a classical **Code Clone Detection (CCD)** tool, on AI-generated and human-authored code. The package includes automation scripts to execute Simian, inject clones into test files, and analyze the detection performance.

## Contents of the Package

### 1. Shell Script (`run_simian.sh`)
This script automates the execution of **Simian** on a specified dataset. It performs the following tasks:
- Navigates to the `simian-4.0.0` directory
- Runs Simian with a **threshold
- Stores detection results in `simian_result.txt`

#### **Usage**
To execute the script, run:

```bash
bash run_simian.sh
``` 

Ensure that **Simian** is properly set up before running the script.

---

### 2. Python Script
The Python script automates **clone injection, execution, and post-processing analysis**. It follows these steps:


#### **How to Run**
Execute the Python script as follows:

```bash
python run_simian.py
```

