"""
    File: pipeline.py
    Authors: Ben Jacobsen, Muaz Ali
    Purpose: A python wrapper for shepherding data through Caliskan's system, 
        from dataset to feature files and model.

    This pipeline is built on top of the original 
    Binary Stylomery work from this repository: https://github.com/calaylin/bda
"""

import sys
import os
import subprocess
import argparse
import fileinput
import re
import time
import psutil


def main():
    parser = argparse.ArgumentParser(description="""Create a random forest using a specified dataset. 
    This script should be run in the root directory of the ComprehensiveAttribution project.""")
    parser.add_argument("dataset_dir", metavar="/path/to/data",
                        type=str, help="path to dataset directory")
    parser.add_argument("--genconf", help="generate config file",
                        action="store_true")
    parser.add_argument("--java", help="specify java7 location for neo4j", type=str,
                        metavar="/path/to/java")    
    parser.add_argument("--initneo", help="initialize neo4j configuration",
                        action="store_true")         
    parser.add_argument("--neo_instance", help="which neo4j instance to use (1-6)",
                        type=int, default=1)
    parser.add_argument("--astonly", help="extract ast and nothing else",
                        action="store_true")
    #args = parser.parse_args()
    parser.add_argument("--steps", help="""specify which steps to be performed.\n
    1 = disassemble with NDISASM\n
    2 = disassemble with bjoern\n
    3 = extract AST\n
    4 = extract CFG\n
    5 = extract features\n
    6 = information gain + model training\n
    default: 123456
    """, default = "123456")
    args, others = parser.parse_known_args()
    
    dataset_dir = os.path.abspath(args.dataset_dir)
    root = os.getcwd()
    
    if args.genconf:
        # generate a configuration file for the java project
        gen_conf(dataset_dir, args.java, args.neo_instance)
    if args.initneo:
        # set the server location for neo4j (only run once)
        with fileinput.FileInput("neo4j/conf/neo4j-server.properties", 
                                inplace=True, backup=".bak") as fobj:
            pattern = re.compile("org.neo4j.server.database.location=*")
            for line in fobj:
                if pattern.match(line):
                    print(line.replace(line, "org.neo4j.server.database.location=" +
                          os.path.join(root,"Attribution/.joernIndex")))
                else:
                    print(line, end='')
             
    os.chdir("bjoern-radare")
    
    
    # create representations of the program
    os.chdir("../Attribution")
    classpath = ":".join([
        os.path.join(root, "Attribution/bin"),
        os.path.join(root, "Attribution/jars/*")
        ])
    
    conf_name = f"config/{os.path.basename(dataset_dir)}.conf"
    
    t0 = time.time()

    if '1' in args.steps:
        disassem1 = java_run(classpath, "BinaryDisassemble", (conf_name,))
    if '2' in args.steps:
        disassem2 = java_run(classpath, "bjoernDisassemble", (conf_name,))
    if '3' in args.steps:
        gen_ast = java_run(classpath, "FeatureCalculators_decompile", (conf_name,))
    if '4' in args.steps:
        i = 1
        while os.path.exists('orient_db.lck'):
            print("orient_db.lck exists, waiting for earlier script to finish")
            time.sleep(i)
            i += 1
        # more potential data races
        f = open('orient_db.lck', 'w')
        f.close()
        
        # start server
        os.chdir('../bjoern-radare')
        bjoernServer = subprocess.Popen(["./bjoern-server.sh"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        os.chdir('../Attribution')
        time.sleep(5) # ample time for server to start

        # actual generation of cfgs
        gen_cfg = java_run(classpath, "bjoernGenerateGraphmlCFG", (conf_name,))

        # terminate server
        child_processes = psutil.Process(bjoernServer.pid).children(recursive=True)
        for child in child_processes:
            child.terminate()
        bjoernServer.terminate()
        # signal that server is available to other processes
        os.remove('orient_db.lck')
    
    t1 = time.time()
    
    if '5' in args.steps:  
        extract_features = java_run(classpath, "FeatureExtractorAllFeatures_decompile", (conf_name,))
   
    t2 = time.time()
   
    if '6' in args.steps:
        train_classifier = java_run(classpath, "AuthorClassificationBasic", (conf_name,))
   
    t3 = time.time()
        
    print(f"Create representations: {t1-t0}")
    print(f"Extract features: {t2-t1}")
    print(f"Train classifier: {t3-t2}")
    
    
    print("done")


def java_run(classpath, program, args):
    return subprocess.run(["java", "-cp", classpath, program, *args])

    
    
def gen_conf(dataset_dir, java_home, neo4j_instance=1):
    root = os.getcwd()
    data_name = os.path.basename(dataset_dir)
    if java_home:
        java_str = f"JAVA_HOME={java_home}"
    else:
        java_str = ''
        
    conf = f"""testFolder = {root}/Attribution/datasets/{data_name}/
language = cpp
bjoern-radare = {root}/bjoern-radare
bjoernJar = {root}/bjoern-radare/bin/bjoern.jar
localBin = /usr/local/bin/
orient_db = {root}/bjoern-radare/orientdb-community-2.1.5
neo4jStart = {java_str} {root}/neo4j/neo4j{neo4j_instance}/bin/neo4j start
neo4jStop = {root}/neo4j/neo4j{neo4j_instance}/bin/neo4j stop
neo4jPort = {7472 + 2*neo4j_instance}
joernJar = {root}/StylometrySetup/joern-0.3.1/bin/joern.jar
joernTools = {root}/StylometrySetup/joern-tools/
joernTemplate = {root}/StylometrySetup/CodeStylometry-missing-joern-tools-files/template.py
joernIndex = {root}/Attribution/.joern{neo4j_instance}
featureFile = {root}/Attribution/arffs/{data_name}.arff
IG_featureFile = {root}/Attribution/arffs/{data_name}_IG.arff
pythonCommand = python2
model_file = {root}/Attribution/models/{data_name}.model
"""
    with open(f"Attribution/config/{data_name}.conf", 'w') as fobj:
        fobj.write(conf)


if __name__ == "__main__":
    main()
