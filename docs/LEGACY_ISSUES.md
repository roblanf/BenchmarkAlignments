# Issues found in the 2019 datasets during the November 2025 migration

The validator (`utility_scripts/validate_dataset.py`) was run over all 67 datasets from the
2019 figShare archive. Fixes applied to the alignment files are listed first; the original
file is kept beside each one as `alignment.nex.orig2019` in the data folder. Open items need
a decision or information from the papers.

## Fixed in the alignments (outside git, in `$BENCHALN_DATA`)

| Dataset | Problem | Fix |
|---|---|---|
| Chen_2015, Worobey_2014a-h | Classic Mac line endings (`\r`) | converted to `\n` |
| Worobey_2014a-h | genome charset named `ssRNA` | renamed `ssRNA_genome` |
| Worobey_2014a-h | no SAMPLINGDATES block although every name carries its year | block added from the year field of each name |
| Broughton_2013 | charset typo `btbd7_2nspos` | renamed `btbd7_2ndpos` |
| Murray_2013 | charset typo `COII_1stpost` | renamed `COII_1stpos` |
| Ran_2018_aa | `CHARPARTITION loci` used site ranges, not charset names | rebuilt from the charsets |

## Fixed in the repository

| Dataset | Problem | Fix |
|---|---|---|
| Becker_2016 | stray file `Find Results` | deleted |
| Irisarri_2017, Murray_2013, Nguyen_2016a-f, Siler_2013, Unmack_2013, Varga_2019, Worobey_2014e/f/h | AMAS summaries did not match the alignment | regenerated |
| all | `dx.doi.org` prefixes | normalised to `doi.org` |

## Open: need a decision or the paper

1. **Empty outgroups** in Becker_2016, Faircloth_2013, Smith_2014, Varga_2019. These fail
   validation. Varga's notes say the outgroups could not be identified from the paper.
   Needs the PDFs, or a decision to accept an empty taxset with a note.
2. **Duplicate taxon names**: Irisarri_2017 has two copies each of Lepisosteus, Pelophylax,
   Protopterus and Typhlonectes; Varga_2019 has two `Boletus_sp`. Biopython silently renames
   the second copy; AMAS silently drops it. The original archives presumably have distinct
   names. Needs the source data to restore them, or a rename with a note.
3. **Taxon names needing quotes** (spaces, dots, `|`, `/`): Nguyen_2016a-f (`A. pisum`),
   Varga_2019 (three names), Worobey_2014a-h (`1935|Avian|A/chicken/Brescia/1902|Italy|H7N7`).
   Legal NEXUS, but awkward downstream. Proposed: sanitise to underscores and record in
   `sequence edits`. The Worobey year field is preserved in SAMPLINGDATES either way.
4. **Codon positions partly present**: Cannon_2016_dna (1st+2nd only, by design, in notes),
   Broughton_2013 btbd7 (1st and 3rd only), Murray_2013 COII (2nd and 3rd only). The last
   two look like curation slips rather than design; needs the partition files from the
   archives.
5. **figshare links** are NA for all 67 until the per-file links are collected from the
   figShare record.
6. **Provenance fields** (`dataset curation`) are NA for all 67 with a note. Filling them
   means re-opening each archive; low priority.
7. **study root age** is NA for most; filling it needs the PDFs (Rob is adding these).
8. **Divergence time** for datasets with a 2019 TimeTree value keeps that value with
   `source: timetree.org`. Replacing them with DateLife queries is a mechanical job once
   query taxa are chosen per dataset.
