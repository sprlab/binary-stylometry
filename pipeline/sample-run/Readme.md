# Sample-Run

This folder contains a minimal test case using a small subset of authors from the dataset. To verify that the pipeline is configured correctly, run it using the dataset provided in the `sample-dataset` folder.

## Sample Authors
The following five authors were selected from the dataset:
- `2011aad`
- `Murat`
- `mavd09`
- `meobeo`
- `sevenkpl`

## Expected Output 

Running the `end_to_end.sh` script should generate the prediction file `results/5_authors.txt` in the `pipeline/results` directory, matching the format and predictions of `sample-results/5_authors.txt`. Note that confidence values may vary slightly.