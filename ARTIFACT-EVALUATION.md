# Artifact Appendix

Paper title: **#Does Coding Style Really Survive Compilation? Stylometry of Executable Code Revisited**

Artifacts HotCRP Id: **#10** 

Requested Badge: **Reproduced, Functional, and Available**

## Description

This artifact contains code and data reproduce the accuracy results presented in the paper. These results correspond to Tables 2 and 3 of the paper. The code trains a Random Forest Classifier model using the provided training feature file and evaluates its accuracy using the test feature files. Note that these feature files have been already preprocessed with the feature extraction pipeline. The average accuracy is computed using 9-fold validation. All feature files are in ARFF format.
Secondly, the artifact also contains data and instructions to inspect the cause (explanability) analysis corresponding to Tables 4 and 5 of the paper.

### Security/Privacy Issues and Ethical Concerns (All badges)

N/A

## Basic Requirements (Only for Functional and Reproduced badges)
The artifacts can be reproduced in the VM setup with the associated PETS Artifacts submission account. 

### Hardware Requirements
To reproduce the results proposed in this evaluation:

- A VM setup with the associated PETS Artifacts submission account is sufficient.
- VM Specs are : 4 cores, 16GB memory, 40GB disk, running Ubuntu 22.04.

To run the pipeline:
A Linux system with at least 8 cores, 32GB memory, and 500GB storage is recommended for optimal performance.


### Software Requirements
The following are the requirements:
 - A linux Environment (ideally Ubuntu 22.04)
 - Java JDK 11
 - Python packages listed in requirments.txt

We also recommend running the pipeline inside a Docker container for consistency and ease of setup.

### Estimated Time and Storage Consumption
The accuracy experiments will take upto 5-10 hours to finish.
The explanability experiments will finish instantly.

## Environment 
The artifacts can be reproduced in the VM setup with the associated PETS Artifacts submission account. A linux based system is reccomended.

### Accessibility (All badges)

The repository containing code and data is made public at https://github.com/sprlab/binary-stylometry.

### Set up the environment (Only for Functional and Reproduced badges)
The artifacts are present in the VM associated with the PETS Artifacts submission account.
Login to the VM using ssh. The login details for the account is found in the PETS Artifacts submission webstie, as I have made the VM accesible to the reviewers.

The artifacts are present in the `/home/artifacts/binary-stylometry` folder.

Moreover, you can also perform all the steps proposed below by cloning: https://github.com/sprlab/binary-stylometry

### Testing the Environment (Only for Functional and Reproduced badges)
Ensure that the installation requirements are met.

## Artifact Evaluation (Only for Functional and Reproduced badges)

The first artifact reproduces the accuracy results reported in the paper. These results are obtained as follows:

- Preprocessed training and testing feature files, generated after feature extraction and reduction using the InfoGain criterion, are used.
- The training feature files are used to train a Random Forest classifier with the following configuration: `-I 500 -K 0 -S 1`. This configuration specifies training 500 decision trees.
- The resulting accuracy metrics are saved in an output JSON folder.

The second aspect of the artifact evaluation focuses on explainability analysis:

- Processed SHAP values for the features of both the top- and low-performing authors are stored in `.npy` files.
- The scripts to identify confidence sorted authors and find top features are included.
- These results support Section 6.2 and Tables 4 and 5 in the paper, including top features, SHAP values, and feature importance scores.
- By an example, demonstrate the usage of erroneous disassembly in action (discussed in Section 6.2).

### Main Results and Claims
This artifact reproduces the accuracy results mentioned in Table 2, Table 3 of the paper. This artifact also supports the results in Tables 4 and 5 (corresponding to explanability Analysis) in the paper.  

#### Main Result 1: Accuracy Results
The first artifact reproduces the accuracy results reported in the paper. 

The accuracies for following dataset experiments are reproduced:
- RQ1.1 (Unoptimized Binaries (baseline experiments)) (Table 2 and Section 5.2)
- RQ1.2 (Optimized and stripped Binaries (baseline experiments)) (Table 3 and Section 5.2)
- RQ1.2 (unoptimized Binaries (.text section experiments)) (Table 3 and Section 5.2)
- RQ1.2 (optimized Binaries (.text section experiments)) (Table 3 and Section 5.2)


#### Main Result 2: Explanability Analysis

This artifact reproduces the top features, SHAP values, and feature importance scores that support the explainability analysis results presented in Tables 4 and 5 of the paper. It also demonstrates the usage of erroneous disassembly in action (discussed in Section 6.2) through an example.


### Experiments 
Make sure you have logged into the linux VM associated with PETS Artifacts submission account. The login instructions are provided in the `Set up the environment` Section above.

#### Experiment 1: Accuracy Results

For **Main Result 1**, follow these steps:

1. Navigate to the results directory:
   ```bash
   cd /home/artifacts/binary-stylometry/results
   ```

2. Run the following script to generate the results sequentially:
   ```bash
   python3 driver.py 1
   python3 driver.py 2
   python3 driver.py 3
   python3 driver.py 4
   ```

3. The corresponding results will be saved in the following directories:
   - `jsons_rq_1`
   - `jsons_rq_2`
   - `jsons_rq_3`
   - `jsons_rq_4`

4. Inspect the average accuracy files in each directory:
   ```
   jsons_rq_{rq_num}/avg_accuracies_summary_of_all.json
   ```
   Compare these accuracy results with those presented in **Tables 2 and 3** of the paper.

### Mapping of Results to Paper Sections:
- `jsons_rq_1` → Corresponds to Table 2 (all experiments of our work) and the Table 2 experiment of optimization - O0.
- `jsons_rq_2` → Corresponds to Table 3 baseline experiment results and stripped binaries in Section 5.2.
- `jsons_rq_3` → Corresponds to Table 3 Accuracy (.text section only disassembly) experiment of optimization - O0.
- `jsons_rq_4` → Corresponds to Table 3 Accuracy (.text section only disassembly) experiment of optimizations - O1, O2, O3, Os.


### Additional Files to Inspect:

- Feature files are stored in `binary-stylometry/data/results_published` and are also listed in README.md.
- RFC models are stored in `binary-stylometry/results/Attribution/saved_models` after they are generated with the driver scripts.

#### Experiment 2: Explanability Analysis

#### SHAP Values & Feature Analysis for 20-Author Datasets

This analysis contains computed SHAP values and feature files for analyzing the **top-** and **low-performing** 20-author datasets. It also contains an example that demonstrates the usage of erroneous disassembly.


#### Usage:
- Identify confidence-sorted authors.
- Extract top features for specific authors, along with corresponding SHAP values.
- Find feature importance values in JSON files.
- Demonstrate the usage of erroneous disassembly in action.

 Firstly, navigate to the explanability directory:
   ```bash
   cd /home/artifacts/binary-stylometry/explanability/
   ```

#### To get confidence-Sorted Authors
#### top-Performing Dataset (20_3, Fold 5)
```bash
python3 display_acc_order.py 20_3.json 5
```
Output: `author_predictions_confidence_20_3.json_5.txt`

#### low-Performing Dataset (20_1, Fold 3)
```bash
python3 display_acc_order.py 20_1.json 3
```
Output: `author_predictions_confidence_20_1.json_3.txt`

#### To fetch top Features for an Author
#### top-Performing Dataset (20_3, Fold 5)
```bash
python3 npy_to_top_features.py 20_3.json_5.npy 20_3_fold_5.arff <author_interest>
```
Example:
```bash
python3 npy_to_top_features.py 20_3.json_5.npy 20_3_fold_5.arff perhark
```

#### low-Performing Dataset (20_1, Fold 3)
```bash
python3 npy_to_top_features.py 20_1.json_3.npy 20_1_fold_3.arff <author_interest>
```
Example:
```bash
python3 npy_to_top_features.py 20_1.json_3.npy 20_1_fold_3.arff WalkerShi
```

#### File Details are provided below

#### top-Performing Dataset (20_3, Fold 5)
- `20_3.json`: Accuracy, features, and feature importance.
- `20_3.json_5.npy`: SHAP values.
- `20_3_fold_5.arff`: Feature file.

#### low-Performing Dataset (20_1, Fold 3)
- `20_1.json`: Accuracy, features, and feature importance.
- `20_1.json_3.npy`: SHAP values.
- `20_1_fold_3.arff`: Feature file.

## Analysis of Features

After top feature names have been extracted out for the given authors, do the following analysis:

For a high level overview:

- Find out total number of unique features across authors.
- Find out total number of common features across authors.
- Find out their SHAP and Feature Importance values ranges (Note that SHAP values may vary across different runs).
- Look at the feature text to determine the feature type.

This would help in reproducing Tables 4 and 5 of the paper.

The SHAP values were found to be in the range (0.001 to 0.01).
The Feature Importance values were found to be in the range (0.5 to 0.8).

For feature level analysis:

Note that this step requires you to run the pipeline to get the intermediate data.

#### ndisasm‑based features

This following analysis would help in reproducing in Table 6 the paper.

- Search the feature text within the ndisasm output (.dis files in the intermediate data) to locate the exact instructions.
- Extract the corresponding machine‑code bytes and translated machine code to ASCII representation.
- Determine the binary section (e.g., .text) in which those bytes occur. This is done by using `readelf` tool and aligning instruction location against offset with the address provided by the tool.
- Classify the feature as code‑based if it exists in .text, otherwise non‑code‑based.
- If a feature occured in non-code based sections, analyze its ASCII String to detect patterns like function calls, symbol usage, etc. 

#### radare2‑based features

- Search and align the feature text in the radare2 disassembly files (nodes.csv file in the intermediate data) to locate the instructions.
- Manually analyze radare2’s autogenerated comments (such as function headers on calls) around the instructions to detect patterns like function calls, etc.

#### AST‑based features

- Search and align the feature text in the decompiled C++ file. 
- Manually analyze the code constructs to detect patterns like function calls, etc.

### Erroneous Disassembly Example

The `/home/artifacts/binary-stylometry/explanability/erroneous_disasm_example` folder contains code and data that demonstrates erroneous disassembly in action using an example. This example is taken from top performing 20-author dataset (20_3) and its top fold (5).

#### Overview

The provided script `analysis.py` does the following:

- Analyzes features that correspond to erroneous disassembly of the source filename (containing author name).
- Processes a snippet of the disassembly file related to the erroneous disassembly containing author name.
- Converts the machine code into its ASCII representation.
- Generates instruction line bigrams from the instruction code associated with the machine code.
- Maps those instructions back to the feature file used by the top performing 20-author model (fold_5).

#### Usage

To perform the analysis, navigate to the `/home/artifacts/binary-stylometry/explanability/erroneous_disasm_example` folder and run:

```sh
python3 analysis.py

```

## Limitations (Only for Functional and Reproduced badges)

The evaluation is based on feature files that have already been preprocessed by the pipeline. This simplifies the process, as the original pipeline can take a long time (weeks) to generate these feature files.
However, feature files can still be regenerated by following the instructions in the pipeline folder and using the 2008-2020 dataset available in the data folder.

## Notes on Reusability (Only for Functional and Reproduced badges)
The pipeline folder can be used by researchers to evaluate thier datasets on the caliskan system.
The datasets in the data can be used by researchers to evaluate their system.
Please read README.md in data, explanability, and pipeline for further information.