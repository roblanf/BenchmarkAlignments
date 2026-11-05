# Potential datasets

A running log of every published dataset considered for this repository, and whether it can
be used. `potential_datasets.csv` has one row per study. Agents extend it; nothing here is ever deleted, so that the
next agent does not re-check the same study. The rules below were agreed with Rob on
2025-11-05 and are the criteria for a row.

## What we are looking for

- Published in a good journal (Systematic Biology, MBE, Nature/Science family, PNAS,
  Current Biology, Evolution, MPE, GBE, PLOS, Cladistics, Systematic Entomology, American
  Journal of Botany, New Phytologist, and comparable). Preprints do not qualify until published.
- Published 2019 or later (the current collection stops at 2019).
- The **alignment itself** archived with its own DOI (Dryad, Zenodo, figShare, OSF, etc.)
  under CC0 or CC-BY. Journal supplementary files and bare GitHub repositories do not count.
  Archives of raw reads or unaligned sequences only do not count.
- Partition information present or reconstructable: which sites belong to which locus, and
  for protein-coding DNA, codon positions (or at least gene boundaries from which frames can
  be verified by translation).
- Big is better: many taxa, many loci, or both. There is no size cap.
- Any taxon. No preference for filling taxonomic gaps; the spread will follow who shares data.
- Not already in `datasets/` (check `summary.csv` for the study DOI).

## How to use the CSV

1. Before checking a study, search the CSV for its DOI. If it is there, do not repeat the work.
2. Add a row as soon as a study is considered, even if it is rejected; record why in `notes`.
3. Verification means: the repository API (Zenodo, Dryad, figShare) was queried for the file
   list and licence, and the archive was downloaded into a scratch directory and inspected
   to confirm an alignment and partition information exist. Dryad blocks scripted downloads;
   for those set `status` to `needs_manual_download` and ask Rob to fetch the archive.
4. Downloaded archives are scratch; do not put them in the repo or in `$BENCHALN_DATA`
   until the dataset is actually being added (see `docs/ADDING_A_DATASET.md`).
5. Never guess a licence or a file name: read it from the repository record.
6. Priority is size: first look for studies with more than about 100 taxa and 500 loci, or
   more than about 1 Mb of alignment. Still log smaller studies you come across.
7. Hard rule: dataset search work touches only this folder. Everything else (downloads,
   scripts, notes) lives in scratch space outside the repository. Commit to `main` directly.

## Columns

| column | meaning |
|---|---|
| `name` | `FirstAuthor_Year`, the name the dataset would get in `datasets/` |
| `status` | `candidate` (found, not verified), `verified` (archive inspected, usable), `needs_manual_download` (Dryad etc.), `rejected`, `added` (now in `datasets/`) |
| `study_DOI` | `doi.org/...` of the paper |
| `journal` | journal name |
| `year` | year of publication |
| `clade` | the ingroup, in one or two words |
| `type` | the broad data-generation approach, one token: `AHE`, `UCE`, `transcriptome`, `exon_capture`, `plastome`, `mitogenome`, `genome`, `Sanger`, `mixed` |
| `DNA_alignment` | `yes` or `no`: the archive holds a nucleotide alignment |
| `AA_alignment` | `yes` or `no`: the archive holds an amino-acid alignment |
| `ntax` | number of taxa in the candidate alignment, or `unknown` |
| `nloci` | number of loci, or `unknown` |
| `nchar` | alignment length in sites, or `unknown` |
| `locus_type` | finer description of the loci than `type`, e.g. `AHE+transcriptome`, `UCE`, `exons`, `rRNA` |
| `dataset_DOI` | `doi.org/...` of the data archive |
| `repository` | `Dryad`, `Zenodo`, `figshare`, `OSF`, ... |
| `license` | `CC0`, `CCBY`, or exactly what the record says if neither |
| `alignment_file` | path inside the archive of the alignment to use, or `unknown` |
| `partition_info` | path inside the archive of the partition file, or how it would be reconstructed, or `none` |
| `archive_size_MB` | size of the archive as reported by the repository |
| `date_checked` | YYYY-MM-DD |
| `checked_by` | `agent` or `rob` |
| `notes` | why it was rejected, caveats, anything the next agent needs |
