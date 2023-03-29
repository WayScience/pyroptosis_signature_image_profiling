# Pyroptosis signature project 

This repository contains the pipelines used to extract single cell morphology features (and/or image features) from different plates. 
These plates can be broken down into "waves" of data for the Interstellar collaboration project.
"Waves" in the context of this repository means different parts of a 384 well plate that contain different stains, conditions, etc.
To view the analysis of the morpoholgy features, please visit the [pyroptosis_signature_data_analysis repository](https://github.com/WayScience/pyroptosis_signature_data_analysis).

## Background

[Pyroptosis](https://www.nature.com/articles/nrmicro2070) is inflammatory cell death which occurs in response to pathogens and damage-associated molecular patterns.

## Aims

1. Describe an organelle morphology signature that predicts pyroptosis.
2. Reveal the organelle interaction landscape during pyroptosis at an ultrastructural level (electron microscopy).

## Platemap for plate 1

![platemap_plate1](figures/platemap_plate1.png)

> There are three waves of data currently analyzed for the [Plate 1 data](Plate_1_data/). On this plate, it is broken down into section where there are either different treatments, different stains, or both. The breakdown of each of the waves can be found in [the README of the Plate_1_data module](Plate_1_data/README.md).

## Create conda environment for the whole repository

All plates and waves will be using the same conda environment to run notebooks/python files.

To create the conda environment, run the code block below:

```bash
conda env create -f interstellar_data_env.yml
```

To activate the environment, run the code block below:

```bash
conda activate interstellar_data
```
