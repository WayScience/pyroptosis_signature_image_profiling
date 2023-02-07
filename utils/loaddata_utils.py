"""
This file contains functions to create different LoadData csvs for specific CellProfiler pipelines.
"""
import os
import pathlib

def create_loaddata_csv(
    index_directory: pathlib.Path,
    config_path: pathlib.Path,
    path_to_output: pathlib.Path,
):
    """
    Create LoadData csv for CellProfiler (used for illum pipelines)

    Parameters
    ----------
    index_directory : pathlib.Path
        path to the `Index.idx.xml` file for the plate (normally located in the /Images folder)
    config_path : pathlib.Path
        path to the `config.yml' file for pe2loaddata to process the csv
    path_to_output : pathlib.Path
        path to the `wave1_loaddata.csv' file used for generating the illumination correction functions for each channel
    """
    command = f"pe2loaddata --index-directory {index_directory} {config_path} {path_to_output}"
    os.system(command)
    print(f'{path_to_output.name} is created!')

def create_loaddata_illum_csv(
    index_directory: pathlib.Path,
    config_path: pathlib.Path,
    path_to_output: pathlib.Path,
    illum_directory:pathlib.Path,
    plate_id:str,
    illum_output_path:pathlib.Path,
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
    command = f"pe2loaddata --index-directory {index_directory} {config_path} {path_to_output} --illum --illum-directory {illum_directory} --plate-id {plate_id} --illum-output {illum_output_path}"
    os.system(command)
    print(f'{illum_output_path.name} is created!')
