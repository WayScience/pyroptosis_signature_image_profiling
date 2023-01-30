# Perform Illumination Correction on Intersteelar wave 1 data

In this module, we demonstrate the method we used to perform illumination correction on the first wave of data.

## BaSiCPy Illumination Correction

We use a software called [BaSiCPy](https://github.com/peng-lab/BaSiCPy/tree/main) to perform the illumination correction of the data per channel. We specifically are using the PyBaSiC version due to the ability to use on static images (currently [an issue](https://github.com/peng-lab/BaSiCPy/issues/120) in the repo).

Illumination correction is an important step in cell image analysis pipelines as it helps with downstream processes like segmentation (more accuracy in segmenting shape and identifying objects to segment) and feature extraction (accurate measurements in intensity, texture, etc.).

## Step 1: Create Conda Environment

```bash
# Run this command to create the conda environment
cd 0.wave1_data/1.preprocessing_data
conda env create -f 1.preprocessing_data.yml
```

Activate the environment prior to the next steps

```bash
# Run this command to create the conda environment
conda activate 1.preprocessing-interstellar
```
