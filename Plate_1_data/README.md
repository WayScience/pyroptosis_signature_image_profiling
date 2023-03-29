# Plate 1 data 

This module holds all of the analysis for the waves of data from plate 1 of the Interstellar collaboration project.

## The waves for the Interstellar plate 1

Currently, there are three waves of data analyzed coming from [plate 1](Plate_1_data/):

| Module | Wave title | Description |
| :---- | :----- | :---------- |
| [0.wave1_data](Plate_1_data/0.wave1_data/) | Nuclei Dilaion Optimization | Using the part of the plate with two channels, Hochest and Gasdermin-D antibody, we perform a CellProfiler pipeline with various nuclei dilation to assess which dilation would allow us to identify the Gasdermin-D around each nuclei when going through pyroptosis. |
| [1.wave2_data](Plate_1_data/1.wave2_data/) | ASC Bleedthrough Assessment | Using images from two different conditions with four channels, we use CellProfiler to take measurements (including colocalization, intensity, etc.) to assess the amount of bleedthrough in the ASC channel from the Mito channel (deep red). |
| [2.wave3_data](Plate_1_data/2.wave3_data/) | Cell Painting Assay + Gasdermin-D Channel | A traditional image-based cell analysis pipeline from CellProfiler is used to extract single cell morphology readouts from SHSY-5Y cells. |