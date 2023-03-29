# Create initial LoadData csv to calculate illumination correction function

In this module, we create a LoadData csv and CellProfiler pipeline for calculating an illumination correction function for each channel.

## pe2loaddata

To create the LoadData csv file for CellProfiler, we use a software called [pe2loaddata](https://github.com/broadinstitute/pe2loaddata/tree/220ac512bfc0c2e582d379b19411c1585272aee3). 
This will create a LoadData csv from the Phenix metadata XML file generated during data acquisition. 

Since we are using one main environment for the entire repository, there is no need to install pe2loaddata in separate environments for each module.

## Create LoadData csv and calculate IC function for each channel in CellProfiler

Run the below code in terminal to output the LoadData CSV file to use in the [interstellar_wave1_illum.cppipe](0.wave1_data/1.cellprofiler_ic_processing/interstellar_wave1_illum.cppipe) CellProfiler pipeline which outputs two functions (`.npy` files) to use in the downstream analysis pipeline.

```bash
cd 0.wave1_data/1.cellprofiler_ic_processing
conda activate interstellar_data
bash run_loaddata_and_ic.sh
```
