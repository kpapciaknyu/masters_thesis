#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/gpfs/data/pcc_lab/shared/py_packages

module load python/gpu/3.7.6  
python3 deepseek.py
