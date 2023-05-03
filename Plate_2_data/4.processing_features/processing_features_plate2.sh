#!/bin/bash

# initialize the correct shell for your machine to allow conda to work (see README for note on shell names)
conda init bash
# activate the main conda environment
conda activate interstellar_data

# convert all notebooks to python files into the scripts folder
jupyter nbconvert --to python --output-dir=scripts/ *.ipynb

# run the python scripts in order (from convert+merge, annotate, normalize, feature select, and extract image features)
python scripts/0.merge_sc_plate2.py 
python scripts/1.annotate_sc_plate2.py
python scripts/2.combine_sc_runs_plate2.py 
python scripts/3.normalize_sc_plate2.py 
python scripts/4.feature_select_sc_plate2.py
python scripts/5.extract_image_features
