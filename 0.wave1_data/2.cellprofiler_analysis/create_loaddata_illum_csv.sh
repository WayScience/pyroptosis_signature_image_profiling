#!/bin/bash
jupyter nbconvert --to python create_loaddata_illum_csv.ipynb
python create_loaddata_illum_csv.py
