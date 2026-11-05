#!/usr/bin/env python3
"""Build a conforming alignment.nex from one concatenated alignment plus a partition table,
or from a folder of single-locus alignments.

Usage (concatenated alignment + partitions):
    python build_alignment_nex.py --alignment aln.phy --format phylip --datatype nucleotide \
        --partitions partitions.csv --genome nuclear --outgroups Taxon_A Taxon_B -o alignment.nex

Usage (one file per locus; concatenated in sorted file-name order):
    python build_alignment_nex.py --loci-dir loci/ --format fasta --datatype protein \
        --genome nuclear --outgroups Taxon_A -o alignment.nex

partitions.csv (for --alignment) has columns: name, start, end, codon (0 or 1), genome (optional).
Ranges are 1-based inclusive. codon=1 produces NAME_1stpos/_2ndpos/_3rdpos charsets with
stride 3 starting at start, start+1, start+2 (so start must be a first codon position; shift it
if the source gene starts mid-codon and say so in README.yaml). --genome gives the genome for
rows without one. Taxon names are sanitised to [A-Za-z0-9_.]; the sanitisation table is
printed so it can be recorded in README.yaml under 'sequence edits'.

For --loci-dir, loci are concatenated in sorted file-name order; taxa missing from a locus
are filled with '?'. Charset names come from the file name without extension. Use
--codon to mark all loci as protein coding (codon position charsets), or give a partitions.csv
with a 'name' and 'codon' column to mark some.
"""
import argparse
import glob
import os
import re
import sys

import pandas as pd
from Bio import AlignIO

GENOMES = ["mitochondrial", "nuclear", "chloroplast", "bacterial", "dsDNA", "ssDNA", "dsRNA", "ssRNA"]


def sanitise(name):
    new = re.sub(r"[^A-Za-z0-9_.]", "_", name.strip().strip("'\""))
    return new


def read_alignment(path, fmt):
    aln = AlignIO.read(path, fmt)
    # for FASTA, Biopython's .id stops at the first space; use the whole header line
    return [((r.description if fmt == "fasta" else r.id), str(r.seq)) for r in aln]


def sites_of(definition):
    """1-based site list for a NEXUS charset definition like '1-12\\3 20-30'."""
    out = []
    for tok in definition.split():
        step = 1
        if "\\" in tok:
            tok, step = tok.split("\\")
            step = int(step)
        if "-" in tok:
            a, b = tok.split("-")
            out.extend(range(int(a), int(b) + 1, step))
        else:
            out.append(int(tok))
    return out


def ranges_of(sites):
    """Collapse a sorted list of 1-based sites into 'a-b c-d' with contiguous runs."""
    sites = sorted(set(sites))
    runs, start, prev = [], sites[0], sites[0]
    for x in sites[1:]:
        if x != prev + 1:
            runs.append((start, prev))
            start = x
        prev = x
    runs.append((start, prev))
    return " ".join(f"{a}-{b}" if a != b else str(a) for a, b in runs)


def write_nexus(out, records, datatype, loci, genome_of, outgroups, samplingdates=None):
    """loci: list of (name, definition) in order; genome_of: {locus name: genome}."""
    ntax, nchar = len(records), len(records[0][1])
    width = max(len(n) for n, _ in records) + 2
    with open(out, "w") as f:
        f.write("#NEXUS\nbegin DATA;\n")
        f.write(f"\tdimensions ntax={ntax} nchar={nchar};\n")
        f.write(f"\tformat datatype={datatype} missing=? gap=-;\n\tmatrix\n")
        for n, s in records:
            f.write(f"\t{n.ljust(width)}{s}\n")
        f.write("\t;\nend;\n\nbegin SETS;\n\n\t[loci]\n")
        for name, definition in loci:
            f.write(f"\tCHARSET {name} = {definition};\n")
        f.write("\n\tCHARPARTITION loci = " + ", ".join(f"{i+1}:{n}" for i, (n, _) in enumerate(loci)) + ";\n")
        f.write("\n\t[genomes]\n")
        # merge sites per genome
        per_genome = {}
        for name, definition in loci:
            per_genome.setdefault(genome_of[name], []).extend(sites_of(definition))
        gnames = []
        for g, sites in per_genome.items():
            gnames.append(g + "_genome")
            f.write(f"\tCHARSET {g}_genome = {ranges_of(sites)};\n")
        f.write("\n\tCHARPARTITION genomes = " + ", ".join(f"{i+1}:{n}" for i, n in enumerate(gnames)) + ";\n")
        f.write("\n\t[outgroups]\n\tTAXSET outgroups = " + " ".join(outgroups) + ";\n\nend;\n")
        if samplingdates:
            f.write(f"\nbegin SAMPLINGDATES;\n\tdimensions ntax={len(samplingdates)};\n\tunits = calendaryears;\n")
            for n, d in samplingdates:
                f.write(f"\t{n}, {d}\n")
            f.write("end;\n")


def codon_charsets(name, start, end):
    return [(f"{name}_1stpos", f"{start}-{end}\\3"), (f"{name}_2ndpos", f"{start+1}-{end}\\3"),
            (f"{name}_3rdpos", f"{start+2}-{end}\\3")]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--alignment", help="concatenated alignment file")
    src.add_argument("--loci-dir", help="folder of single-locus alignments")
    ap.add_argument("--format", default="fasta", help="Biopython AlignIO format (fasta, phylip, phylip-relaxed, nexus)")
    ap.add_argument("--datatype", choices=["nucleotide", "protein"], required=True)
    ap.add_argument("--partitions", help="partitions.csv (see --help)")
    ap.add_argument("--genome", choices=GENOMES, help="default genome for all loci")
    ap.add_argument("--codon", action="store_true", help="(--loci-dir) all loci are protein coding, in frame 1")
    ap.add_argument("--outgroups", nargs="+", required=True, help="outgroup taxon names (after sanitising)")
    ap.add_argument("--samplingdates", help="CSV with columns taxon,date for tip-dated data")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    parts = pd.read_csv(args.partitions) if args.partitions else None
    loci, genome_of = [], {}

    if args.alignment:
        records = read_alignment(args.alignment, args.format)
        if parts is None:
            sys.exit("--partitions is required with --alignment")
        for _, r in parts.iterrows():
            g = r.get("genome", args.genome) if "genome" in parts.columns and pd.notna(r.get("genome")) else args.genome
            if g not in GENOMES:
                sys.exit(f"no genome for partition {r['name']}")
            if int(r.get("codon", 0)) == 1:
                cs = codon_charsets(r["name"], int(r.start), int(r.end))
            else:
                cs = [(r["name"], f"{int(r.start)}-{int(r.end)}")]
            for n, d in cs:
                loci.append((n, d))
                genome_of[n] = g
    else:
        files = sorted(glob.glob(os.path.join(args.loci_dir, "*")))
        per_locus = []
        taxa = []
        for fpath in files:
            recs = read_alignment(fpath, args.format)
            per_locus.append((os.path.splitext(os.path.basename(fpath))[0], dict(recs), len(recs[0][1])))
            for n, _ in recs:
                if n not in taxa:
                    taxa.append(n)
        seqs = {t: [] for t in taxa}
        pos = 1
        codon_flags = {}
        if parts is not None and "codon" in parts.columns:
            codon_flags = dict(zip(parts["name"], parts["codon"]))
        for name, d, length in per_locus:
            for t in taxa:
                seqs[t].append(d.get(t, "?" * length))
            is_codon = args.codon or int(codon_flags.get(name, 0)) == 1
            cs = codon_charsets(name, pos, pos + length - 1) if is_codon else [(name, f"{pos}-{pos+length-1}")]
            g = args.genome
            if parts is not None and "genome" in parts.columns:
                gg = parts.loc[parts["name"] == name, "genome"]
                if len(gg) and pd.notna(gg.iloc[0]):
                    g = gg.iloc[0]
            if g not in GENOMES:
                sys.exit(f"no genome for locus {name}")
            for n, dd in cs:
                loci.append((n, dd))
                genome_of[n] = g
            pos += length
        records = [(t, "".join(seqs[t])) for t in taxa]

    # sanitise names
    renamed = []
    out_records = []
    for n, s in records:
        n2 = sanitise(n)
        if n2 != n:
            renamed.append((n, n2))
        out_records.append((n2, s))
    if len({n for n, _ in out_records}) != len(out_records):
        sys.exit("duplicate taxon names after sanitising; fix the source names first")
    missing_og = [o for o in args.outgroups if o not in {n for n, _ in out_records}]
    if missing_og:
        sys.exit(f"outgroups not in alignment: {missing_og}")
    sd = None
    if args.samplingdates:
        sdf = pd.read_csv(args.samplingdates)
        sd = [(sanitise(str(r.taxon)), r.date) for r in sdf.itertuples()]
    write_nexus(args.out, out_records, args.datatype, loci, genome_of, args.outgroups, sd)
    print(f"wrote {args.out}: {len(out_records)} taxa, {len(out_records[0][1])} sites, {len(loci)} charsets")
    if renamed:
        print(f"{len(renamed)} taxon names sanitised (record in README.yaml 'sequence edits'):")
        for a, b in renamed[:50]:
            print(f"  {a} -> {b}")
        if len(renamed) > 50:
            print(f"  ... and {len(renamed)-50} more")


if __name__ == "__main__":
    main()
