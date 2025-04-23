#!/bin/bash

# This script is the driver script to generate feature files and RFC model given a single-fold binary+decompiled_cpp dataset.

#The `end_to_end.sh` script executes the following steps using `pipeline.py`, `arff_parse.py` and `acc.py` scripts:

### Training Phase:
# 1. Disassemble with NDISASM  
# 2. Disassemble with bjoern-radare2  
# 3. Extract AST using joern-tools
# 4. Extract CFG using bjoern-radare2 (with a timeout, as sometimes the tool gets stuck)
# 5. Consolidate features into ARFF files  
# 6. Perform information gain analysis and train the RFC model  

### Testing Phase:
# 1. Disassemble with NDISASM  
# 2. Disassemble with bjoern-radare2
# 3. Extract AST using joern-tools
# 4. Extract CFG using bjoern-radare2 (with a timeout, as sometimes the tool gets stuck)
# 5. Consolidate features into ARFF files  
# 6. Extract features from ARFF files to match the information gain-selected features from the training phase  

# Finally, the extracted test features are evaluated using the trained model to generate accuracy results.

dataset_name=$1
dataset_name=$(echo $dataset_name | tr -d "/")
train_name="$dataset_name"_train
test_name="$dataset_name"_test


path_to_train=Attribution/datasets/$train_name
path_to_test=Attribution/datasets/$test_name

# Running steps 1 to 3

python3 pipeline.py --steps 123 $path_to_train

# Running steps 4-6

python3 exec_s4_to.py $path_to_train
python3 pipeline.py --steps 56 $path_to_train


echo -e "\n\n\n"
echo "Training Done, now running the testing"
echo -e "\n\n\n"

# Running steps 1 to 5

python3 pipeline.py --steps 123 $path_to_test
python3 exec_s4_to.py $path_to_test
python3 pipeline.py --steps 5 $path_to_test


train_IG="$train_name"_IG
arff_addr_train=Attribution/arffs/$train_IG.arff
arff_addr_test=Attribution/arffs/$test_name.arff

python3 arff_parse.py $arff_addr_test --features $arff_addr_train

mkdir -p results
results_name=$dataset_name.txt

cd Attribution

java -cp jars/commons-io-2.6-sources.jar:jars/weka.jar weka.classifiers.trees.RandomForest -T arffs/"$test_name"_ff_"$train_IG".arff -l models/"$train_name".model -p 0 >& ../results/$results_name
cd ..

python3 acc.py results/$results_name