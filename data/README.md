# Binary Stylometry Data

## Details of Dataset Paths

- ```results_published/```: This contains ARFF feature files that were generated after processing with the pipeline.
- ```baseline_dataset/cpp_dataset_2008_2020.tar.gz```: This contains the baseline GCJ dataset sampled from the years 2008-2020.
- ```/processed_data/unoptimized_x86_dataset.tar.gz```: This contains the preprocessed dataset after the above dataset is compiled with g++ (v4.8) and decompiled with IDAPRO Hexrays (v8.3). This dataset, when decompressed and sampled for different author counts (20, 50, 100), can be used as an input to be fed to pipeline.