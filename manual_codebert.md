# Replication Package for Code Clone Detection using CodeBERT

## Overview
This replication package provides scripts and instructions for using **CodeBERT**, a transformer-based model for detecting code clones. The package automates **data preprocessing, tokenization, feature extraction, and clone classification** using CodeBERT.

## Contents of the Package

### 1. CodeBERT Clone Detection Script 
This script automates **code pair comparison using CodeBERT**. It performs the following tasks:
- **Preprocesses source code** by removing comments and docstrings
- **Tokenizes code snippets** using the CodeBERT tokenizer
- **Converts tokens to embeddings** and generates input sequences
- **Passes tokenized sequences through CodeBERT** for classification
- **Determines whether the code pair is a clone or not**


#### **How to Run**
Execute the Python script as follows:

```bash
python run_codebert.py
```

Ensure that the **CodeBERT model is properly downloaded and configured** before execution.

---

## Key Features

### 1. **Code Clone Detection using CodeBERT**
- **Uses a transformer-based approach** to detect code clones
- **Generates tokenized feature vectors** for similarity assessment

### 2. **Performance Analysis**
- **Outputs total detected clones and non-clones**
- **Uses `argmax` classification on CodeBERT embeddings**

---

## Dependencies
Ensure the following dependencies are installed before running the scripts:

```bash
pip install torch transformers tqdm seaborn
``` 

Additionally, **Python 3.6+** and **PyTorch** are required.

---

## Supporting files
- model.py
- codeBERT_model.bin
