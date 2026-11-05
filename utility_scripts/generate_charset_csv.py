#!/usr/bin/env python3
"""Write charset.csv for a dataset from the SETS block of its alignment.nex.

Usage:
    python generate_charset_csv.py DATASET_FOLDER [--data-dir DIR] [--force]

charset.csv has one row per charset in CHARPARTITION loci, in the same order, with the
genome of each charset taken from CHARPARTITION genomes. Columns:

    alignment_name, partition_name, charset_definition, partition_start, partition_end,
    partition_skip, locus_name, codon_position, genome, data_type

charset_definition is the NEXUS definition verbatim (e.g. "1-1592\\3" or "10-20 35-40") and is
authoritative. start/end/skip are filled only for simple start-end\\skip charsets and are NA
for multi-range charsets.

The file is the tabular, machine-friendly twin of the SETS block; validate_dataset.py
checks the two agree.
"""
import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_dataset import (CODON_SUFFIXES, CHARSET_CSV_COLUMNS, GENOME_CHARSETS,  # noqa: E402
                              _parse_sets_block, find_alignment)
from Bio.Nexus import Nexus  # noqa: E402


def build_rows(aln_path, dataset_name):
    text = open(aln_path, encoding="utf-8", errors="replace").read()
    charsets, charpartitions, _ = _parse_sets_block(text)
    if charpartitions is None or set(charpartitions) != {"loci", "genomes"}:
        raise ValueError("alignment.nex needs CHARPARTITIONs 'loci' and 'genomes'")
    aln = Nexus.Nexus(aln_path)
    site_genome = {}
    for g in charpartitions["genomes"]:
        if g not in GENOME_CHARSETS:
            raise ValueError(f"genome charset {g} is not one of {sorted(GENOME_CHARSETS)}")
        for s in aln.charsets[g]:
            site_genome[s] = g[: -len("_genome")]
    data_type = "AA" if aln.datatype == "protein" else "DNA"
    rows = []
    for name in charpartitions["loci"]:
        sites = aln.charsets[name]
        definition = charsets[name].rstrip(";").strip()
        start, end = sites[0] + 1, sites[-1] + 1
        skip = (sites[1] - sites[0]) if len(sites) > 1 else 1
        if sites != list(range(sites[0], sites[-1] + 1, skip)):
            start = end = skip = "NA"  # multi-range charset; charset_definition is authoritative
        suffix = next((s for s in CODON_SUFFIXES if name.endswith(s)), None)
        locus = name[: -len(suffix)] if suffix else name
        codon = CODON_SUFFIXES.index(suffix) + 1 if suffix else "NA"
        genomes = {site_genome.get(s) for s in sites}
        if len(genomes) != 1 or None in genomes:
            raise ValueError(f"charset {name} spans more than one genome charset: {genomes}")
        rows.append([dataset_name, name, definition, start, end, skip, locus, codon, genomes.pop(), data_type])
    return pd.DataFrame(rows, columns=CHARSET_CSV_COLUMNS)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--data-dir", default=os.environ.get("BENCHALN_DATA"))
    ap.add_argument("--force", action="store_true", help="overwrite an existing charset.csv")
    args = ap.parse_args()
    folder = os.path.abspath(args.folder.rstrip("/"))
    name = os.path.basename(folder)
    out = os.path.join(folder, "charset.csv")
    if os.path.exists(out) and not args.force:
        sys.exit(f"{out} exists; use --force to overwrite")
    aln_path = find_alignment(folder, args.data_dir)
    if aln_path is None:
        sys.exit("alignment.nex not found")
    df = build_rows(aln_path, name)
    df.to_csv(out, index=False)
    print(f"wrote {out} ({len(df)} charsets)")


if __name__ == "__main__":
    main()
