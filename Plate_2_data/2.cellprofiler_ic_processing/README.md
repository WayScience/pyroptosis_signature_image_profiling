# Create and edit LoadData csv and calculate illumination correction function

In this module, we created a LoadData CSV file for loading in maximum projection images to CellProfiler. 
To do this, we created a LoadData CSV for all the raw images and removed all rows except for rows with the last z-plane and changed the paths to maximum projection images (as the max projection images have the same name as the raw images with the last z-plane). 
We then ran a CellProfiler pipeline for calculating an illumination correction (IC) function (`.npy` file) for all images in each channel. 

As stated in the [previous module README](Plate_2_data/1.cellprofiler_quality_control/README.md), this methodology is inspired by a project from the Broad Institute and we had the guidance of [Erin Weisbart](https://github.com/ErinWeisbart).

## Create LoadData CSV, edit it, and calculate IC function for each channel in CellProfiler

To create, edit, and calculate illumination correction for the LoadData CSV data for all images per channel in the data, run the [loaddata_edit_and_ic.ipynb](loaddata_edit_and_ic.ipynb) notebook using the code below.

```bash
bash loaddata_edit_and_ic.sh
```

To run this notebook for 5 channels (4,928 image sets), it took approximately an hour.
