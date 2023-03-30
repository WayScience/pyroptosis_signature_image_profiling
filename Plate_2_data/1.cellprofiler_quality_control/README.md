# Create LoadData CSV and create maximum projection images 

In this module, we create a LoadData csv and run a CellProfiler pipeline that performs maximum projection on the images and saves them into a new folder.
This pipeline names the outputted max projected images as the last z-plane.
In our case we have 4 z-planes (p01-p03) so our images contain the last z-plane p04.

## pe2loaddata

To create the LoadData csv file for CellProfiler, we use a software called [pe2loaddata](https://github.com/broadinstitute/pe2loaddata/tree/220ac512bfc0c2e582d379b19411c1585272aee3). 
This will create a LoadData csv from the Phenix metadata XML file generated from data acquisition. 

## Create the LoadData CSV and create max projection images

To create LoadData CSV and run CellProfiler to output the maximum projection images for each channel and site, run the [loaddata_and_maxproj.ipynb](loaddata_and_maxproj.ipynb) notebook using the code block below:

```bash
bash loaddata_and_maxproj.sh
```

To run this pipeline, it took approximately 8 hours.
