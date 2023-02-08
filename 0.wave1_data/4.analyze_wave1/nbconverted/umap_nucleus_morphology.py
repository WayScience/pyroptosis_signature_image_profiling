#!/usr/bin/env python
# coding: utf-8

# ## Nucleus morphology UMAP

# In[1]:


import pathlib
import pandas as pd

from pycytominer import normalize, feature_select
from pycytominer.cyto_utils import infer_cp_features

import umap


# In[2]:


# Focus on gasdermin cols
gasdermin_cols = [
    "TranslocatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD",
    "DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD",
    "TranslocatedNuclei_Neighbors_NumberOfNeighbors_Expanded"
]


# In[3]:


# Load single cell profiles
feature_dir = pathlib.Path("..", "3.process_features", "data")

# This determines the file
file_prefix = "interstellar_wave1_dilate"
file_suffix = "_sc.csv.gz"
dilation_factor = 50

cp_file = pathlib.Path(feature_dir, f"{file_prefix}{dilation_factor}{file_suffix}")
output_umap_file = pathlib.Path("results", f"umap_embeddings_dilation{dilation_factor}.csv.gz")

# Load data
cp_df = pd.read_csv(cp_file, low_memory=False)

# Remove outliers
cp_df = (
    cp_df
    .query("DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD < 100")
    .reset_index(drop=True)
)

print(cp_df.shape)
cp_df.head()


# In[4]:


# Process only the nucleus features through the pipeline
# Remove all information from gasdermin channel
nucleus_features = infer_cp_features(cp_df, compartments="Nuclei")
nucleus_features = [x for x in nucleus_features if "Gasdermin" not in x]

metadata_features = infer_cp_features(cp_df, metadata=True)

cp_norm_fs_df = normalize(
    profiles=cp_df,
    features=nucleus_features,
    method="standardize"
)

ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
    "drop_na_columns"
]
cp_norm_fs_df = feature_select(
    profiles=cp_norm_fs_df,
    features=nucleus_features,
    operation=ops,
    na_cutoff=0
)

print(cp_norm_fs_df.shape)
cp_norm_fs_df.head()


# In[5]:


# Fit UMAP
cp_feature_df = cp_norm_fs_df.drop(metadata_features, axis="columns")

umap_fit = umap.UMAP(random_state=42, n_components=2)

embeddings_df = pd.DataFrame(
    umap_fit.fit_transform(cp_feature_df), columns=["UMAP0", "UMAP1"]
)

embeddings_df = pd.concat([
    cp_norm_fs_df.loc[:, metadata_features],
    embeddings_df,
    cp_df.loc[:, gasdermin_cols]
], axis="columns")

dose_recode = {
    "0": "low",
    "0.1µM": "low",
    "1µM": "low",
    "1µg/ml + 1µM": "low",
    "2.5µM": "high",
    "10µM": "high",
    "1µg/ml + 10µM": "high"
}
embeddings_df = embeddings_df.assign(
    Metadata_dose_recode=embeddings_df.Metadata_dose.replace(dose_recode)
)

# Output file
embeddings_df.to_csv(output_umap_file, index=False)

print(embeddings_df.shape)
embeddings_df.head()

