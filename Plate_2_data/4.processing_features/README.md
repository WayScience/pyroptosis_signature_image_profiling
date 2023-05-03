# Extract single cells from CellProfiler output + normalize and feature select

In this module, we extract single cell data from the CellProfiler .sqlite file outputs, convert to parquet files, and perform annotation to add platemap metadata to each run, merge the runs into one parquet file, normalize features, and perform feature selection on the normalized features.

## CytoTable

We use [CytoTable](https://github.com/cytomining/CytoTable/tree/main) to extract single cells and merge them from the SQLite outputs and convert into paraquet files.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the annotation, normalization, and feature selection of the merged single cell data (parquet files from CytoTable).

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/) from the Pycytominer team.

## Extract and process single cell features from CellProfiler

Using the code below, execute the `sh` file and merge single cells to use for annotation, normalization, and feature selection.

```bash
source processing_features_plate2.sh
```
