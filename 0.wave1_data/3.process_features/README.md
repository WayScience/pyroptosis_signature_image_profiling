# Extract single cells from Interstellar wave 1 data

In this module, we extract single cells from each of the CellProfiler .sqlite file outputs.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the merging and extraction of the Interstellar wave 1 single cell features.

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/pycytominer.cyto_utils.html#pycytominer.cyto_utils.cells.SingleCells.merge_single_cells) from the Pycytominer team.

## Extract single cell features from each dilation pipeline

Run this code in terminal to extract single cells and create csv files:

```sh
bash extract_sc_interstellar.sh
```

