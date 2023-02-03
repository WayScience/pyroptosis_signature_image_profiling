# Extract single cells from Interstellar wave 1 data

In this module, we extract single cells from each of the CellProfiler .sqlite file outputs.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the merging and extraction of the Interstellar wave 1 single cell features.

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/pycytominer.cyto_utils.html#pycytominer.cyto_utils.cells.SingleCells.merge_single_cells) from the Pycytominer team.

## Step 1: Create conda environment

Make sure you are in the `0.wave1_data/3.process_features` directory before performing the below command.

```sh
# Run this command in terminal to create the conda environment
conda env create -f 3.process_features.yml
```


