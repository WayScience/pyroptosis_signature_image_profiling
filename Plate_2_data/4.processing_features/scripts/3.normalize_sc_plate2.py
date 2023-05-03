#!/usr/bin/env python
# coding: utf-8

# # Normalize annotated single cells using negative control (DSMO 0.025% and DMSO 0.100%)

# ## Import libraries

# In[ ]:


import pathlib
import pandas as pd

from pycytominer import normalize
from pycytominer.cyto_utils import output


# ## Set paths and variables

# In[ ]:


# directory where parquet files are located
data_dir = pathlib.Path("./data/")

# define input path for combined annotated parquet file
annotated_file_path = str(pathlib.Path(f"{data_dir}/SHSY5Y_sc.parquet"))

# define ouput path for normalized parquet file
normalized_output_file = str(pathlib.Path(f"{data_dir}/SHSY5Y_sc_norm.parquet"))


# ## Normalize with standardize method with negative control on annotated data

# In[ ]:


# read in annotated single cell data
annotated_df = pd.read_parquet(annotated_file_path)
print("Normalizing annotated merged single cells!")

# normalize annotated data
normalized_df = normalize(
        # df with annotated raw merged single cell features
        profiles=annotated_df,
        # specify samples used as normalization reference (negative control)
        samples="Metadata_inhibitor == 'DMSO' and Metadata_inhibitor_concentration == 0.025 and Metadata_inducer1 == 'DMSO'",
        # normalization method used
        method="standardize",
)

# save df as parquet file
output(
    df=normalized_df,
    output_filename=normalized_output_file,
    output_type="parquet",
)
print(f"Single cells have been normalized for SH-SY5Y cells and saved to {pathlib.Path(normalized_output_file).name} !")


# In[ ]:


# check to see if the features have been normalized
print(normalized_df.shape)
normalized_df.head()

