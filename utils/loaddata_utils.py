"""
This file contains functions to create different LoadData csvs for specific CellProfiler pipelines
and to edit these outputted csvs.
"""


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
        index_directory,
        config_path,
        path_to_output,
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
        index_directory,
        config_path,
        path_to_output,
        "--illum",
        "--illum-directory",
        illum_directory,
        "--plate-id",
        plate_id,
        "--illum-output",
        illum_output_path,
    ]
    subprocess.run(command, check=True)
    print(f"{illum_output_path.name} is created!")


def edit_loaddata_csv(path_to_loaddata_csv: pathlib.Path):
    """
    This function loads in the loaddata csv and edit it to remove unnessecary rows and
    correct the paths to the maximum projection images.

    Parameters
    ----------
    path_to_loaddata_csv : pathlib.Path
        path to the loaddata csv to be edited
    """
    loaddata_df = pd.read_csv(path_to_loaddata_csv)

    # finds the last z-plane value and assigns it as a variable
    # Metadata_PlaneID values are 1-3 which correlates to the file names p01-p03
    final_z = max(loaddata_df["Metadata_PlaneID"].unique())

    # create df with only the rows with the last z-plane ID and edit path to the maximum projected images
    loaddata_df = loaddata_df.loc[loaddata_df["Metadata_PlaneID"] == final_z]
    loaddata_df = loaddata_df.replace(regex=r"Images", value="Maximum_Images")

    # save the loaddata csv back to the same path
    loaddata_df.to_csv(path_to_loaddata_csv, index=False)
    print(f"{path_to_loaddata_csv.name} has been corrected!")
