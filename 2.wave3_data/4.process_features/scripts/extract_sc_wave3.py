#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd

from pycytominer import normalize, feature_select
from pycytominer.cyto_utils import cells, output


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = "../3.cellprofiler_analysis"
output_dir = "data"


# ## Set paths to sqlite files

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file = "interstellar_wave3.sqlite"
single_cell_file = f"sqlite:///{cp_dir}/analysis_output/{sql_file}"
platemap_file = "../../metadata/Interstellar_platemap.csv"

# Set path with name for outputted data
sc_output_file = pathlib.Path(f"{output_dir}/interstellar_wave3_sc.csv.gz")
sc_norm_output_file = pathlib.Path(f"{output_dir}/interstellar_wave3_sc_norm_cellprofiler.csv.gz")
sc_norm_fs_output_file = pathlib.Path(f"{output_dir}/interstellar_wave3_sc_norm_fs_cellprofiler.csv.gz")


# ## Set up names for linking columns between tables in the database file

# In[4]:


# Define custom linking columns between compartments
linking_cols = {
    "Per_Cytoplasm": {
        "Per_Cells": "Cytoplasm_Parent_Cells",
        "Per_Nuclei": "Cytoplasm_Parent_Nuclei",
    },
    "Per_Cells": {"Per_Cytoplasm": "Cells_Number_Object_Number"},
    "Per_Nuclei": {"Per_Cytoplasm": "Nuclei_Number_Object_Number"},
}


# ## Load and view platemap file

# In[5]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df.head()


# ## Set up `SingleCells` class from Pycytominer

# In[6]:


# Instantiate SingleCells class
sc = cells.SingleCells(
    sql_file=single_cell_file,
    compartments=["Per_Cells", "Per_Cytoplasm", "Per_Nuclei"],
    compartment_linking_cols=linking_cols,
    image_table_name="Per_Image",
    strata=["Image_Metadata_Well", "Image_Metadata_Plate"],
    merge_cols=["ImageNumber"],
    image_cols="ImageNumber",
    load_image_data=True
)


# ## Merge single cells 

# In[7]:


# Merge single cells across compartments
anno_kwargs = {"join_on": ["Metadata_well", "Image_Metadata_Well"]}

sc_df = sc.merge_single_cells(
    platemap=platemap_df,
    **anno_kwargs,
)

# Save level 2 data as a csv
output(sc_df, sc_output_file)

print(sc_df.shape)
sc_df.head()


# ## Normalize data by DMSO 0.1% treatment

# In[9]:


sc_df["Metadata_treatment"].unique()


# In[10]:


# Normalize single cell data and write to file
normalize_sc_df = normalize(
    sc_df,
    samples="Metadata_treatment == 'DMSO 0.1%'",
    method="standardize"
)

output(normalize_sc_df, sc_norm_output_file)

print(normalize_sc_df.shape)
normalize_sc_df.head()


# ## Feature selection

# In[11]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

feature_select_norm_sc_df = feature_select(
    normalize_sc_df,
    operation=feature_select_ops
)

output(feature_select_norm_sc_df, sc_norm_fs_output_file)

print(feature_select_norm_sc_df.shape)
feature_select_norm_sc_df.head()


# ## View info of the dataframe for single cell data

# In[12]:


sc_df.info()


# ---
# 
# ### Visualize basic count statistics

# In[13]:


sc_df.Metadata_treatment.value_counts()


# In[14]:


pd.crosstab(sc_df.Metadata_treatment, sc_df.Metadata_Well)

