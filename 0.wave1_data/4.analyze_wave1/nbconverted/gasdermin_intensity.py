#!/usr/bin/env python
# coding: utf-8

# # Determine the distribution of Gasdermin intensity
# 
# - Across treatments per dilation experiment

# In[1]:


import pathlib
import pandas as pd
import plotnine as gg


# In[2]:


# Load single cell profiles
feature_dir = pathlib.Path("..", "3.process_features", "data")

# This determines the file
file_prefix = "interstellar_wave1_dilate"
file_suffix = "_sc.csv.gz"
dilation_factors = [25, 50, 100]

# Determine output figure directory
figure_dir = "figures"


# In[3]:


# Create three figures per dilation experiment
for dilation_factor in dilation_factors:
    cp_file = pathlib.Path(feature_dir, f"{file_prefix}{dilation_factor}{file_suffix}")

    # Load data
    cp_df = pd.read_csv(cp_file, low_memory=False)

    # Ensure dose is a string and recode to high/low
    cp_df.Metadata_dose = cp_df.Metadata_dose.astype(str)

    dose_recode = {
        "0": "low",
        "0.1µM": "low",
        "1µM": "low",
        "1µg/ml + 1µM": "low",
        "2.5µM": "high",
        "10µM": "high",
        "1µg/ml + 10µM": "high"
    }
    cp_df = cp_df.assign(Metadata_dose_recode=cp_df.Metadata_dose.replace(dose_recode))

    # Recode number of neighbors
    median_neighbors = (
        cp_df.TranslocatedNuclei_Neighbors_NumberOfNeighbors_Expanded.median()
    )

    cp_df = cp_df.assign(Metadata_neighbor_recode="high")
    (
        cp_df
        .loc[
            cp_df.TranslocatedNuclei_Neighbors_NumberOfNeighbors_Expanded < median_neighbors,
            "Metadata_neighbor_recode"
        ]
    ) = "low"

    # Create variable for translocation ratio
    cp_df = (
        cp_df
        .assign(
            translocation_ratio = (
                cp_df.TranslocatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD / 
                cp_df.DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD
            )
        )
    )

    # Remove outliers
    cp_df = cp_df.query("DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD < 100")

    # Plot translocation of nuclei
    translocated_gg = (
        gg.ggplot(
            cp_df,
            gg.aes(
                x = "TranslocatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD"
            )
        )
        + gg.geom_density(gg.aes(color="Metadata_treatment", linetype="Metadata_dose_recode"))
        + gg.facet_wrap("~Metadata_neighbor_recode", labeller=lambda x: f"Neighbors: {x}")
        + gg.theme_bw()
        + gg.ggtitle(f"Dilation factor: {dilation_factor}")
    )

    output_fig = pathlib.Path(figure_dir, f"translocated_gasdermin_dilation{dilation_factor}.png")
    translocated_gg.save(output_fig, dpi=500, width=6, height=4)

    # Plot total gasdermin
    total_gasdermin_gg = (
        gg.ggplot(
            cp_df,
            gg.aes(
                x = "DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD"
            )
        )
        + gg.geom_density(gg.aes(color="Metadata_treatment", linetype="Metadata_dose_recode"))
        + gg.facet_wrap("~Metadata_neighbor_recode", labeller=lambda x: f"Neighbors: {x}")
        + gg.theme_bw()
        + gg.ggtitle(f"Dilation factor: {dilation_factor}")
    )
    output_fig = pathlib.Path(figure_dir, f"total_gasdermin_dilation{dilation_factor}.png")
    total_gasdermin_gg.save(output_fig, dpi=500, width=6, height=4)

    # Plot gasdermin ratio
    gasdermin_ratio_gg = (
        gg.ggplot(cp_df, gg.aes(x="translocation_ratio"))
        + gg.geom_density(gg.aes(color="Metadata_treatment", linetype="Metadata_dose_recode"))
        + gg.facet_wrap("~Metadata_neighbor_recode", labeller=lambda x: f"Neighbors: {x}")
        + gg.theme_bw()
        + gg.ggtitle(f"Dilation factor: {dilation_factor}")
    )
    output_fig = pathlib.Path(figure_dir, f"gasdermin_ratio_dilation{dilation_factor}.png")
    gasdermin_ratio_gg.save(output_fig, dpi=500, width=6, height=4)

