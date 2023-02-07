#!/bin/bash
jupyter nbconvert --to python create_loaddata_wave1_csv.ipynb
python create_loaddata_wave1_csv.py
