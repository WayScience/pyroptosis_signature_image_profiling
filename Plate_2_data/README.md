# Plate 2 data 

This module holds all of the analysis for data from plate 2 of the Interstellar collaboration project.

## Conditions

The data from plate 2 consist of modified Cell Painting images from a 384-well plate where we use 308 wells of the plate as to avoid problems with edge wells. 

The Cell Painting stains include (in the correct order of the channels):

1. HOECHST 33342 -> Nuclei
2. PhenoVue Fluor 488 -> Concanavalin A/Endoplasmic Reticulum (ER)
3. Alexa514 -> Gasdermin-D (Abcam) 
4. WGA555/Phalloidin568 -> PM and Glogi/Actin
5. Mito_641_narrow -> Mitochondria

We removed the RNA stain to include the Gasdermin stain due to the high signal overlap between the Mito and Gasdermin channel from as seen in the experiment from plate 1, specifically the module [1.wave2_data](Plate_1_data/1.wave2_data/).
