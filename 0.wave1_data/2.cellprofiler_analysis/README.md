# Perform CellProfiler analysis on Interstellar wave 1 data

In this module, we create a LoadData csv with the illumination correction function to use in the [LoadData module in CellProfiler](https://cellprofiler-manual.s3.amazonaws.com/CPmanual/LoadData.html) and perform segmentation + feature extraction using CellProfiler.

We run the [interstellar_wave1_analysis.cpproj](interstellar_wave1_analysis.cpproj) pipeline and output three sqlite files. 
Each file corresponds to a dilation size (Figure 1):

1) interstellar_wave1_dilate25 = Dilation structuring element disk with size 25 pixels (approx. half the average cell diameter)
2) interstellar_wave1_dilate50 = Dilation structuring element disk with size 50 pixels (approx. equal to the average cell diameter)
3) interstellar_wave1_dilate100 = Dilation structuring element disk with size 100 pixels (approx. double the average cell diameter)

![dilation_ex.png](figures/dilation_ex.png)

> Figure 1. CellProfiler dilation sizes and respective objects. 
> This figure shows how the various sizes for dilation in the `DilateObjects` module impacts the nuclei in an image. 
> The images for each dilation are split into the two objects, `Dilated Nuclei` which are the nuclei that are dilated and `Translocated Nuclei` which are the `Dilated Nuclei` with the original `Nuclei` subtracted from the object. 

We decided to test with various dilation values since we do not know how far Gasdermin-D translocates.
We will be able to assess the best dilate value during further analysis.

## Step 1: Create LoadData csv with illumination functions included

To create the LoadData csv to use in the analysis pipeline, `pe2loaddata` uses the following structure:

```bash
pe2loaddata --index-directory <index-directory> path/to/config.yml path/to/output.csv --illum --illum-directory <illum-directory> --plate-id <plate-id> --illum-output output_with_illum.csv
```

To create the LoadData csv with illum, make sure to change the paths within the [create_loaddata_illum_csv.ipynb](create_loaddata_illum_csv.ipynb) to reflect your local machine paths before running the code below (e.g. a local path for my computer starts with `/home/jenna`).

Run this code in terminal to create the csv file:

```bash
bash create_loaddata_illum_csv.sh
```

## Step 2: Run `intersteller_wave1_analysis.cpproj` in CellProfiler

To create the sqlite files, we ran the pipeline in the CellProfiler GUI three independent times where each run had a different dilation size. 
It took approximately an hour for the dilation 25 pipeline to run, 2 hours for 50 dilation, and 4 hours for 100 dilation.
