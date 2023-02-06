#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd

import pycytominer
from pycytominer.cyto_utils import cells, output


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = "../2.cellprofiler_analysis"
output_dir = "data"


# ## Set paths to sqlite files

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file = "interstellar_wave1_dilate50.sqlite"
single_cell_file = f"sqlite:///{cp_dir}/analysis_output/{sql_file}"
platemap_file = f"{cp_dir}/metadata/Interstellar_wave1_platemap.csv"

# Set path with name for outputted data
sc_output_file = pathlib.Path(f"{output_dir}/interstellar_wave1_dilate50_sc.csv.gz")


# ## Set up names for linking columns between tables in the database file

# In[4]:


# Define custom linking columns between compartments
linking_cols = {
    "Per_TranslocatedNuclei": {
        "Per_DilatedNuclei": "TranslocatedNuclei_Parent_DilatedNuclei",
        "Per_Nuclei": "TranslocatedNuclei_Parent_Nuclei",
    },
    "Per_DilatedNuclei": {"Per_TranslocatedNuclei": "DilatedNuclei_Number_Object_Number"},
    "Per_Nuclei": {"Per_TranslocatedNuclei": "Nuclei_Number_Object_Number"},
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
    compartments=["Per_DilatedNuclei", "Per_TranslocatedNuclei", "Per_Nuclei"],
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


# ---
# 
# ### Visualize basic count statistics

# In[8]:


sc_df.Metadata_treatment.value_counts()


# In[9]:


pd.crosstab(sc_df.Metadata_treatment, sc_df.Metadata_Well)

