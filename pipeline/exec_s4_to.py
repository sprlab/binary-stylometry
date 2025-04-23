#!/usr/bin/env python3
"""
Runs step4 on each author up to 2 times with a timeout.
"""
import sys, os
import shutil
import subprocess
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("Usage: driver.py <dataset-dir>")

dir1 = Path(sys.argv[1])
dir2 = dir1.with_name(dir1.name + '.back')
dir3 = dir1.with_name(dir1.name + '.temp')
ds_name = dir1.name
faulty_log = Path('faulty_authors.txt')

if dir2.exists():
    shutil.rmtree(dir2)
shutil.copytree(dir1, dir2)

def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)

def append_faulty(author):
    with faulty_log.open('a') as f:
        f.write(author + '\n')

reset_dir(dir1)
reset_dir(dir3)

for author_dir in dir2.iterdir():
    if not author_dir.is_dir():
        continue
    author = author_dir.name
    tries = 0
    while True:
        orient_db_lck = 'Attribution/orient_db.lck'
        if os.path.exists(orient_db_lck):
            os.remove(orient_db_lck)
        db_process = 'bjoern-radare/orientdb-community-2.1.5/bin/server.sh'
        try:
            subprocess.run(['pkill', '-9', '-f', db_process], check=True)
        except subprocess.CalledProcessError:
            pass

        tries += 1
        reset_dir(dir1)
        shutil.copytree(author_dir, dir1 / author)
        cmd = [sys.executable, 'pipeline.py', '--steps','4', str(dir1)]
        try:
            subprocess.run(cmd, check=True, timeout=120)
        except subprocess.TimeoutExpired:
            if tries >= 2:
                append_faulty(author)
                break
            continue
        except subprocess.CalledProcessError:
            append_faulty(author)
            break

        data_root = dir1 / author
        all_good = True
        ## checking if CFG files have been generated
        for prob in data_root.iterdir():
            cfg_dir = prob / f"{prob.name}_{author}_bjoernDisassembly" / f"{prob.name}_{author}CFG"
            if not cfg_dir.is_dir() or not any(cfg_dir.iterdir()):
                append_faulty(author)
                all_good = False
        if all_good or tries >= 2:
            break

    target = dir3 / author
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree((dir1 / author), target)

if dir1.exists():
    shutil.rmtree(dir1)
dir3.rename(dir1)
