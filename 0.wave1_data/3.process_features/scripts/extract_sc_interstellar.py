#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd

import sys
sys.path.append("../../utils/")
import sc_extraction_utils as sc_util

from pycytominer.cyto_utils import cells, output


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = "../2.cellprofiler_analysis"
output_dir = "data"
platemap_file = pathlib.Path("../../metadata/Interstellar_platemap.csv")

# dictionary with variables for each dilation
dilation_info_dictionary = {
    "dilation_25": {
        "sql_file": "dilate25.sqlite",
        "sc_output_file" : pathlib.Path(f"{output_dir}/dilate25_sc.csv.gz")
    },
    "dilation_50": {
        "sql_file": "dilate50.sqlite",
        "sc_output_file" : pathlib.Path(f"{output_dir}/dilate50_sc.csv.gz")
    },
    "dilation_75": {
        "sql_file": "dilate75.sqlite",
        "sc_output_file" : pathlib.Path(f"{output_dir}/dilate75_sc.csv.gz")
    },
}


# In[3]:


# Define custom linking columns between compartments
linking_cols = {
    "Per_TranslocatedNuclei": {
        "Per_DilatedNuclei": "TranslocatedNuclei_Parent_DilatedNuclei",
        "Per_Nuclei": "TranslocatedNuclei_Parent_Nuclei",
    },
    "Per_DilatedNuclei": {"Per_TranslocatedNuclei": "DilatedNuclei_Number_Object_Number"},
    "Per_Nuclei": {"Per_TranslocatedNuclei": "Nuclei_Number_Object_Number"},
}


# In[4]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df.head()


# In[5]:


for dilation, info in dilation_info_dictionary.items():
    # set the parameters for the function as variables based on the dilation dictionary info
    method_name = dilation
    sql_file = info["sql_file"]
    single_cell_file =  f"sqlite:///{cp_dir}/analysis_output/{sql_file}"

    # run CP analysis for each dilation
    sc_util.extract_single_cells(
        single_cell_file=single_cell_file,
        linking_cols=linking_cols,
        platemap_df=platemap_df,
        output_folder=output_dir,
        method_name=method_name,
    )

