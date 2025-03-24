# Binary Stylometry Results

To reproduce the results presented in the paper, use the `driver.py` script. This script trains a Random Forest Classifier model using the provided training feature file and evaluates its accuracy using the test feature files. The average accuracy is computed using 9-fold validation. All feature files are in ARFF format.

```bash
python3 driver.py <result_num> 
```

## Parameters and Corresponding Results Generation:

- ```<1>```: RQ1.1 (Unoptimized Binaries (baseline experiments))
- ```<2>```: RQ1.2 (Optimized and stripped Binaries (baseline experiments))
- ```<3>```: RQ1.2 (unoptimized Binaries (.text section experiments))
- ```<4>```: RQ1.2 (optimized Binaries (.text section experiments))

## Details of Dataset Paths

The details regarding the ARFF feature files datasets are given below:

- ```../data/results_published/RQ1_1```: RQ1.1 (Unoptimized Binaries (baseline experiments))
- ```../data/results_published/RQ1_2```: RQ1.2 (Optimized and stripped Binaries (baseline experiments))
- ```../data/results_published/ndisasm_experiments/RQ1_1```: RQ1.2 (unoptimized Binaries (.text section experiments))
- ```../data/results_published/ndisasm_experiments/RQ1_2```: RQ1.2 (optimized Binaries (.text section experiments))

## Requirements

- Java 11: Ensure that Java Development Kit (JDK) version 11 is installed on your system.
- Install python3 requirements using `pip3 install -r requirements.txt`
