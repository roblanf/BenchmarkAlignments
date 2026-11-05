# New dataset files

`README.yaml` in this folder is the template for a dataset's metadata. Copy it to
`datasets/<Name>/README.yaml` and fill in every field; the text in brackets says what goes
where. Do not add, remove or rename keys: `utility_scripts/validate_dataset.py` enforces the
structure.

The complete procedure for adding a dataset, including how to build `alignment.nex`, verify
codon positions, and look up divergence times, is in `../docs/ADDING_A_DATASET.md`.
