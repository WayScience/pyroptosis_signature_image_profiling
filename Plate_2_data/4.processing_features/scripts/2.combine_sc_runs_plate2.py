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
merged_runs_path = pathlib.Path(f"{output_dir}/PBMC_sc.parquet")


# In[ ]:


# set paths to each individual run file after annotation
first_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_1.parquet")
second_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_2.parquet")
third_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_3.parquet")
fourth_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_4.parquet")
fifth_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_5.parquet")
sixth_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_6.parquet")
seventh_run_sc_path = pathlib.Path(f"{annotated_dir}/PBMC_batch_7.parquet")


# ## Combine the parquet files into one

# In[3]:


# read parquet files into pandas dataframes
first_run_sc = pd.read_parquet(first_run_sc_path)
second_run_sc = pd.read_parquet(second_run_sc_path)
third_run_sc = pd.read_parquet(third_run_sc_path)
fourth_run_sc = pd.read_parquet(fourth_run_sc_path)
fifth_run_sc = pd.read_parquet(fifth_run_sc_path)
sixth_run_sc = pd.read_parquet(sixth_run_sc_path)
seventh_run_sc = pd.read_parquet(seventh_run_sc_path)

# concatenate dataframes and save as parquet file
PBMC_run_sc = pd.concat(
    [
        first_run_sc,
        second_run_sc,
        third_run_sc,
        fourth_run_sc,
        fifth_run_sc,
        sixth_run_sc,
        seventh_run_sc,
    ],
    ignore_index=True,
)
output(
    df=PBMC_run_sc,
    output_filename=merged_runs_path,
    output_type="parquet",
)
print(f"The runs have been merged into one file called {merged_runs_path.name}!")


# In[4]:


# check to see if the merge function worked (should be approximately 600,000 rows)
print(PBMC_run_sc.shape)
PBMC_run_sc.head()
