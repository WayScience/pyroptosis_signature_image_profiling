#!/usr/bin/env python
# coding: utf-8

# # Combine runs run parquet files into one

# ## Import libraries

# In[1]:


import pandas as pd
import pathlib
import gc

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
first_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_1_sc.parquet")
second_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_2_sc.parquet")
third_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_3_sc.parquet")
fourth_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_4_sc.parquet")
fifth_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_5_sc.parquet")
sixth_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_6_sc.parquet")
seventh_run_sc_path = pathlib.Path(f"{annotated_dir}/batch_7_sc.parquet")


# ## Combine the parquet files into one

# In[3]:


# read parquet files into pandas dataframes
print("Reading parquet files into pandas dataframes...")
first_run_sc = pd.read_parquet(first_run_sc_path)
second_run_sc = pd.read_parquet(second_run_sc_path)
third_run_sc = pd.read_parquet(third_run_sc_path)
fourth_run_sc = pd.read_parquet(fourth_run_sc_path)
fifth_run_sc = pd.read_parquet(fifth_run_sc_path)
sixth_run_sc = pd.read_parquet(sixth_run_sc_path)
seventh_run_sc = pd.read_parquet(seventh_run_sc_path)

print("Merging runs into one dataframe...")
# concatenate dataframes and save as parquet file
print("Concatenating dataframes 1 and 2...")
PBMC_run_sc = pd.concat(
    [
        first_run_sc,
        second_run_sc
    ],
    ignore_index=True,
)
del first_run_sc, second_run_sc
gc.collect()

print("Concatenating dataframe 3")

PBMC_run_sc = pd.concat(
    [
    PBMC_run_sc,
    third_run_sc,
    ],
    ignore_index=True,
)
del third_run_sc
gc.collect()

print("Concatenating dataframe 4")
PBMC_run_sc = pd.concat(
    [
    PBMC_run_sc,
    fourth_run_sc,
    ],
    ignore_index=True,
)
del fourth_run_sc
gc.collect()

print("Concatenating dataframe 5")
PBMC_run_sc = pd.concat(
    [
    PBMC_run_sc,
    fifth_run_sc,
    ],
    ignore_index=True,
)
del fifth_run_sc
gc.collect()

print("Concatenating dataframe 6")
PBMC_run_sc = pd.concat(
    [
    PBMC_run_sc,
    sixth_run_sc,
    ],
    ignore_index=True,
)
del sixth_run_sc
gc.collect()

print("Concatenating dataframe 7")
PBMC_run_sc = pd.concat(
    [
    PBMC_run_sc,
    seventh_run_sc,
    ],
    ignore_index=True,
)
del seventh_run_sc
gc.collect()

print("Saving merged runs to parquet file...")

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

