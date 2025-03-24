"""
This script prints the confidence level of author predictions made by the model for 
a given fold.
"""

import os, sys, json, re ,pprint
import numpy as np 


if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} <json_file> <fold_no> ")
    sys.exit(1)

try:

    file_path = sys.argv[1]
    fold=int(sys.argv[2])

except Exception as e:
    print("Error: Arguments incorrect.")
    sys.exit(1)

with open(file_path, 'r') as file:
    data = json.load(file)

res=data[f'fold_{fold}']['result_output']
lines = res.strip().split('\n')[3:]  # Skip the header and empty lines
data2 = []

for line in lines:
    
    parts = line.split()
    print(parts)
    inst = int(parts[0])
    actual = parts[1]
    actual=actual.split(":")[1]
    predicted = parts[2].split(":")[1]

    prediction_confidence = float(parts[-1])
    data2.append((inst, actual, predicted, prediction_confidence))

# Sort the data by prediction confidence in descending order
sorted_data = sorted(data2, key=lambda x: x[3], reverse=True)

print("=== Sorted Predictions by Confidence ===\n")
print("actual predicted prediction")
for inst, actual, predicted, prediction_confidence in sorted_data:
    print(f"{actual} {predicted} {prediction_confidence:.3f}")

base_name = os.path.basename(file_path)
with open(f"author_predictions_confidence_{base_name}_{fold}.txt", "w") as file:
    for inst, actual, predicted, prediction_confidence in sorted_data:
        file.write(f"{actual} {predicted} {prediction_confidence:.3f}\n")
