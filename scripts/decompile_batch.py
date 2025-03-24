"""
This script batch decompiles a binary dataset into decompiled C++ files using IDA Pro.
Input arguments: dataset path, number of processes to use.
Requirements: IDA Pro with Hex-Rays.
"""

import sys
import os
from multiprocessing import Pool


## Provide IDA PRO PATH here

IDAT_PATH=""
cmd_hexa="-Ohexrays:{outfile}:ALL -A"

path=sys.argv[1]
n = int(sys.argv[2])

def decompile(path):
    path_author=path[0]
    author=path[1]
    problem=path[2]
    problem_path=path_author+f"/{problem}"
    out_path=path_author+f"/{problem}_{author}"
    cmd_full=IDAT_PATH+' '+cmd_hexa.format(outfile=out_path)+f' {problem_path}'
    print(cmd_full)
    os.system(cmd_full)
    os.system(f'rm -rf {problem_path}.i64')

    return 0
problem_list=[]
for author in os.listdir(path):
    path_author=f"{path}/{author}"
    for problem in os.listdir(path_author):
        pack=[path_author,author,problem]
        problem_list.append(pack)

start_index = 0
# Iterate through the list in chunks of size n
while start_index < len(problem_list):
    chunk = problem_list[start_index:start_index + n]
    len_pool=len(chunk)
    with Pool(len_pool) as p:
        output_vals=p.map(decompile,chunk)
        print(f'{start_index+n} decompiled so far.')
        p.close()
    
    start_index += n