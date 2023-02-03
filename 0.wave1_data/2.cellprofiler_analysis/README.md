# Perform CellProfiler analysis on Interstellar wave 1 data

In this module, we create a LoadData csv with the illumination correction function and perform segmentation + feature extraction using CellProfiler.

We run the [interstellar_wave1_analysis.cpproj](interstellar_wave1_analysis.cpproj) pipeline and output three sqlite files. 
Each file corresponds to a dilation size (Figure 1):

1) interstellar_wave1_dilate25 = Dilation structuring element disk with size 25 pixels (approx. half the average cell diameter)
2) interstellar_wave1_dilate50 = Dilation structuring element disk with size 50 pixels (approx. equal to the average cell diameter)
3) interstellar_wave1_dilate100 = Dilation structuring element disk with size 100 pixels (approx. double the average cell diameter)

![dilation_ex.png](figures/dilation_ex.png)

> Figure 1. CellProfiler dilation sizes and respective objects. This figure shows how the various sizes for dilation in the `DilateObjects` module impacts the nuclei in an image. The images for each dilation are split into the two objects, `Dilated Nuclei` which are the nuclei that are dilated and `Translocated Nuclei` which are the `Dilated Nuclei` with the original `Nuclei` subtracted from the object. 

We decided to test with various dilation values since we do not know how far Gasdermin-D translocates.
We will be able to assess the best dilate value during further analysis.

## Step 1: Create LoadData csv with illumination functions included

To create the LoadData csv to use in the analysis pipeline, you must use the following structure from the `pe2loaddata` repository.

> pe2loaddata --index-directory <index-directory> path/to/config.yml path/to/output.csv --illum --illum-directory <illum-directory> --plate-id <plate-id> --illum-output output_with_illum.csv

The following code is ran to create the wave1_loaddata_with_illum.csv file:

```sh
pe2loaddata --index-directory /home/jenna/Interstellar_Project/0.wave1_data/0.download_data/70117_20230118MM1_AbTest_V2__2023-01-25T16_44_54-Measurement1/Images 0.wave1_data/1.cellprofiler_ic_processing/config.yml 0.wave1_data/1.cellprofiler_ic_processing/wave1_loaddata.csv --illum --illum-directory /home/jenna/Interstellar_Project/0.wave1_data/1.cellprofiler_ic_processing/illum_directory --plate-id 70117_20230118MM1_AbTest_V2 --illum-output wave1_loaddata_with_illum.csv
```

## Step 2: Run `intersteller_wave1_analysis.cpproj` in CellProfiler

To create the sqlite files, we ran the pipeline in the CellProfiler GUI three independent times where each run had a different dilation size. 
It took approximately an hour for the dilation 25 pipeline to run, 2 hours for 50 dilation, and 4 hours for 100 dilation.
