"""
This file contains functions to create different LoadData csvs for specific CellProfiler pipelines
and to edit these outputted csvs.
"""


import os
import subprocess
import pathlib
import pandas as pd


def create_loaddata_csv(
    index_directory: pathlib.Path,
    config_path: pathlib.Path,
    path_to_output: pathlib.Path,
):
    """
    Create LoadData csv for CellProfiler (used for illum or zproj pipelines)

    Parameters
    ----------
    index_directory : pathlib.Path
        path to the `Index.idx.xml` file for the plate (normally located in the /Images folder)
    config_path : pathlib.Path
        path to the `config.yml' file for pe2loaddata to process the csv
    path_to_output : pathlib.Path
        path to the `wave1_loaddata.csv' file used for generating the illumination correction functions for each channel
    """
    command = [
        "pe2loaddata",
        "--index-directory",
        str(index_directory),
        str(config_path),
        str(path_to_output),
    ]
    subprocess.run(command, check=True)
    print(f"{path_to_output.name} is created!")


def create_loaddata_illum_csv(
    index_directory: pathlib.Path,
    config_path: pathlib.Path,
    path_to_output: pathlib.Path,
    illum_directory: pathlib.Path,
    plate_id: str,
    illum_output_path: pathlib.Path,
):
    """
    Create LoadData csv with illum correction functions for CellProfiler (used for analysis pipelines)

    Parameters
    ----------
    index_directory : pathlib.Path
        path to the `Index.idx.xml` file for the plate (normally located in the /Images folder)
    config_path : pathlib.Path
        path to the `config.yml' file for pe2loaddata to process the csv
    path_to_output : pathlib.Path
        path to the `wave1_loaddata.csv' file used for generating the illumination correction functions for each channel
    illum_directory : pathlib.Path
        path to folder where the illumination correction functions (.npy files) are located
    plate_id : str
        string of the name of the plate to create the csv
    illum_output_path : pathlib.Path
        path to where the new csv will be created along with the name (e.g. path/to/wave1_loaddata_with_illum.csv)
    """
    command = [
        "pe2loaddata",
        "--index-directory",
        str(index_directory),
        str(config_path),
        str(path_to_output),
        "--illum",
        "--illum-directory",
        str(illum_directory),
        "--plate-id",
        plate_id,
        "--illum-output",
        str(illum_output_path),
    ]
    subprocess.run(command, check=True)
    print(f"{illum_output_path.name} is created!")

    # remove the LoadData CSV that is created without the illum functions as it is not needed
    os.remove(path_to_output)
    print(f"The {path_to_output.name} CSV file has been removed as it does not contain the IC functions.")


def edit_loaddata_csv(path_to_loaddata_csv: pathlib.Path):
    """
    This function loads in the loaddata csv and edit it to remove unnessecary rows and
    correct the paths to the maximum projection images.

    Parameters
    ----------
    path_to_loaddata_csv : pathlib.Path
        path to the LoadData CSV to be edited
    """
    loaddata_df = pd.read_csv(path_to_loaddata_csv)

    # finds the last z-plane value and assigns it as a variable
    # Metadata_PlaneID values can be any range of values, but this finds the max value
    final_z = max(loaddata_df["Metadata_PlaneID"].unique())

    # create df with only the rows with the last z-plane ID and edit path to the maximum projected images
    loaddata_df = loaddata_df.loc[loaddata_df["Metadata_PlaneID"] == final_z]
    loaddata_df = loaddata_df.replace(regex=r"Images", value="Maximum_Images")

    # save the loaddata csv back to the same path
    loaddata_df.to_csv(path_to_loaddata_csv, index=False)
    print(f"{path_to_loaddata_csv.name} has been edited! All rows have been removed except rows with last z-plane. The remaining rows paths are updated.")

def split_loaddata_csv_by_col(
    path_to_loadata: pathlib.Path,
    output_dir: pathlib.Path,
    col_metadata_name: str,
    col_val_to_split: int,
    first_csv_name: str,
    second_csv_name: str,
):
    """
    This function will split a LoadData CSV (specifically with illumination correction (IC) functions) 
    in half (two groups) based on columns into two different CSVs.
    This is can used for when you have different cell types on the same plate.

    Parameters
    ----------
    path_to_loadata : pathlib.Path
        path to the LoadData CSV with IC functions to be edited
    output_dir : pathlib.Path
        path to directory where new LoadData CSVs will be saved to
    col_metadata_name : str
        metadata column in the LoadData CSV that contains the values for the column of the plate
    col_val_to_split : int
        integer of the last column number of the plate for the first group that the column in being split by.
        Example: the first cell type in a plate runs from columns 1-6 and the second is 7-12, so the 
        col_val_to_split value would be 6.
    first_csv_name : str
        name of the LoadData CSV for the first group of the plate (name should include loaddata and state
        that there are IC functions)
        Example: loaddata_PBMC_with_ic
    second_csv_name : str
        name of the LoadData CSV for the second group of the plate (see example above)
    """
    # load in LoadData CSV as pandas dataframe
    loaddata_df = pd.read_csv(path_to_loadata)

    # split the df based on the col value in half where the first df is the part of the plate runs up to the col_val_to_split column
    first_df = loaddata_df[loaddata_df[col_metadata_name] <= col_val_to_split] 
    # the second df is all values above the col_val_to_split value (not including it)
    second_df = loaddata_df[loaddata_df[col_metadata_name] > col_val_to_split]

    # save new LoadData CSVs based on given name
    first_df.to_csv(pathlib.Path(f"{output_dir}/{first_csv_name}.csv"), index=False)
    second_df.to_csv(pathlib.Path(f"{output_dir}/{second_csv_name}.csv"), index=False)
    print(f"{path_to_loadata.name} has been split into {first_csv_name}.csv and {second_csv_name}.csv!")

def split_loaddata_csv_by_row(
    path_to_loaddata: pathlib.Path,
    output_dir: pathlib.Path,
    row_index_val: int, 
    first_csv_name: str,
    second_csv_name: str,
):
    """
    This function will split a LoadData CSV in half (two groups) based on columns into two different CSVs.
    This is can used for when you have different cell types on the same plate.

    Parameters
    ----------
    path_to_loadata : pathlib.Path
        path to the LoadData CSV with IC functions to be edited
    output_dir : pathlib.Path
        path to directory where new LoadData CSVs will be saved to
    row_index_val : int
        index value to separate 
    first_csv_name : str
        name of the LoadData CSV for the first group of the plate (name should include loaddata and state
        that there are IC functions)
        Example: loaddata_PBMC_with_ic
    second_csv_name : str
        name of the LoadData CSV for the second group of the plate (see example above)
    """
    # load in LoadData CSV as pandas dataframe
    loaddata_df = pd.read_csv(path_to_loaddata)

    # splitting dataframe by row index
    df_1 = loaddata_df.iloc[:row_index_val,:]
    df_2 = loaddata_df.iloc[row_index_val:,:]

    # save new LoadData CSVs based on given name
    df_1.to_csv(pathlib.Path(f"{output_dir}/{first_csv_name}.csv"), index=False)
    df_2.to_csv(pathlib.Path(f"{output_dir}/{second_csv_name}.csv"), index=False)
    print(f"{path_to_loaddata.name} has been split into {first_csv_name}.csv and {second_csv_name}.csv!")
