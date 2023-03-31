# Create and edit LoadData csv and calculate illumination correction function

In this module, we created a LoadData csv, removed rows except for those with the last z-plane and corrected paths to maximum projection images (as they have the same name as the last z-plane). We then ran a CellProfiler pipeline for calculating an illumination correction (IC) function (`.npy` file) for all images in each channel. 

As stated in the [previous module README](Plate_2_data/1.cellprofiler_quality_control/README.md), this methodology is inspired by a project from the Broad Institute and we had the guidance of [Erin Weisbart](https://github.com/ErinWeisbart).

## Step 4: Create LoadData CSV, edit it, and calculate IC function for each channel in CellProfiler

To create and edit the LoadData CSV and calculate the illumination correction function for both channels in the data, run the [loaddata_edit_and_ic.ipynb](loaddata_edit_and_ic.ipynb) note using the code below.

```bash
bash loaddata_edit_and_ic.sh
```

To run this notebook for 5 channels (4,928 image sets), it took approximately an hour.
