"""
This script demonstrates erroneous disassembly in action using an example.

- It analyzes features that correspond to erroneous disassembly of the source filename (containing author name).
- It processes a snippet of the disassembly file that corresponds to erroneous disassembly of the source filename.
- It converts the machine code of the erroneous disassembly file into its ASCII representation.
- It generates instruction line bigrams from the instruction code associated with the machine code.
- It maps those instructions back to the features in the feature file used by the best performing 20-author model (fold_5).

"""

import sys
import re

def replace_hex_numbers(instruction):
    return re.sub(r'0x[0-9a-fA-F]+', 'hexadecimal', instruction)

def find_bigram_in_file(feature_file, bigram_string):
    with open(feature_file, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()[:203]]  

    for line  in lines:
        if bigram_string in line:
            print('======')
            print(f"Bigram found in feature file: {feature_file},\n"
            f"Bigram: {bigram_string}\n"
            f"Feature: {line}\n")
                
            print('======')


def hex_to_ascii_and_bigrams(file_path, feature_file):
    ascii_string = ""
    instructions = []

    with open(file_path, "r") as file:
        for line in file:
            parts = line.split(maxsplit=2) 
            if len(parts) < 3:
                continue  

            hex_bytes = parts[1]  
            instruction = replace_hex_numbers(parts[2])  
            instructions.append(instruction.strip())  

            try:
                ascii_string += bytes.fromhex(hex_bytes).decode()  
            except ValueError:
                continue  

    print(f"\nDecoded ASCII String of corresponding Machine Code in disassembly snippet file: {file_path}:")
    print(f'"{ascii_string}"')

    print("\nDisassembly Instruction Line Bigrams of corresponding Machine Code:")
    bigrams = []
    for instr1, instr2 in zip(instructions, instructions[1:]):
        instr_bigram = f"{instr1} {instr2}"
        bigrams. append(instr_bigram)

    
        print("Instr bigram:", instr_bigram)
    print(f"\nTrying to find the line bigram instruction features in the feature file {feature_file}.\n")
    for bigram in bigrams:
        find_bigram_in_file(feature_file, bigram)


if __name__ == "__main__":
    disassembly_snippet = "5654742835396608_kicius_errnoneous_part.dis"
    feature_file = "20_3_fold_5_train.arff"
    hex_to_ascii_and_bigrams(disassembly_snippet, feature_file )


