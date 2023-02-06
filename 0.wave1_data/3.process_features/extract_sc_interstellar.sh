#!/bin/bash
jupyter nbconvert --to python extract_sc_interstellar.ipynb
python extract_sc_interstellar.py
