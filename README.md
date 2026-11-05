# BenchmarkAlignments

## What's this?

A curated repository of DNA and amino acid alignments with comprehensive metadata.

## What's it for?

To test, verify, benchmark, and compare software and methods in phylogenetics.

## How many datasets, how big?

See `summary.csv`, which has one row per dataset with the alignment statistics and the key
metadata. As of November 2025 the database contains:

* 67 datasets
* 66,934 partitions
* 31,971,550 alignment columns
* 2,623,278,645 alignment matrix cells

## Getting the data

The alignments are stored on figShare (about 1 GB in total), one `.tar.gz` per dataset:
https://figshare.com/s/622e9e0a156e5233944b. Click 'Download All' and extract each archive,
or from the command line:

```shell
mkdir BenchmarkAlignments_data && cd BenchmarkAlignments_data
curl -L "https://ndownloader.figshare.com/articles/7092356?private_link=622e9e0a156e5233944b" > BenchmarkAlignments.zip
unzip BenchmarkAlignments.zip
find . -name "*.tar.gz" -exec tar xzf {} \;
rm *.tar.gz BenchmarkAlignments.zip
```

You now have one folder per dataset, e.g. `Anderson_2013`.

## What's in each folder?

1. `README.yaml`: metadata on the study and the dataset: references and DOIs, licence,
   which file in the original archive the alignment came from and why, what was edited,
   outgroups, the clade and its NCBI taxon ID, and divergence-time estimates (from DateLife
   and from the study itself). The template with field descriptions is
   `new_dataset_files/README.yaml`.
2. `alignment.nex`: the alignment in non-interleaved NEXUS format, with a SETS block
   defining every locus (codon positions separated for protein-coding DNA), the genome each
   site comes from, and the outgroup taxa. Tip-dated datasets also carry a SAMPLINGDATES block.
3. `charset.csv`: the same partition information as a table, one row per charset, with
   locus name, codon position and genome.
4. `alignment.nex-summary.txt` and `alignment.nex-seq-summary.txt`: statistics on the whole
   alignment and on each sequence, from [AMAS](https://github.com/marekborowiec/AMAS).

This repository tracks everything except the alignments and the papers.

## Can I use these datasets?

Yes. All of the original datasets are publicly archived under CC0 or CC-BY. Everything here
that is not a dataset (`summary.csv`, the `README.yaml` files, the code) is CC-BY.

## Attribution

If you use any of the datasets, please cite three things:

1. The original study (reference and DOI in `README.yaml` and `summary.csv`).
2. The dataset itself (DOI in `README.yaml` and `summary.csv`).
3. This repository (github.com/roblanf/BenchmarkAlignments).

This rewards the people who spend months in the field and the lab and then share their data.

## I want individual loci, not concatenated alignments

```shell
python3 utility_scripts/split_into_loci.py -i INPUT_FOLDER -o OUTPUT_FOLDER
```

This writes one NEXUS file per locus, named `<dataset>_<locus>`, merging codon-position
charsets back into whole genes and ignoring genome charsets. Note that what a 'locus' is
differs between datasets (a transcript, an exon, a UCE); see the original papers.

## Adding a dataset

Read `docs/ADDING_A_DATASET.md`. In short: create the `benchaln` conda environment from
`environment.yml`, build a conforming `alignment.nex`, verify codon positions by
translation, look up divergence times with DateLife, fill `README.yaml`, and run
`utility_scripts/validate_dataset.py` until it passes. Known issues with the older datasets
are listed in `docs/LEGACY_ISSUES.md`.

## I have something to say

Errors, bugs, suggested datasets or features: https://github.com/roblanf/BenchmarkAlignments/issues
