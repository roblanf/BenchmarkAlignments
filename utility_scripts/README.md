# Utility scripts

All scripts run in the `benchaln` conda environment (see `../environment.yml`) and take a
dataset folder as their main argument. Alignments are gitignored, so scripts find
`alignment.nex` either in the dataset folder or in `$BENCHALN_DATA/<Name>/`.

The procedure for adding a dataset is in `../docs/ADDING_A_DATASET.md`. In pipeline order:

| Script | Purpose |
|---|---|
| `build_alignment_nex.py` | Build a conforming `alignment.nex` from a concatenated alignment plus a partition table, or from a folder of single-locus files. Sanitises taxon names and reports the changes. |
| `check_codon_frames.py` | Verify `_1stpos/_2ndpos/_3rdpos` annotations by translating in all three frames and counting stop codons. |
| `datelife_query.R` | Query DateLife for the MRCA age of a set of taxa; `--yaml` prints a block for `README.yaml`. |
| `generate_charset_csv.py` | Write `charset.csv` from the SETS block. |
| `generate_summaries.py` | Write the two AMAS summary files (uses the bundled `AMAS.py`). |
| `validate_dataset.py` | Run every check on one dataset. Non-zero exit on any error. `--no-network` skips DOI and NCBI lookups. |
| `build_summary_csv.py` | Rebuild `../summary.csv` from all datasets. |
| `tests/` | `pytest -q tests/` validates every dataset; `-k Name` for one. |
| `gzip_datasets.py` | Make `<Name>.tar.gz` archives for figShare. |
| `split_into_loci.py` | For users: split database alignments into single-locus files. |
| `install_datelife.R` | Install DateLife into the env (not available on conda). |
| `migrate_yaml_2025.py` | One-off: convert a 2019-schema `README.yaml` to the current schema. |

Quick check of the whole database without network access:

```bash
export BENCHALN_DATA=/path/to/alignments
cd utility_scripts && pytest -q tests/ --no-network
```
