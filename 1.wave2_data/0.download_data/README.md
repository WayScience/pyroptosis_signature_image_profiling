# Download data for wave 2: ASC Bleedthrough Assessment

In this module, we will provide the instructions for downloading the wave 2 data, which is a modified Cell Painting assay consisting of 4 channels totalling 4,608 images images. 
There are 2 conditions within this wave:

For **condition 7**:
- HOECHST 33342 -> Nuclei
- Alexa 488 -> ASC
- Mito_641_narrow -> Mitochondria
- Alexa 700_narrow -> absolute spill over form mito 641

For **condition 8**:
- HOECHST 33342 -> Nuclei
- Alexa 488 -> nothing/autofluorescence 
- Mito_641_narrow -> Mitochondria
- Alexa 700_narrow -> ASC

![wave2_platemap](figures/wave2_platemap_fig.png)

Since Alexa 488 and Alexa 700_narrow are staining for different things based on the condition, the metadata for these two channels will include both conditions 7 and 8 (e.g. Alexa 488 = ASC_nothing). 
Since the condition is not included in the metadata `Index.idx.xml` file, it will be added to the final extracted single cell csv file manually.

**Note:** The original name of the plate (or collect of wells in a plate) had to be changed due to the inclusion of spaces in the name causing issues downstream.
