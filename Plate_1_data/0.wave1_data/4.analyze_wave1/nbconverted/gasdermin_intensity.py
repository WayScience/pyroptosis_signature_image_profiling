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

# Determine output directories
figure_dir = "figures"
results_dir = "results"


# In[3]:


# Logic for recode dose information
dose_recode = {
    # ATP
    "0.1mM": "low",
    "1mM": "high",
    
    # DMSO and Media Only
    "0": "low",
    
    # Disulfiram
    "0.1µM": "low",
    "2.5µM": "high",
    
    # Flagellin
    "0.1µg/ml": "low",
    "1µg/ml": "high",
    
    # H2O2
    "50µM": "low",
    "500µM": "high",
    
    # LPS
    "10µg/ml": "high",  # Note, LPS low is the same as Flagellin high
    
    # LPS + Nigericin
    "1µg/ml + 1µM": "low",
    "1µg/ml + 10µM": "high",
    
    # Thapsigargin
    "1µM": "low",
    "10µM": "high",
}


# In[4]:


# Create three figures per dilation experiment
for dilation_factor in dilation_factors:
    cp_file = pathlib.Path(feature_dir, f"{file_prefix}{dilation_factor}{file_suffix}")

    # Load data
    cp_df = pd.read_csv(cp_file, low_memory=False)

    # Ensure dose is a string and recode to high/low
    cp_df.Metadata_dose = cp_df.Metadata_dose.astype(str)
    cp_df = cp_df.assign(Metadata_dose_recode=cp_df.Metadata_dose.replace(dose_recode))

    # Note, LPS has the same dose low as flagellin high, adjust this
    cp_df.loc[
        (
            (cp_df.Metadata_treatment == "LPS") &
            (cp_df.Metadata_dose == "1µg/ml")
        ), "Metadata_dose_recode"
    ] = "low"
    
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
    
    # Determine cell count per well
    cell_count_df = (
        cp_df
        .groupby(["Metadata_treatment", "Metadata_dose_recode", "Metadata_Well"])
        ["Metadata_row"]
        .count()
        .reset_index()
        .rename(columns={"Metadata_row": "Metadata_cell_count"})
    )

    # Build a replicate_id column unique per treatment and well
    cell_count_df = (
        pd.concat(
            [
                cell_count_df, (
                    cell_count_df
                    .groupby(["Metadata_treatment", "Metadata_dose_recode"])
                    .cumcount()
                )
            ], axis=1
        )
        .rename(columns={0: "Metadata_replicate_id"})
    )

    cell_count_df.Metadata_replicate_id = "replicate_" + cell_count_df.Metadata_replicate_id.astype(str)

    # Save cell count file
    cell_count_file = pathlib.Path(results_dir, f"cell_count_dilation{dilation_factor}.tsv")
    cell_count_df.to_csv(cell_count_file, sep="\t", index=False)

    # Merge cell count data back to cp_df
    cp_df = cp_df.merge(
        cell_count_df,
        on=["Metadata_Well", "Metadata_treatment", "Metadata_dose_recode"]
    )
    
    # Plot translocation of nuclei
    translocated_gg = (
        gg.ggplot(
            cp_df,
            gg.aes(
                x = "TranslocatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD"
            )
        )
        + gg.geom_density(gg.aes(color="Metadata_treatment", linetype="Metadata_dose_recode"))
        + gg.facet_grid(
            "Metadata_replicate_id~Metadata_neighbor_recode",
            labeller=gg.labeller(cols=lambda x: f"Neighbors: {x}")
        )
        + gg.theme_bw()
        + gg.ggtitle(f"Dilation factor: {dilation_factor}")
    )

    output_fig = pathlib.Path(figure_dir, f"translocated_gasdermin_dilation{dilation_factor}.png")
    translocated_gg.save(output_fig, dpi=500, width=6, height=6)

    # Plot total gasdermin
    total_gasdermin_gg = (
        gg.ggplot(
            cp_df,
            gg.aes(
                x = "DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD"
            )
        )
        + gg.geom_density(gg.aes(color="Metadata_treatment", linetype="Metadata_dose_recode"))
        + gg.facet_grid(
            "Metadata_replicate_id~Metadata_neighbor_recode",
            labeller=gg.labeller(cols=lambda x: f"Neighbors: {x}")
        )
        + gg.theme_bw()
        + gg.ggtitle(f"Dilation factor: {dilation_factor}")
    )
    output_fig = pathlib.Path(figure_dir, f"total_gasdermin_dilation{dilation_factor}.png")
    total_gasdermin_gg.save(output_fig, dpi=500, width=6, height=6)

    # Plot gasdermin ratio
    gasdermin_ratio_gg = (
        gg.ggplot(cp_df, gg.aes(x="translocation_ratio"))
        + gg.geom_density(gg.aes(color="Metadata_treatment", linetype="Metadata_dose_recode"))
        + gg.facet_grid(
            "Metadata_replicate_id~Metadata_neighbor_recode",
            labeller=gg.labeller(cols=lambda x: f"Neighbors: {x}")
        )
        + gg.theme_bw()
        + gg.ggtitle(f"Dilation factor: {dilation_factor}")
    )
    output_fig = pathlib.Path(figure_dir, f"gasdermin_ratio_dilation{dilation_factor}.png")
    gasdermin_ratio_gg.save(output_fig, dpi=500, width=6, height=6)

