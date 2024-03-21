#!/bin/bash


#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=250G
#SBATCH --partition=amilan
#SBATCH --qos=normal
#SBATCH --time=24:00:00
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

# echo "Processing of plate 2 data steps 0-1 complete"
