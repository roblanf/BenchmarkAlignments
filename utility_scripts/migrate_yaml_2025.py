#!/usr/bin/env python3
"""One-off migration of README.yaml files from the 2019 schema to the 2025 schema.

Usage:
    python migrate_yaml_2025.py DATASET_FOLDER [--data-dir DIR]

Safe to re-run: a file already in the new schema is left alone.

Mapping:
  * DOIs: 'dx.doi.org/' -> 'doi.org/'
  * 'used for tree inference: X' -> {concatenated: X, locus trees: no}
  * 'timetree root age' -> divergence time block with source 'timetree.org' (or 'NA')
  * 'alignment' and 'genomes' blocks are dropped: alignment.nex and charset.csv hold them
  * dataset curation fields are set to 'NA' with a note that provenance predates the schema
  * outgroups are copied from the TAXSET in alignment.nex
  * figshare is 'NA' until the per-dataset file link is filled in
"""
import argparse
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_dataset import _parse_sets_block, find_alignment  # noqa: E402

LEGACY_NOTE = ("Curated before the November 2025 schema: source file, partition provenance and "
               "sequence edits were not recorded at the time.")


def q(s):
    """Quote a YAML scalar string safely."""
    if s is None:
        return "NA"
    s = str(s)
    if s == "NA":
        return "NA"
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yn(b):
    return "yes" if b else "no"


def migrate(folder, data_dir):
    path = os.path.join(folder, "README.yaml")
    y = yaml.safe_load(open(path))
    ds, st = y["dataset"], y["study"]
    if "divergence time" in ds:
        print(f"{folder}: already migrated")
        return
    doi_s = st["DOI"].replace("dx.doi.org/", "doi.org/").replace("https://", "").replace("http://", "")
    doi_d = str(ds["DOI"]).replace("dx.doi.org/", "doi.org/").replace("https://", "").replace("http://", "")

    aln_path = find_alignment(folder, data_dir)
    outgroups = []
    if aln_path:
        _, _, taxsets = _parse_sets_block(open(aln_path, encoding="utf-8", errors="replace").read())
        outgroups = (taxsets or {}).get("outgroups", [])

    tt = ds.get("timetree root age", "NA")
    if tt == "NA" or tt is None:
        div = {"source": "NA", "query taxa": "NA", "date accessed": "NA", "median age": "NA",
               "min age": "NA", "max age": "NA", "N chronograms": "NA", "source studies": "NA"}
    else:
        div = {"source": "timetree.org", "query taxa": "NA", "date accessed": "NA", "median age": str(tt),
               "min age": "NA", "max age": "NA", "N chronograms": "NA", "source studies": "NA"}

    notes = ds.get("notes", "NA")
    notes = "NA" if notes in (None, "NA") else str(notes).strip()
    notes = LEGACY_NOTE if notes == "NA" else notes + " " + LEGACY_NOTE

    cl = ds["study clade"]
    out = f"""study:
    reference: {q(st["reference"])}
    year: {int(st["year"])}
    DOI: {doi_s}

dataset:
    DOI: {doi_d}
    license: {ds["license"]}
    figshare: NA
    dataset curation:
        alignment file: NA
        partition information: NA
        justification: NA
        sequence edits: NA
    used for tree inference:
        concatenated: {yn(ds["used for tree inference"])}
        locus trees: no
    divergence time:
        source: {div["source"]}
        query taxa: {div["query taxa"]}
        date accessed: {div["date accessed"]}
        median age: {div["median age"]}
        min age: {div["min age"]}
        max age: {div["max age"]}
        N chronograms: {div["N chronograms"]}
        source studies: {div["source studies"]}
    study root age: {ds.get("study root age", "NA")}
    study clade:
        latin: {q(cl["latin"])}
        english: {q(cl["english"])}
        taxon ID: {int(cl["taxon ID"])}
    outgroups: {q(", ".join(outgroups)) if outgroups else "NA"}
    notes: {q(notes)}
"""
    # round-trip check
    new = yaml.safe_load(out)
    assert new["study"]["year"] == st["year"]
    open(path, "w").write(out)
    print(f"{folder}: migrated ({len(outgroups)} outgroups)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="+")
    ap.add_argument("--data-dir", default=os.environ.get("BENCHALN_DATA"))
    args = ap.parse_args()
    for f in args.folders:
        migrate(os.path.abspath(f.rstrip("/")), args.data_dir)


if __name__ == "__main__":
    main()
