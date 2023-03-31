# Create LoadData CSV and create maximum projection images 

In this module, we create a LoadData csv and run a CellProfiler pipeline that performs maximum projection on the images and saves them into a new folder.
This pipeline names the outputted max projected images as the last z-plane.
In our case we have 4 z-planes (p01-p04), which means that the outputted maximum projected images will be named the same as the raw images from the p04 z-plane.

This methodology is inspired by [a project from the Broad Institute](https://github.com/broadinstitute/imaging-platform-pipelines/tree/455d8ffa2a0a6cb7341868139f3f1719b9d5ea2c/cellpainting_ipsc_20x_phenix_with_bf_bin1_cp4).
We discussed the process with Erin Weisbart in [an image.sc post](https://forum.image.sc/t/performing-max-projection-using-phenix-data-based-on-broad-institute-project/77262).

## pe2loaddata

For this project, we use a software called [pe2loaddata](https://github.com/broadinstitute/pe2loaddata/tree/220ac512bfc0c2e582d379b19411c1585272aee3). 
This software is specific to images acquired from a Phenix microscrope.
The main function of this software is to create a LoadData csv from the Phenix metadata XML file generated from data acquisition for CellProfiler to use to load in the images to the pipeline. 

## Create the LoadData CSV and create max projection images

To create LoadData CSV and run CellProfiler to output the maximum projection images for each channel and site, run the [loaddata_and_maxproj.ipynb](loaddata_and_maxproj.ipynb) notebook using the code block below:

```bash
bash loaddata_and_maxproj.sh
```

To run this pipeline, it took approximately 8 hours.
