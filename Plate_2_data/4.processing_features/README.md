# Extract single cells and image features from CellProfiler output + normalize and feature select single cell features

In this module, we extract single cell data from the CellProfiler .sqlite file outputs, convert to parquet files, and perform annotation to add platemap metadata to each run, merge the runs into one parquet file, normalize features, and perform feature selection on the normalized features.

## CytoTable

We use [CytoTable](https://github.com/cytomining/CytoTable/tree/main) to extract single cells and merge them from the SQLite outputs and convert into paraquet files.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the annotation, normalization, and feature selection of the merged single cell data (parquet files from CytoTable).

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/) from the Pycytominer team.

## Extract and process single cell features from CellProfiler

Using the code below, execute the `sh` file and merge single cells to use for annotation, normalization, and feature selection and extract image features.

There are two different `sh` files for each cell type.
For SHSY5Y cells run the following code:

```bash
source processing_features_plate2_SHSY5Y.sh
```

For PBMCs run the following code:

```bash
source processing_features_plate2_PBMCs.sh
```
Note that all notebook code is not run, but rather run via converted scripts.
