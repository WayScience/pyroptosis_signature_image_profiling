#!/bin/bash
jupyter nbconvert --to python create_loaddata_wave2_csv.ipynb
python create_loaddata_wave2_csv.py
