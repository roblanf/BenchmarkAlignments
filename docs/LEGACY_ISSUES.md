# Issues found in the 2019 datasets during the November 2025 migration

The validator (`utility_scripts/validate_dataset.py`) was run over all 67 datasets from the
2019 figShare archive. Fixes applied to the alignment files are listed first. Open items are tracked as GitHub
issues labelled `legacy-data`.

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
| Nguyen_2016a-f, Varga_2019, Worobey_2014a-h | taxon names with spaces, dots, `|`, `/`, `-`, `!` | sanitised to underscores, recorded in `sequence edits` |
| Irisarri_2017, Murray_2013, Nguyen_2016a-f, Siler_2013, Unmack_2013, Varga_2019, Worobey_2014e/f/h | AMAS summaries did not match the alignment | regenerated |
| all | `dx.doi.org` prefixes | normalised to `doi.org` |

## Open

1. **Empty outgroups**: Becker_2016 (#61), Faircloth_2013 (#62), Smith_2014 (#63),
   Varga_2019 (#64). Need the papers.
2. **Duplicate taxon names**: Irisarri_2017 (#65), Varga_2019 (#66). Need the source archives.
3. **Codon positions partly present**: Broughton_2013 btbd7 (1st and 3rd only) and
   Murray_2013 COII (2nd and 3rd only) look like curation slips; Cannon_2016_dna (1st and
   2nd only) is by design. To be checked against the Dryad archives and papers. Dryad blocks
   automated downloads (HTTP 403), so the archives have to be fetched in a browser.
4. **figshare links** are NA for all 67 until the per-file links are collected from the
   figShare record.
5. **Provenance fields** (`dataset curation`) are NA for all 67 with a note. Filling them
   means re-opening each archive; low priority.
6. **study root age** is NA for most; filling it needs the PDFs.
7. **Divergence time** for datasets with a 2019 TimeTree value keeps that value with
   `source: timetree.org`. Replacing them with DateLife queries is a mechanical job once
   query taxa are chosen per dataset.
