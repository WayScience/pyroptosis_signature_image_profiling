# Perform CellProfiler analysis on Interstellar wave 1 data

In this module, we create a LoadData csv with the illumination correction (IC) function to use in the [LoadData module in CellProfiler](https://cellprofiler-manual.s3.amazonaws.com/CPmanual/LoadData.html) and perform segmentation + feature extraction using CellProfiler.

We run the [interstellar_wave1_analysis.cpproj](interstellar_wave1_analysis.cpproj) pipeline and output three sqlite files. 
Each file corresponds to a dilation size (Figure 1):

1) interstellar_wave1_dilate25 = Dilation structuring element disk with size 25 pixels (approx. half the average cell diameter)
2) interstellar_wave1_dilate50 = Dilation structuring element disk with size 50 pixels (approx. equal to the average cell diameter)
3) interstellar_wave1_dilate75 = Dilation structuring element disk with size 75 pixels (approx. double the average cell diameter). This was changed from 100 originally since it was using a lot of computational power.

![dilation_ex.png](figures/dilation_ex.png)

> Figure 1. Example of CellProfiler dilation sizes and respective objects. 
> This figure shows how the various sizes for dilation in the `DilateObjects` module impacts the nuclei in an image. 
> The images for each dilation are split into the two objects, `Dilated Nuclei` which are the nuclei that are dilated and `Translocated Nuclei` which are the `Dilated Nuclei` with the original `Nuclei` subtracted from the object. 

We decided to test with various dilation values since we do not know how far Gasdermin-D translocates to assess if Gasdermin-D is being measured.

## Create LoadData csv with IC functions and extract features with `loaddata_and_analysis.ipynb` notebook

To create the sqlite files for each dilation, run the [loaddata_and_analysis.ipynb](0.wave1_data/2.cellprofiler_analysis/loaddata_and_analysis.ipynb) notebook.
It took approximately an hour for the dilation 25 pipeline to run, 2 hours for 50 dilation, and 4 hours for 100 dilation.

Run this code in terminal to create the csv files:

```bash
bash loaddata_and_analysis.sh
```
