"""
This collection of functions runs CellProfiler and will rename the .sqlite outputted to any specified name if running an analysis pipeline.
"""

# must use the annotations import as CellProfiler is restricted to Python 3.8 at this time so Optional
# by itself only works in Python 3.10
from __future__ import annotations
from typing import Optional
import os
import subprocess
import pathlib


def rename_sqlite_file(
    sqlite_dir_path: pathlib.Path, name: str, hardcode_sqlite_name: str
):
    """Rename the .sqlite file to be {method}.sqlite as to differentiate between the files

    Args:
        sqlite_dir_path (pathlib.Path): path to CellProfiler_output directory
        name (str): new name for the SQLite file
        hardcode_sqlite_name (str): hardcoded name of the returned SQLite file from CellProfiler to change
    """
    try:
        # CellProfiler requires a name to be set in to pipeline, so regardless of plate or method, all sqlite files name are hardcoded
        sqlite_file_path = pathlib.Path(
            f"{sqlite_dir_path}/{hardcode_sqlite_name}.sqlite"
        )

        new_file_name = str(sqlite_file_path).replace(
            sqlite_file_path.name, f"{name}.sqlite"
        )

        # change the file name in the directory
        pathlib.Path(sqlite_file_path).rename(pathlib.Path(new_file_name))
        print(f"The file is renamed to {pathlib.Path(new_file_name).name}!")

    except FileNotFoundError as e:
        print(
            f"The {hardcode_sqlite_name}.sqlite file is not found in directory. Either the pipeline wasn't ran properly or the file is already renamed.\n"
            f"{e}"
        )


def run_cellprofiler(
    path_to_pipeline: str,
    path_to_output: str,
    path_to_loaddata: str,
    sqlite_name: Optional[None | str] = None,
    hardcode_sqlite_name: Optional[str | None] = None,
    analysis_run: Optional[bool | False] = False,
):
    """Run CellProfiler on data using LoadData CSV. It can be used for both a illumination correction pipeline and analysis pipeline.

    Args:
        path_to_pipeline (str): path to the CellProfiler .cppipe file with the segmentation and feature measurement modules
        path_to_output (str): path to the output folder (the directory will be created if it doesn't already exist)
        path_to_loaddata (str): path to the LoadData CSV to load in the images and IC functions
        sqlite_name (str, optional): string with name for SQLite file for an analysis pipeline (default is None)
        analysis_run (bool, optional): will use functions to complete an analysis pipeline (default is False)
    """
    # check to make sure the paths to files are correct and they exists before running CellProfiler
    if not os.path.exists(path_to_pipeline):
        raise FileNotFoundError(f"Directory '{path_to_pipeline}' does not exist")
    if not os.path.exists(path_to_loaddata):
        raise FileNotFoundError(f"Directory '{path_to_loaddata}' does not exist")

    if not analysis_run:
        # run CellProfiler on a plate that has not been analyzed yet
        print(f"Starting CellProfiler run on {pathlib.Path(path_to_loaddata).name}")
        # a log file is created for each plate or data set name that holds all outputs and errors
        with open(
            pathlib.Path(
                f"logs/cellprofiler_output_{pathlib.Path(path_to_loaddata).name}.log"
            ),
            "w",
        ) as cellprofiler_output_file:
            # run CellProfiler for a IC or zproj pipeline
            command = [
                "cellprofiler",
                "-c",
                "-r",
                "-p",
                path_to_pipeline,
                "-o",
                path_to_output,
                "--data-file",
                path_to_loaddata,
            ]
            subprocess.run(command, capture_output=cellprofiler_output_file, check=True)

    if analysis_run:
        # runs through any files that are in the output path
        if any(
            files.name.startswith(sqlite_name)
            for files in pathlib.Path(path_to_output).iterdir()
        ):
            raise NameError(
                f"The file {sqlite_name}.sqlite has already been renamed! This means it was probably already analyzed."
            )

        # run CellProfiler on a plate that has not been analyzed yet
        print(f"Starting CellProfiler run on {pathlib.Path(path_to_loaddata).name}")
        # a log file is created for each plate or data set name that holds all outputs and errors
        with open(
            pathlib.Path(
                f"logs/cellprofiler_output_{pathlib.Path(path_to_loaddata).name}.log"
            ),
            "w",
        ) as cellprofiler_output_file:
            # run CellProfiler for an analysis run
            command = [
                "cellprofiler",
                "-c",
                "-r",
                "-p",
                path_to_pipeline,
                "-o",
                path_to_output,
                "--data-file",
                path_to_loaddata,
            ]
            subprocess.run(command, capture_output=cellprofiler_output_file, check=True)

        # rename the outputted .sqlite file to the
        rename_sqlite_file(
            sqlite_dir_path=pathlib.Path(path_to_output),
            name=sqlite_name,
            hardcode_sqlite_name=hardcode_sqlite_name,
        )
