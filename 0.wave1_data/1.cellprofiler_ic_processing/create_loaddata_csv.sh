#!/bin/bash
jupyter nbconvert --to python create_loaddata_csv.ipynb
python create_loaddata_csv.py
