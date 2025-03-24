#!/bin/bash

# Remove all JSON folders
rm -rf jsons_rq_*

# Clear saved models in the Attribution dir
rm -rf Attribution/saved_models/*

# Remove all model files in the Attribution dir
rm -rf Attribution/model/*

# Delete ARFF files in the Attribution dir
rm -rf Attribution/arffs/*
