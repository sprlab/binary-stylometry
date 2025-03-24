"""
This is the driver script to regenerate the results presented in the paper. 
The usage instructions are given.

For each different dataset, this driver script does the following:
It uses compute_result.py to:
- Train a Random Forest Classifier model based on training feature file using weka library
- Compute the accuracy score using the saved model and the test feature file
- Performs 9 fold-validation of accuracy scores for a given dataset by taking the average of each fold
- Save all the accuracy scores to json output files.

"""

import sys, os
import json
from pathlib import Path
from collections import defaultdict
import subprocess
from pprint import pprint

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

rq_paths = {
    1: os.path.join(base_dir, 'data/results_published/RQ1_1'),
    2: os.path.join(base_dir, 'data/results_published/RQ1_2'),
    3: os.path.join(base_dir, 'data/results_published/ndisasm_experiments/RQ1_1'),
    4: os.path.join(base_dir, 'data/results_published/ndisasm_experiments/RQ1_2')
}


def calculate_mean_by_prefix(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    prefix_groups = defaultdict(list)
    for key, value in data.items():
        if isinstance(value, (int, float)):
            prefix = key[:-2]
            prefix_groups[prefix].append(value)

    return {prefix: sum(values) / len(values) for prefix, values in prefix_groups.items()}

def generate_rq_results(rq_path,rq_num):
    output_folder = Path(f'jsons_rq_{rq_num}')
    output_folder.mkdir(parents=True, exist_ok=True) 
    results_cmd = ['python3', 'compute_result.py', rq_path, str(output_folder)]
    subprocess.run(results_cmd, check=True)

    print(f"The output JSON files containing accuracies are stored in: {output_folder}")

    output_json = f'{output_folder}/summary_of_all.json'
    output_avg_accuracy_json =  f'{output_folder}/avg_accuracies_summary_of_all.json'
    results = calculate_mean_by_prefix(output_json)

    saved_models_dir = os.path.abspath("Attribution/saved_models")
    print(f"The corresponding RFC models are saved in: {saved_models_dir}")

    output_avg_accuracy_json = os.path.join(output_folder, 'avg_accuracies_summary_of_all.json')

    with open(output_avg_accuracy_json, 'w') as f:
        json.dump(results, f, indent=4)
        print("Average accuracies are printed below:")
        pprint(results)

    print(f"Average accuracies summary has been saved in: {os.path.abspath(output_avg_accuracy_json)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <rq_number (1 (x86 32-bit binaries), 2 (optimized and stripped binaries), 3 (.text only x86 32-bit unoptimized binaries), 4 (.text only x86 32-bit optimized binaries)>")
        sys.exit(1)

    try:
        rq_num = int(sys.argv[1])
        if rq_num not in rq_paths:
            raise ValueError("Invalid RQ number. Please specify 1, 2, 3, 4.")
        rq_path = str(Path(rq_paths[rq_num]).resolve())
        generate_rq_results(rq_path,rq_num)
    except ValueError as e:
        print(e)
        sys.exit(1)
