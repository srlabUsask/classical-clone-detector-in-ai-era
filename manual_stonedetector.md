# Replication Package for StoneDetector Evaluation

## Overview
This replication package provides all necessary scripts and instructions for evaluating **StoneDetector**, a classical **Code Clone Detection (CCD)** tool. The package includes **automation scripts** for running StoneDetector on AI-generated and human-authored clone benchmarks, **pre-processing utilities**, and **post-processing evaluation scripts**.

## Contents of the Package

### 1. Shell Script (`run_stonedetector.sh`)
This script automates the execution of **StoneDetector** on a given test dataset. It performs the following tasks:
- Navigates to the `StoneDetector` directory
- Compiles StoneDetector using Gradle
- Runs StoneDetector on a sample dataset (`test/JHotDraw`)
- Stores error logs (`errors.txt`) and results (`results.txt`)

#### **Usage**
To execute the script, run:

```bash
bash run_stonedetector.sh
```

Ensure that **StoneDetector** is properly set up before running the script.

---

### 2. Python Scripts (`main_gcb()` and `main_bcb()`)
The Python scripts automate clone injection, execution, and result processing:
- **`main_gcb()`** → Evaluates AI-generated clones**
- **`main_bcb()`** → Evaluates human-authored clones**


#### **How to Run**
Execute the Python script as follows:

```bash
python run_stonedetector.py
```


