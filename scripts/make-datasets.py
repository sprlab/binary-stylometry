"""
Given a dataset, this script generates 9-fold variants for further processing.
Input arguments: dataset path, output path, and the number of authors to sample.
"""

import os,sys
from random import sample

num_authors=int(sys.argv[3])
output_dir=sys.argv[2]
path_to_ds=sys.argv[1]
total_folds=9
paths=os.listdir(path_to_ds)
authors_sampled_randomly=sample(paths,num_authors)
authors_clean=[author.replace('.','',5) for author in authors_sampled_randomly]
os.system(f"rm -rf {output_dir}")
os.system(f"mkdir -p {output_dir}")
path_name=f"{num_authors}_authors"
path_name_train=f"{num_authors}_authors_train"
path_name_test=f"{num_authors}_authors_test"
for fold in range(total_folds):
    os.system(f"mkdir -p {output_dir}/{path_name}_{fold}/{path_name_train}")
    os.system(f"mkdir -p {output_dir}/{path_name}_{fold}/{path_name_test}")
for author in authors_sampled_randomly:
     for fold in range(total_folds):
        os.system(f"cp -r {path_to_ds}/{author} {output_dir}/{path_name}_{fold}/{path_name_train}")
        os.system(f"cp -r {path_to_ds}/{author} {output_dir}/{path_name}_{fold}/{path_name_test}")

problems=os.listdir(f"{path_to_ds}/{authors_sampled_randomly[0]}")
problems=[problem.split('_')[0] for problem in problems]
fold=0
def get_path(list,problem):
    for elem in list:
        if problem in elem:
            return elem
    return 0
for author in authors_sampled_randomly:
    fold=0
    for problem in problems:

        problems_train=os.listdir(f"{output_dir}/{path_name}_{fold}/{path_name_train}/{author}")
        problems_test=os.listdir(f"{output_dir}/{path_name}_{fold}/{path_name_test}/{author}")
        os.system(f"rm -rf {output_dir}/{path_name}_{fold}/{path_name_train}/{author}/{get_path(problems_train,problem)}")
        for prob in problems:
            if prob!=problem:
                os.system(f"rm -rf {output_dir}/{path_name}_{fold}/{path_name_test}/{author}/{get_path(problems_test,prob)}")
        fold+=1
