#!/usr/bin/env python3
"""Verify codon-position annotations in alignment.nex by translation.

Usage:
    python check_codon_frames.py DATASET_FOLDER [--data-dir DIR] [--table N] [--max-stop-frac 0.01]

For every gene with *_1stpos/_2ndpos/_3rdpos charsets, the sites of the three charsets are
re-assembled into codons in the annotated frame and translated with the given genetic code
(default 1, standard; use e.g. 5 for invertebrate mitochondrial, 2 for vertebrate
mitochondrial, 11 for bacterial/plastid). Codons containing gaps or ambiguities are skipped.

The fraction of internal stop codons is reported for the annotated frame and for the two
alternative frames. A correct annotation gives a near-zero stop fraction in the annotated
frame and clearly higher fractions in the other two. The script exits non-zero if any gene
fails that test, and prints a table you should paste into the curation notes or PR.

This replaces the old "translate it in Geneious and BLAST it" step.
"""
import argparse
import os
import sys
from collections import Counter

from Bio.Data import CodonTable
from Bio.Nexus import Nexus

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_dataset import CODON_SUFFIXES, find_alignment  # noqa: E402


def stop_fraction(seqs, sites, table):
    """sites: ordered list of 0-based columns in frame order (pos1,pos2,pos3,pos1,...)."""
    stops = total = 0
    stop_codons = set(table.stop_codons)
    for s in seqs:
        for i in range(0, len(sites) - 2, 3):
            codon = (s[sites[i]] + s[sites[i + 1]] + s[sites[i + 2]]).upper()
            if any(c not in "ACGT" for c in codon):
                continue
            total += 1
            if codon in stop_codons:
                stops += 1
    return stops, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--data-dir", default=os.environ.get("BENCHALN_DATA"))
    ap.add_argument("--table", type=int, default=1, help="NCBI genetic code id (default 1)")
    ap.add_argument("--max-stop-frac", type=float, default=0.01,
                    help="max fraction of internal stops tolerated in the annotated frame")
    ap.add_argument("--genes", nargs="*", help="only check these genes")
    args = ap.parse_args()

    aln_path = find_alignment(args.folder, args.data_dir)
    if aln_path is None:
        sys.exit("alignment.nex not found")
    aln = Nexus.Nexus(aln_path)
    if aln.datatype == "protein":
        sys.exit("protein alignment: nothing to check")
    table = CodonTable.unambiguous_dna_by_id[args.table]
    seqs = [str(aln.matrix[t]) for t in aln.taxlabels]

    genes = sorted({c[: -len(s)] for c in aln.charsets for s in CODON_SUFFIXES if c.endswith(s)})
    if args.genes:
        genes = [g for g in genes if g in args.genes]
    failures = 0
    print(f"{'gene':40s} {'codons':>8s} {'stop%_frame1':>12s} {'stop%_frame2':>12s} {'stop%_frame3':>12s}  verdict")
    for g in genes:
        pos = {s: aln.charsets.get(g + s) for s in CODON_SUFFIXES}
        if any(v is None for v in pos.values()):
            print(f"{g:40s} skipped: not all three codon positions present")
            continue
        p1, p2, p3 = pos["_1stpos"], pos["_2ndpos"], pos["_3rdpos"]
        n = min(len(p1), len(p2), len(p3))
        # frames: annotated (1,2,3), and shifted alternatives (2,3,1') and (3,1',2')
        all_sites = sorted(p1 + p2 + p3)
        frames = {}
        for shift in range(3):
            frames[shift] = all_sites[shift:]
        results = []
        for shift in range(3):
            stops, total = stop_fraction(seqs, frames[shift], table)
            results.append((stops / total if total else float("nan"), total))
        # which shift corresponds to the annotated frame? the one starting at min(p1)
        annotated_shift = all_sites.index(min(p1)) if min(p1) in all_sites[:3] else 0
        fr = [r[0] for r in results]
        ok = fr[annotated_shift] <= args.max_stop_frac and all(
            fr[annotated_shift] < fr[k] for k in range(3) if k != annotated_shift)
        verdict = "OK" if ok else "CHECK"
        if not ok:
            failures += 1
        print(f"{g:40s} {results[annotated_shift][1]:8d} {fr[0]*100:12.2f} {fr[1]*100:12.2f} {fr[2]*100:12.2f}  {verdict} (annotated frame = frame {annotated_shift+1})")
    print(f"\n{len(genes)} genes checked with genetic code {args.table}; {failures} need attention")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
