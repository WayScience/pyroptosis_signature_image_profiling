# Perform CellProfiler analysis on Interstellar wave 3 data

In this module, we create a LoadData csv with the illumination correction function to use in the [LoadData module in CellProfiler](https://cellprofiler-manual.s3.amazonaws.com/CPmanual/LoadData.html), edit this csv to contain the correct pathing and rows, and perform IC, segmentation, and feature extraction using CellProfiler.

We run the [interstellar_wave3_analysis.cpproj](interstellar_wave1_analysis.cpproj) pipeline and outputted one sqlite file containing all of the feature and whole image measurements. 


## Step 1: Create LoadData csv with illumination functions included and edit it

To create the LoadData csv to use in the analysis pipeline, `pe2loaddata` uses the following structure:

```sh
pe2loaddata --index-directory <index-directory> path/to/config.yml path/to/output.csv --illum --illum-directory <illum-directory> --plate-id <plate-id> --illum-output output_with_illum.csv
```

To create the LoadData csv with illum, make sure to change the paths within the [create_edit_illum_loaddata_csv.ipynb](create_edit_illum_loaddata_csv.ipynb) to reflect your local machine paths before running the code below (e.g. a local path for my computer starts with `/home/jenna`).

After this, you will run the `edit_loaddata_csv` function in the notebook to correct the path and remove unnecessary row as decribed in the previous module.

Run this code in terminal to create the csv file:

```sh
bash create_edit_illum_loaddata_csv.sh
```

## Step 2: Run `interstellar_wave3_analysis.cppipe` in CellProfiler

To create the sqlite file, we ran the pipeline in the CellProfiler GUI where it took approximately 51 hours to run.

## Step 3: Run `interstellar_wave3_imagequality.cppipe` in CellProfiler

To assess the image quality of the wave 3 data, we ran this pipeline in CellProfiler GUI to output image feature readouts. 
It is caluclating image quality measurements on the raw images and the corrected images (w/ illumination correction).
It took
