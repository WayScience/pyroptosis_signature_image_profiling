# Create and edit LoadData csv and calculate illumination correction function

In this module, we created a LoadData csv, edited to remove uncessary rows and corrected paths to maximum projection images, and ran a CellProfiler pipeline for calculating an illumination correction (IC) function for each channel.

## pe2loaddata

To create the LoadData csv file for CellProfiler, we use a software called [pe2loaddata](https://github.com/broadinstitute/pe2loaddata/tree/220ac512bfc0c2e582d379b19411c1585272aee3). 
This will create a LoadData csv from the Phenix metadata XML file generated from data acquisition. 

## Step 1: Create CellProfiler environment

If you do not already have CellProfiler installed in a conda environment, please reference [the README from wave1 data](../../0.wave1_data/1.cellprofiler_ic_processing/README.md) for the instructions.

We are using CellProfiler v4.2.4 for all pipelines.

## Step 2: Install pe2loaddata

If you have not already installed `pe2loaddata`, use follow the instructions from [the README from wave1 data](../../0.wave1_data/1.cellprofiler_ic_processing/README.md) to create the pe2loaddata environment.

## Step 3: Create LoadData csv

To create the LoadData csv for CellProfiler, the format to is as follows:

```sh
pe2loaddata --index-directory <index-directory> config.yml output.csv
```

To create the LoadData csv, make sure to change the paths within the [create_loaddata_csv.ipynb](create_loaddata_csv.ipynb) to reflect your local machine paths before running the code below (e.g. a local path for my computer starts with `/home/jenna`).

Run this code in terminal to create the csv file:

```sh
bash create_loaddata_illum_csv.sh
```
## Step 4: Correct the LoadData csv

To be able to load in the correct images for the IC pipeline, the csv must be corrected to remove rows that aren't the last z-plane (see documentation from previous module for reasoning) and to correct the pathing to where the maximum projection images are located.

## Step 5: Calculate IC function for each channel in CellProfiler

To calculate the illumination correction function for both channels in the data, run the [interstellar_wave2_illum.cppipe](interstellar_wave2_illum.cppipe) pipeline in the CellProfiler GUI to output the two functions (`.npy` files) to use in the analysis pipeline.

To run this pipeline and calculate the IC function for 4 channels (1152 image sets), it took approximately 20 minutes.
