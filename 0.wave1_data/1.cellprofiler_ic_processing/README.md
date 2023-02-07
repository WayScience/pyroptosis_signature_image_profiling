# Create initial LoadData csv to calculate illumination correction function

In this module, we create a LoadData csv and CellProfiler pipeline for calculating an illumination correction function for each channel.

## pe2loaddata

To create the LoadData csv file for CellProfiler, we use a software called [pe2loaddata](https://github.com/broadinstitute/pe2loaddata/tree/220ac512bfc0c2e582d379b19411c1585272aee3). 
This will create a LoadData csv from the Phenix metadata XML file generated from data acquisition. 

## Step 1: Create CellProfiler environment

If you do not already have CellProfiler installed in a conda environment, you can run the code below to create one.

```sh
conda env create -f cellprofiler_environment.yml
```

We are using CellProfiler v4.2.4 for all pipelines.

## Step 2: Install pe2loaddata

Using the code below, install `pe2loaddata` using the [pe2loaddata_env.yml](pe2loaddata_env.yml) file.

```sh
conda env create -f pe2loaddata_env.yml
```

## Step 3: Create LoadData csv

To create the LoadData csv for CellProfiler, the format to is as follows:

```sh
pe2loaddata --index-directory <index-directory> config.yml output.csv
```

To create the LoadData csv, make sure to change the paths within the [create_loaddata_wave1_csv.ipynb](create_loaddata_wave1_csv.ipynb) to reflect your local machine paths before running the code below (e.g. a local path for my computer starts with `/home/jenna`).

Run this code in terminal to create the csv file:

```sh
bash create_loaddata_wave1_csv.sh
```

## Step 4: Calculate IC function for each channel in CellProfiler

To calculate the illumination correction function for both channels in the data, run the [interstellar_wave1_illum.cppipe](interstellar_wave1_illum.cppipe) pipeline in the CellProfiler GUI to output the two functions (`.npy` files) to use in the analysis pipeline.
