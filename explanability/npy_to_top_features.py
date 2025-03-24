
"""
This script prints the top SHAP features for a desired author.
"""

import os, sys, json, re ,pprint
from scipy.io import arff
import numpy as np 
import time

if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} <npy> <test_arff_file> <author_interest> ")
    sys.exit(1)

try:
    npy_file = sys.argv[1]
    author_interest = sys.argv[3]
    arff_file_path=sys.argv[2]

except Exception as e:
    print("Error: Arguments incorrect.")
    sys.exit(1)


def get_top_features_proba(shap_values, class_index, num_features=20):
    global features_all_authors
    # Get SHAP values for the specified author
    shap_values_class = shap_values[:,:,class_index]
    # Calculate the mean absolute SHAP values for each feature
    shap_values_abs_mean = np.mean(np.abs(shap_values_class), axis=0)
    top_feature_indices = np.argsort((shap_values_abs_mean))[-num_features:][::-1]
    top_features = [features_all_authors[x] for x in top_feature_indices]

    return top_features, shap_values_abs_mean[top_feature_indices]

def prune_feature_scipy(feature):
    val=feature.strip()
    return val
data, meta = arff.loadarff(arff_file_path)
features_all_authors = []
for feature in list(meta.names()[:-1]):
    feautre_new=prune_feature_scipy(feature)
    features_all_authors.append(feautre_new)

author_names = meta[meta.names()[-1]][1]
authors_all_names=list(author_names)
class_num=authors_all_names.index(author_interest)
shap_values=np.load(npy_file)

top_features_class_author, feature_importance_class_author = get_top_features_proba(shap_values, class_num)

print(f"Top features for author {author_interest}:")
idx=1

for feature, importance in zip(top_features_class_author, feature_importance_class_author):
    print(f"{idx}: {feature}: {importance}")
    idx+=1

