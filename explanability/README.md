# Binary Stylometry Explanability Analysis

This folder contains computed SHAP values and feature files for analyzing top features of authors of top-performing and low-performing 20-author datasets.

You can use this folder to:
- Identify confidence-sorted authors.
- Extract top features for specific authors. The shap values of the corresponding top features will also be listed.
- Find feature importance values in the corresponding json files.
- Demonstrate the usage of erroneous disassembly features in action using an example. 

## Requirements

- Install python3 requirements using `pip3 install -r requirements.txt`

### Feature and SHAP Files

This contains the following files:

- top Performing Dataset (20_3)
  - `20_3.json`: JSON file containing accuracy, features, and feature importance values for the top-performing 20-author dataset.
  - `20_3.json_5.npy`: NPY file containing computed SHAP values of features for the top-performing 20-author dataset (fold 5).
  - `20_3_fold_5.arff`: Feature file for the top-performing 20-author dataset (fold 5).
- low Performing Dataset (20_1)
  - `20_1.json`: JSON file containing accuracy, features, and feature importance values for the low-performing 20-author dataset.
  - `20_1.json_3.npy`: NPY file containing computed SHAP values of features for the low-performing 20-author dataset (fold 3).
  - `20_1_fold_3.arff`: Feature file for the low-performing 20-author dataset (fold 3).




### Confidence-Sorted Authors

To get confidence-sorted authors for the top-performing dataset (20_3) and top-performing fold (5):

```bash
python3 display_acc_order.py 20_3.json 5
```

The output will be saved to:

```
author_predictions_confidence_20_3.json_5.txt
```

### Extracting Top Features for an Author

For your author of interest, get top features using the following script:

```bash
python3 npy_to_top_features.py 20_3.json_5.npy 20_3_fold_5.arff <author_interest>
```

Example:

```bash
python3 npy_to_top_features.py 20_3.json_5.npy 20_3_fold_5.arff perhark
```

### Confidence-Sorted Authors (low Performing)

For the low-performing dataset (20_1) and top-performing fold (3):

```bash
python3 display_acc_order.py 20_1.json 3
```

The output will be saved to:

```
author_predictions_confidence_20_1.json_3.txt
```

### Extracting Top Features for an Author (low Performing)

For your author of interest, get top features using the following script:

```bash
python3 npy_to_top_features.py 20_1.json_3.npy 20_1_fold_3.arff <author_interest>
```

Example:

```bash
python3 npy_to_top_features.py 20_1.json_3.npy 20_1_fold_3.arff WalkerShi
```


### Erroneous Disassembly Analysis Script

The `erroneous_disasm_example` folder contains code and data that demonstrates erroneous disassembly in action using an example. This example is taken from best performing 20-author dataset (20_3) and its top fold (5). 

#### Overview
The provided script does the following:

- Analyzes features that correspond to erroneous disassembly of the source filename (containing author name).
- Processes a snippet of the disassembly file related to the erroneous disassembly containing author name.
- Converts the machine code into its ASCII representation.
- Generates instruction line bigrams from the instruction code associated with the machine code.
- Maps those instructions back to the feature file used by the best performing 20-author model (fold_5).

#### Usage

To use this script, navigate to the `erroneous_disasm_example` folder and run:

```sh
python3 analysis.py

```
