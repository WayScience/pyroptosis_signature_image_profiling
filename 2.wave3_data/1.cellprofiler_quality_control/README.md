# Create LoadData csvs to create maximum projection images

In this module, we create two LoadData csv and CellProfiler pipelines for performing maximum projection on the images and saving them.
This pipeline names the max projected images as the last z-plane.
In our case we have 3 z-planes (p01-p03) so our images contain the last z-plane p03.

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

To create the LoadData csv, make sure to change the paths within the [create_loaddata_maxproj_wave3_csv.ipynb](create_loaddata_maxproj_wave3_csv.ipynb) to reflect your local machine paths before running the code below (e.g. a local path for my computer starts with `/home/jenna`).

Run this code in terminal to create the csv file:

```sh
bash create_loaddata_illum_csv.sh
```

## Step 4: Create the maximum projection images for each channel and site in CellProfiler

To create the maximum projection images for each channel and site, run the [zproj.cppipe](zproj.cppipe) pipeline in the CellProfiler GUI.

To run this pipeline, it took approximately 30 minutes.
