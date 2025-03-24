# Erroneous Disassembly Analysis Script

This folder contains code and data that demonstrates **erroneous disassembly** in action using an example. This example is taken from best performing 20-author dataset (20_3) and its top fold (5).

#### Overview

The provided script `analysis.py` does the following:

- Analyzes features that correspond to erroneous disassembly of the source filename (containing author name).
- Processes a snippet of the disassembly file related to the erroneous disassembly containing author name.
- Converts the machine code into its ASCII representation.
- Generates instruction line bigrams from the instruction code associated with the machine code.
- Maps those instructions back to the feature file used by the top performing 20-author model (fold_5).

#### Usage

```sh
python3 analysis.py

```