# Create and edit LoadData csv and calculate illumination correction function

In this module, we created a LoadData csv, edited to remove rows that are not the last z-plane and corrected paths to maximum projection images (as they have the same name as the last z-plane), and ran a CellProfiler pipeline for calculating an illumination correction (IC) function for all images in each channel. 
An IC function (`.npy` file) per channel is created based on all images in a channel.

This methodology is inspired by [a project from the Broad Institute](https://github.com/broadinstitute/imaging-platform-pipelines/tree/455d8ffa2a0a6cb7341868139f3f1719b9d5ea2c/cellpainting_ipsc_20x_phenix_with_bf_bin1_cp4).
We discussed the process with Erin Weisbart in [an image.sc post](https://forum.image.sc/t/performing-max-projection-using-phenix-data-based-on-broad-institute-project/77262).

## pe2loaddata

To create the LoadData csv file for CellProfiler, we use a software called [pe2loaddata](https://github.com/broadinstitute/pe2loaddata/tree/220ac512bfc0c2e582d379b19411c1585272aee3). 
This will create a LoadData csv from the Phenix metadata XML file generated from data acquisition. 

## Step 1: Create CellProfiler environment

If you do not already have CellProfiler installed in a conda environment, please reference [the README from wave1 data](../../0.wave1_data/1.cellprofiler_ic_processing/README.md) for the instructions.

We are using CellProfiler v4.2.4 for all pipelines.

## Step 2: Install pe2loaddata

If you have not already installed `pe2loaddata`, use follow the instructions from [the README from wave1 data](../../0.wave1_data/1.cellprofiler_ic_processing/README.md) to create the pe2loaddata environment.

## Step 3: Create and correct LoadData csv

To create the LoadData csv for CellProfiler, the format to is as follows:

```sh
pe2loaddata --index-directory <index-directory> config.yml output.csv
```

To create the LoadData csv, make sure to change the paths within the [create_edit_loaddata_csv.ipynb](create_edit_loaddata_csv.ipynb) to reflect your local machine paths before running the code below (e.g. a local path for my computer starts with `/home/jenna`).

To be able to load in the correct images for the IC pipeline, the csv is corrected to remove rows that aren't the last z-plane (see documentation from previous module for reasoning) and the pathing is updated to where the maximum projection images are located.

Run this code in terminal to create the csv file:

```sh
bash create_loaddata_illum_csv.sh
```

## Step 4: Calculate IC function for each channel in CellProfiler

To calculate the illumination correction function for both channels in the data, run the [interstellar_wave3_illum.cppipe](interstellar_wave2_illum.cppipe) pipeline in the CellProfiler GUI to output the two functions (`.npy` files) to use in the analysis pipeline.

To run this pipeline and calculate the IC function for 6 channels (960 image sets), it took approximately 35 minutes.
