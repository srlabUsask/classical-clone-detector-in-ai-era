# Are classical clone detectors good enough for the AI era? 

Device used for this research: Linux (Ubuntu 22.04 LTS) machine with 128 GB of RAM, 12th Gen Intel® Core™ i7-12700K processor and NVIDIA GeForce RTX 3080 GPU.

Accepted in 41st International Conference on Software Maintenance and Evolution (ICSME), 2025.

## Download benchmarks

BigCloneBench: https://github.com/clonebench/BigCloneBench

SemanticCloneBench: https://drive.google.com/file/d/1KicfslV02p6GDPPBjZHNlmiXk-9IoGWl/view

GPTCloneBench: https://github.com/srlabUsask/GPTCloneBench


## Interviews
Expert opinions (conversation transcript) can be found in interviews folder.


### To reproduce the work, all the clone detectors must be installed.

## Download and install tools:

Follow the given instruction to download and install the tool in respective URL.

PMD/CPD: https://pmd.github.io/pmd/pmd_userdocs_installation.html

Simian: https://simian.quandarypeak.com/download/

    For Simian, you can download by accepting their academic license and in case commercial purpose, authorization required.

Deckard: https://github.com/skyhover/Deckard

Clone Digger: https://sourceforge.net/p/clonedigger/svn/HEAD/tree/trunk/

CCCD: https://github.com/Code-Clone-Detection-Images/Concolic-Code-Clone-Detection

CloneWorks: https://github.com/jeffsvajlenko/CloneWorks

StoneDetector: https://github.com/StoneDetector/StoneDetector

ASTNN: https://github.com/zhangj111/astnn

CodeBERT: https://github.com/microsoft/CodeBERT


## How to run tools

Apart from CCCD, for rest of the tools Python version 3.6 has been used to run. For CCCD, docker installation required. 

Docker installation guideline: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04


Each file is associated with a sh file. To run a tool, use run_<tool_name>.py file. It will call run_<tool_name>.sh file where necessary commands are given to run.


For example, to PMD/CPD, you need to run `python run_pmd.py` file. It will within itself call `run_pmd.sh` file.

For CodeBERT and ASTNN, bash file not required as they are using model architecture to design and run.


To cite this work:

```

@inproceedings{alam2025classical,
  author    = {Alam, Ajmain I. and Roy, Palash R. and Al-omari, Farouq and Roy, Chanchal and Roy, Banani and Schneider, Kevin},
  title     = {Are Classical Clone Detectors Good Enough For the AI Era?},
  year      = {2025},
  booktitle = {Proceedings of the 41st International Conference on Software Maintenance and Evolution (ICSME)},
  location  = {Auckland, New Zealand},
  series    = {ICSME '25}
}

```
