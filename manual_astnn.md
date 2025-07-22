# Replication Package for Code Clone Detection using ASTNN

## Overview
This replication package provides scripts and instructions for using **ASTNN (Abstract Syntax Tree-based Neural Network)** for code clone detection. The package automates **data preprocessing, AST parsing, embedding generation, model training, and evaluation** using ASTNN.

## Contents of the Package

### 1. ASTNN Pipeline 
This script automates **data preprocessing, AST parsing, embedding generation, and dataset preparation**.


#### **How to Run**
Execute the pipeline script as follows:

```bash
python astnn_pipeline.py
``` 


---

### 2. ASTNN Training & Evaluation 
This script **trains the ASTNN model and evaluates it** on a benchmark dataset.


#### **How to Run**
Execute the script as follows:

```bash
python run_astnn.py
``` 

---

## Dependencies
Ensure the following dependencies are installed before running the scripts:

```bash
pip install torch pandas numpy gensim tqdm javalang
``` 

Additionally, **ASTNN requires PyTorch and Word2Vec embeddings**.

---

## Supporting files
- astnn_model.py
- astnn_tree.py
- astnn_utils.py
