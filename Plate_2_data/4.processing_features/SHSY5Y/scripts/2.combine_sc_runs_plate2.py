#!/usr/bin/env python
# coding: utf-8

# # Combine runs run parquet files into one

# ## Import libraries

# In[1]:


import pandas as pd
import pathlib

from pycytominer.cyto_utils import output


# ## Set paths

# In[2]:


# set path to parquet directory with annotated runs
annotated_dir = pathlib.Path("./data/annotated_data")

# directory where the combined parquet file is saved to
output_dir = pathlib.Path("./data/combined_data")
output_dir.mkdir(exist_ok=True)

# set path for combined run parquet file
merged_runs_path = pathlib.Path(f"{output_dir}/SHSY5Y_sc.parquet")


# In[3]:


# set paths to each individual run file after annotation
first_run_sc_path = pathlib.Path(f"{annotated_dir}/SHSY5Y_batch_1_sc.parquet")
second_run_sc_path = pathlib.Path(f"{annotated_dir}/SHSY5Y_batch_2_sc.parquet")


# ## Combine the parquet files into one

# In[4]:


# read parquet files into pandas dataframes
first_run_sc = pd.read_parquet(first_run_sc_path)
second_run_sc = pd.read_parquet(second_run_sc_path)

# concatenate dataframes and save as parquet file
SHSY5Y_run_sc = pd.concat(
    [
        first_run_sc,
        second_run_sc,
    ],
    ignore_index=True,
)
output(
    df=SHSY5Y_run_sc,
    output_filename=merged_runs_path,
    output_type="parquet",
)
print(f"The runs have been merged into one file called {merged_runs_path.name}!")


# In[5]:


# check to see if the merge function worked (should be approximately 600,000 rows)
print(SHSY5Y_run_sc.shape)
SHSY5Y_run_sc.head()

