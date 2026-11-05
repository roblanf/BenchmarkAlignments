#!/usr/bin/env python3
"""Rebuild summary.csv (one row per dataset) from the files in datasets/.

Usage:
    python build_summary_csv.py [--repo DIR]

Sources per dataset: README.yaml (metadata), charset.csv (partition and genome counts),
alignment.nex-summary.txt (AMAS statistics). The alignment itself is not needed, so this
runs on a plain checkout of the repository.
"""
import argparse
import glob
import os

import pandas as pd
import yaml

AMAS_COLS = ["No_of_taxa", "Alignment_length", "Total_matrix_cells", "Undetermined_characters",
             "Missing_percent", "No_variable_sites", "Proportion_variable_sites",
             "Parsimony_informative_sites", "Proportion_parsimony_informative",
             "AT_content", "GC_content"]
GENOMES = ["mitochondrial", "nuclear", "chloroplast", "bacterial", "dsDNA", "ssDNA", "dsRNA", "ssRNA"]


def dataset_row(folder):
    name = os.path.basename(folder)
    y = yaml.safe_load(open(os.path.join(folder, "README.yaml")))
    st, ds = y["study"], y["dataset"]
    cs = pd.read_csv(os.path.join(folder, "charset.csv"))
    am = pd.read_csv(os.path.join(folder, "alignment.nex-summary.txt"), sep="\t").iloc[0]
    row = {"name": name,
           "datatype": "protein" if (cs.data_type == "AA").all() else "nucleotide",
           "ntax": int(am.No_of_taxa),
           "nchar": int(am.Alignment_length),
           "n_partitions": len(cs),
           "n_loci": cs.locus_name.nunique(),
           "codon_positions_annotated": bool(cs.codon_position.astype(str).str.match(r"^[123]").any())}
    for g in GENOMES:
        row[f"genome_{g}"] = bool((cs.genome == g).any())
    for c in AMAS_COLS[2:]:
        row[c] = am.get(c, "")
    dt = ds["divergence time"]
    row.update({
        "study_reference": st["reference"], "study_year": st["year"], "study_DOI": st["DOI"],
        "dataset_DOI": ds["DOI"], "license": ds["license"], "figshare": ds["figshare"],
        "used_for_concatenated_tree": ds["used for tree inference"]["concatenated"],
        "used_for_locus_trees": ds["used for tree inference"]["locus trees"],
        "clade_latin": ds["study clade"]["latin"], "clade_english": ds["study clade"]["english"],
        "clade_taxon_ID": ds["study clade"]["taxon ID"],
        "divergence_time_source": dt["source"], "divergence_time_median": dt["median age"],
        "divergence_time_min": dt["min age"], "divergence_time_max": dt["max age"],
        "divergence_time_n_chronograms": dt["N chronograms"],
        "study_root_age": ds["study root age"],
        "n_outgroups": 0 if ds["outgroups"] == "NA" else len([t for t in ds["outgroups"].split(",") if t.strip()]),
        "alignment_file": ds["dataset curation"]["alignment file"],
        "notes": ds["notes"],
    })
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    args = ap.parse_args()
    folders = sorted(glob.glob(os.path.join(args.repo, "datasets", "*", "README.yaml")))
    rows = [dataset_row(os.path.dirname(f)) for f in folders]
    df = pd.DataFrame(rows)
    out = os.path.join(args.repo, "summary.csv")
    df.to_csv(out, index=False)
    print(f"wrote {out}: {len(df)} datasets, {df.n_partitions.sum()} partitions, "
          f"{df.nchar.sum()} sites, {int(df.Total_matrix_cells.sum())} cells")


if __name__ == "__main__":
    main()
