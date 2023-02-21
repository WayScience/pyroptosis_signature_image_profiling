# Extract single cells from Interstellar wave 3 data

In this module, we extract single cell and image feature data from the CellProfiler .sqlite file outputs.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the annotation and output of the Interstellar wave 2 image features.

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/pycytominer.cyto_utils.html#pycytominer.cyto_utils.cells.SingleCells.merge_single_cells) from the Pycytominer team.

## Step 1: Create conda environment

If you have not already made the `3.process_features_interstellar` environment from wave 1, then make sure you are in the `0.wave1_data/3.process_features` directory and perform the below command to create the environment.

```sh
# Run this command in terminal to create the conda environment
conda env create -f 3.process_features.yml
```

## Step 2: Extract image features 

Run this code in terminal to extract image features and create csv file:

```sh
bash extract_image_features_interstellar.sh
```
