# Perform CellProfiler analysis on Plate 2

In this module, we create a LoadData CSV with the illumination correction (IC) functions to use in the [LoadData module in CellProfiler](https://cellprofiler-manual.s3.amazonaws.com/CPmanual/LoadData.html).
We then edited this CSV to contain the correct pathing and rows (with maximum projection images).
Using CellProfiler, we perform IC, segmentation, and feature extraction to output CSVs. 
For context, we call all of these processes together as `analysis`.

We run the [interstellar_wave3_analysis.cpproj](interstellar_wave1_analysis.cpproj) pipeline and outputted one sqlite file containing all of the feature and whole image measurements. 


## Create LoadData CSV with IC functions, edit it, and perform analysis in CellProfiler

To create, edit, and calculate illumination correction for the LoadData CSV data for all images per channel in the data, run the [loaddata_edit_and_ic.ipynb](loaddata_edit_and_ic.ipynb) notebook using the code below.

```bash
conda activate interstellar_data
cd Plate_2_data/3.cellprofiler_analysis/
bash loaddata_edit_and_analysis.sh
```

To run this notebook for all maximum projection images (4,928 image sets split by cell type), it took approximately __ days in total.
