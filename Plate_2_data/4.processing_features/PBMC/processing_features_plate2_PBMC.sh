#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1

#SBATCH --mem=600G
#SBATCH --partition=amem
#SBATCH --qos=mem
#SBATCH --time=72:00:00
#SBATCH --output=sample-%j.out

module purge

module load anaconda

# activate the main conda environment
conda activate interstellar_data

# convert all notebooks to python files into the scripts folder
jupyter nbconvert --to python --output-dir=scripts/ *.ipynb

# run the python scripts in order (from convert+merge, annotate, normalize, feature select, and extract image features)
echo "Starting processing of plate 2 data"

echo "Converting and merging plate 2 data"
python scripts/0.merge_sc_plate2.py 
echo "Annotating plate 2 data"
python scripts/1.annotate_sc_plate2.py
echo "Combining plate 2 data"
python scripts/2.combine_sc_runs_plate2.py 
echo "Normalizing plate 2 data"
python scripts/3.normalize_sc_plate2.py 
echo "Feature selecting plate 2 data"
python scripts/4.feature_select_sc_plate2.py
echo "Extracting image features from plate 2 data"
python scripts/5.extract_image_features.py
echo "Processing of plate 2 data complete"
