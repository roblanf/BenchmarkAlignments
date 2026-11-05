# Adding a dataset

This is the complete procedure. It is written so that an agent (or a person) can follow it
without further guidance. Every step produces something checkable. Where a step needs a
judgement, the judgement and its basis are written into `README.yaml`.

Terms: the **study** is the paper; the **dataset** is the archived data the paper points to;
the **ingroup** is the clade the study is about, excluding outgroups.

## 0. What qualifies

- A published study with a DOI.
- An alignment archived with its own DOI (Dryad, Zenodo, figShare, etc.) under CC0 or CC-BY.
  Supplementary files hosted on a journal website do not qualify. Nor do GitHub repositories
  unless they are archived with a DOI.
- Partition information: which sites are which locus, and for protein-coding DNA, codon
  positions. If the archive has no partition file, the information must be reconstructable
  from the paper or supplement (for example a table of gene boundaries). If it cannot be,
  stop and tell Rob.

## 1. Set up

```bash
cd /path/to/BenchmarkAlignments && git pull
git worktree add -b dataset/<Name> ../BenchmarkAlignments-<Name> main   # Name = FirstAuthor_Year
cd ../BenchmarkAlignments-<Name>        # work here; the main working tree is never switched
mkdir datasets/<Name>
mkdir -p $BENCHALN_DATA/<Name> $BENCHALN_DATA/_sources/<Name>
```

Get the paper and supplement PDFs into `datasets/<Name>/` (gitignored):

```bash
python utility_scripts/fetch_paper.py 10.1038/s41586-024-07324-0 <Name>
```

This resolves the DOI to a PubMed Central id and downloads the article PDF
(`<Name>_paper.pdf`) and every supplementary file from PMC's open-access bucket. It works
for open-access papers and for NIH-funded author manuscripts. If it reports that the paper
is not in PMC, ask Rob: he drops PDFs in `pdfs/` at the repository root; move them into the
dataset folder and name them `<Name>_paper.pdf` and `<Name>_supplement.pdf`. Publisher
sites block scripted downloads, so do not persist with them. Do not proceed to step 3 until
you have the paper and its supplements.

Data archives: Zenodo and figShare can be downloaded by script (see `_sources/` under
`$BENCHALN_DATA`); Dryad blocks scripts, so ask Rob to download Dryad archives into
`$BENCHALN_DATA/_sources/<Name>/`. Download the data archive into `$BENCHALN_DATA/_sources/<Name>/`, in its own
empty folder, and keep it: it is the provenance.

## 2. Read the paper

Read the whole paper and every relevant supplement, not just the methods, and read the
metadata page of the data repository (file list, descriptions, licence). Nothing goes into
`README.yaml` before this is done: every field is either read from these sources or
computed from the alignment. In particular, do not infer `used for tree inference` from the
headline method; a coalescent study may still concatenate loci for branch lengths or
dating, and a concatenation study may also report gene trees. You are looking for:

- Which alignment in the archive was used for the main tree (usually figure 1 or 2).
- Taxon sampling, outgroups, and whether any taxa were removed before analysis.
- How loci were defined and whether protein-coding loci were kept in frame.
- Whether single-locus (gene) trees were inferred.
- The genome of origin of each locus (nuclear, mitochondrial, chloroplast, bacterial, or a
  viral genome type).
- Any root age estimate reported by the study (text, a figure, or a table).
- For viruses or ancient DNA, the sampling date of each sequence.

Write the answers down as you go; they go into `README.yaml`.

## 3. Choose the alignment

Pick the alignment used for the study's main result. If there are several candidates (for
example DNA and amino acid versions, or trimmed and untrimmed), pick one and record why in
`dataset curation / justification`. A second version may become a second dataset
(`<Name>_aa`, `<Name>_dna`) as in Cannon_2016. Prefer the version with the most taxa and
loci that the study actually analysed.

## 4. Build `alignment.nex`

The target format is exactly that of `datasets/Anderson_2013` (see `$BENCHALN_DATA`). Use
`utility_scripts/build_alignment_nex.py` to create it from either a concatenated alignment
plus a partition table, or a folder of single-locus alignments. It writes the DATA block,
the SETS block with `loci` and `genomes` charpartitions, the `outgroups` taxset, and an
optional SAMPLINGDATES block.

Conventions the validator enforces:

- DATA block first, `datatype=nucleotide` or `protein`, `missing=? gap=-`, non-interleaved.
- Charset names: a locus is `NAME`; a protein-coding DNA locus is `NAME_1stpos`,
  `NAME_2ndpos`, `NAME_3rdpos` with stride 3 (stride 2 if the source deliberately excludes a
  codon position; say so in notes).
- `CHARPARTITION loci` lists every locus charset; together they cover every site exactly once.
- Genome charsets are named `<genome>_genome` with genome in: mitochondrial, nuclear,
  chloroplast, bacterial, dsDNA, ssDNA, dsRNA, ssRNA. `CHARPARTITION genomes` covers every
  site exactly once.
- `TAXSET outgroups` names at least one taxon, unless the data are tip-dated and carry a
  SAMPLINGDATES block.
- Taxon names use only `A-Z a-z 0-9 _ .` (no hyphens: Biopython reads an unquoted hyphen as a gap). The build script sanitises names and prints the
  changes; copy that list into `dataset curation / sequence edits`.
- Unix line endings. No duplicate taxon names.

Do not edit sequences. If a taxon must be dropped (for example it is in the archive but not
in the published tree), say exactly which and why in `sequence edits`.

## 5. Verify codon positions

For any nucleotide dataset with protein-coding loci:

```bash
python utility_scripts/check_codon_frames.py datasets/<Name> --table <genetic code>
```

Every gene must come out `OK`: near-zero internal stops in the annotated frame, more in the
other two. If a gene fails, the frame in the source partition file is wrong or the gene
starts mid-codon; fix the charset starts and re-run. Paste the output table into the PR.
Use the right genetic code (1 standard, 2 vertebrate mito, 5 invertebrate mito, 11
bacterial and plastid); if loci come from different genomes, run once per genome with
`--genes`.

## 6. Divergence time

Choose two or three species in the ingroup from its most distantly related lineages, so that
their most recent common ancestor is the ingroup root. Then:

```bash
Rscript utility_scripts/datelife_query.R --yaml "Species one" "Species two" "Species three"
```

Paste the printed block into `README.yaml`. If DateLife returns nothing, try different or
more species, and try genus names. If it still returns nothing, set `source: NA` for all
fields, say so in notes, and tell Rob. Separately, if the study reports a root age for the
ingroup, put it in `study root age` and cite the figure or table in notes. If it does not,
`study root age: NA` is correct.

## 7. Fill `README.yaml`

Copy `new_dataset_files/README.yaml` and fill every field. The brackets describe each one.
Specific rules:

- `reference`: Vancouver style from Google Scholar's "cite".
- `DOI` fields start with `doi.org/`, no scheme. Study and dataset DOIs differ.
- `license`: read it from the archive page. Dryad is CC0, figShare and Zenodo show the
  licence on the record. CC-BY is written `CCBY`.
- `figshare: NA` (Rob fills it after upload).
- `dataset curation`: the exact path inside the archive of the file you used; where the
  partitions came from; why this alignment; every edit you made.
- `outgroups`: the same names, comma-separated, as the TAXSET.
- `study clade / taxon ID`: the NCBI Taxonomy id of the smallest clade containing the
  ingroup. Check it resolves.
- `notes`: anything a user would want to know. Mention excluded codon positions, tip
  dating, taxa removed, and which of several archive files this is.

## 8. Generate the derived files and validate

```bash
python utility_scripts/generate_charset_csv.py datasets/<Name>
python utility_scripts/generate_summaries.py   datasets/<Name> --cores 8
python utility_scripts/validate_dataset.py     datasets/<Name>      # network on
python utility_scripts/build_summary_csv.py
cd utility_scripts && pytest -q tests/ -k <Name>
```

All errors must be fixed. Warnings must each be either fixed or explained in the PR.

## 9. Hand over

Only when step 8 passes in full with network checks on, and nothing about the dataset is
waiting on Rob, open a pull request from `dataset/<Name>` to `main` containing the four tracked files and
the regenerated `summary.csv`. The PR description lists: the archive file used, every
judgement call, every sequence edit, the codon-frame table, the DateLife output, and any
warnings. Say that the alignment is at `$BENCHALN_DATA/<Name>/alignment.nex` and needs
uploading to figShare. Rob reviews, uploads, fills `figshare`, and merges.

## What NA means

NA is a positive statement that the value does not exist, not that nobody looked:
`study root age: NA` means the paper reports no root age. `outgroups: NA` means the data
are tip-dated and need no outgroup. `sequence edits: NA` means no edits were made. The only
fields where NA is allowed because the information could not be obtained are in
`divergence time`, and then notes must say DateLife returned nothing. For everything else,
if you cannot find the value, ask Rob rather than writing NA.
