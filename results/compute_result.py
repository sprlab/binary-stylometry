"""
This script is used as a helper script by the driver script to generate models, results, etc.
"""

import sys
import pprint,json,os
import subprocess
import numpy as np
from pathlib import Path

def parse_weka(weka_output, with_confidence=False):
    """
    Parses the classification made by weka to compute the accuracy score.
    """
    try:
        lines = weka_output.split('\n')
        data = lines[5:] # unclear if this is a safe assumption - TODO
        num_errors = 0
        total = 0
        obj_vals = list()
        for line in data:
            if not line:
                break

            words = line.split()
            total += 1
            confidence = words[-1]
            if len(words) == 4: # correct classification
                obj_vals.append(1-float(confidence))
            elif len(words) == 5: # misclassification
                num_errors += 1 
                obj_vals.append(float(confidence))
            else:
                print("data ended, terminating")
                break

        if with_confidence:
            print(obj_vals)
            return sum(obj_vals)/len(obj_vals)
        else:

            return ( 1 - (num_errors / total)) *100
    except:
        return 0




def compute_accuracies (dataset_arff_folder,output_json_folder):
    """
    This method does the following:
    - Generate a Random Forest Classifier model based on training feature file using weka library
    - Compute the accuracy score using the saved model and the test feature file
    - Performs 9 fold-validation of accuracy scores for a given dataset by taking the average of each fold
    - Save all the accuracy scores to a json output
    """
    result_all={}

    for dataset_path in os.listdir(dataset_arff_folder):
        accs=[]
        dataset_fold=os.path.join(dataset_arff_folder, dataset_path)
        arff_paths = [os.path.join(dataset_fold, file) for file in os.listdir(dataset_fold)]
        i=0
        c_path=os.getcwd()
        attribution_path=c_path+'/Attribution'
        all_folds={}

        ## finding absolute paths of feature files for the given fold

        for arff_file_p in arff_paths:
            if ('_ff_' in arff_file_p):
                continue
            feature_vector={}
            os.chdir(c_path)
            fold=int(arff_file_p.split('.')[2].split('_')[1])

            arff_file_train=arff_file_p
            arff_file_test=''

            for file_arff in arff_paths:
                if '_ff_' in file_arff and os.path.basename(arff_file_p) in file_arff:
                    arff_file_test=file_arff
                    break

            arff_file_train=os.path.abspath(arff_file_train)
            arff_file_test=os.path.abspath(arff_file_test)
            print(f"Fold: {fold}, Training ARFF file: {arff_file_train}, Test ARFF file: {arff_file_test}\n")

            if not (os.path.exists(arff_file_train) and os.path.exists(arff_file_test)):
                print('error in arff feature file paths')
                sys.exit(1)


            os.system("rm -rf Attribution/model/*")
            cmd_copy=f'cp {arff_file_train} Attribution/arffs/train.arff'
            print(cmd_copy,'\n')

             ## Generate RFC model file using weka
            os.system(cmd_copy)
            cmd_weka=f'java -cp Attribution/jars/commons-io-2.6-sources.jar:Attribution/jars/weka.jar weka.classifiers.trees.RandomForest -t {arff_file_train} -d Attribution/model/m.model -I 500 -K 0 -S 1 -attribute-importance -print 2> /dev/null'
            print(cmd_weka,'\n')

            output = subprocess.check_output(cmd_weka, shell=True).decode('utf-8')
            dataset_fold_dict = dict()
            
            os.chdir(attribution_path)

            ## Generate classification for the given fold's test file using weka

            cmd_acc=f'java -cp jars/commons-io-2.6-sources.jar:jars/weka.jar weka.classifiers.trees.RandomForest -T {arff_file_test} -l model/m.model -p 0'
            os.system(f'cp model/m.model saved_models/{os.path.basename(arff_file_p)}_{fold}.model' )

            output = subprocess.check_output(cmd_acc, shell=True).decode('utf-8')

            ## Compute classification accuracy for the given fold
            acc=parse_weka(output)
            if acc!=0:
                accs.append(acc)
            dataset_fold_dict['acc_fold']=acc
            all_folds[f'fold_{fold}']=dataset_fold_dict

        all_folds['avg_accuracy']= np.mean(accs)
        os.chdir(c_path)

        result_all[dataset_path]=np.mean(accs)
        
        ## Save classification accuracy for all 9 folds

        with open(output_json_folder+'/'+dataset_path+'.json', 'w') as json_file:
            json.dump(all_folds, json_file,indent=4)

        print(f"Avg accuracy of {dataset_path}:", np.mean(accs),'\n')
    output_path = os.path.join(output_json_folder, 'summary_of_all.json')

     ## Save classification accuracy for all datasets

    with open(output_path, 'w') as json_file:
        json.dump(result_all, json_file, indent=4)

    print(f"Summary of accuracies saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) <3:
            print(f"Usage: python3 {sys.argv[0]} <dataset_arff_folder> <json_output_folder>")
            sys.exit(1)
    dataset_arff_folder = sys.argv[1]
    output_json_folder = sys.argv[2]
    compute_accuracies(dataset_arff_folder,output_json_folder)

