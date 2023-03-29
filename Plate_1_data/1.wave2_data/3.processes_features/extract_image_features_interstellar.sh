#!/bin/bash
jupyter nbconvert --to python extract_image_features_interstellar.ipynb
python extract_image_features_interstellar.py
