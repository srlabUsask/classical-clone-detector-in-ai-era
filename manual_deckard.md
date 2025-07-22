# Replication Package for Deckard Clone Detection

## Overview
This replication package provides scripts and instructions for running **Deckard**, a classical **Code Clone Detection (CCD)** tool, on AI-generated and human-authored clones. The package automates **clone injection, execution, and analysis**, allowing systematic evaluation of Deckard’s performance on detecting syntactic and semantic code clones.

## Contents of the Package

### 1. Shell Script (`run_deckard.sh`)
This script automates the execution of **Deckard** on a given dataset. It performs the following tasks:
- Navigates to the `Deckard/` directory
- Runs Deckard’s clone detection pipeline using the predefined script
- Outputs the detected clone clusters in `clusters/`

#### **Usage**
To execute the script, run:

```bash
bash run_deckard.sh
``` 

Ensure that **Deckard is installed and properly configured** before running the script.

---

### 2. Python Script
This script automates **clone injection, execution, and post-processing analysis**.


#### **How to Run**
Execute the Python script as follows:

```bash
python run_deckard.py
```


## Dependencies
Ensure the following dependencies are installed before running the scripts:

**Deckard requires Java 8+ and appropriate build tools**.


