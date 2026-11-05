#!/usr/bin/env python3
"""Generate AMAS summary files for a dataset.

Usage:
    python generate_summaries.py DATASET_FOLDER [--data-dir DIR] [--cores N] [--force]

Writes alignment.nex-summary.txt and alignment.nex-seq-summary.txt into DATASET_FOLDER
using the AMAS.py bundled in this directory. Existing files are kept unless --force.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_dataset import find_alignment  # noqa: E402
from Bio.Nexus import Nexus  # noqa: E402

AMAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AMAS.py")


def generate(folder, data_dir=None, cores=4, force=False):
    folder = os.path.abspath(folder.rstrip("/"))
    sumf = os.path.join(folder, "alignment.nex-summary.txt")
    seqf = os.path.join(folder, "alignment.nex-seq-summary.txt")
    if os.path.isfile(sumf) and os.path.isfile(seqf) and not force:
        print(f"{folder}: summaries exist (use --force to regenerate)")
        return
    aln_path = find_alignment(folder, data_dir)
    if aln_path is None:
        raise FileNotFoundError("alignment.nex not found")
    datatype = Nexus.Nexus(aln_path).datatype
    dtype = "aa" if datatype == "protein" else "dna"
    with tempfile.TemporaryDirectory() as tmp:
        # AMAS names outputs after the input file, so run it on a copy named alignment.nex
        link = os.path.join(tmp, "alignment.nex")
        os.symlink(aln_path, link)
        subprocess.run([sys.executable, AMAS, "summary", "-f", "nexus", "-d", dtype,
                        "-i", link, "-c", str(cores), "-s", "-o", os.path.join(tmp, "summary.txt")],
                       check=True, cwd=tmp)
        shutil.move(os.path.join(tmp, "summary.txt"), sumf)
        shutil.move(os.path.join(tmp, "alignment.nex-seq-summary.txt"), seqf)
    print(f"{folder}: wrote summaries")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--data-dir", default=os.environ.get("BENCHALN_DATA"))
    ap.add_argument("--cores", type=int, default=4)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    generate(args.folder, args.data_dir, args.cores, args.force)


if __name__ == "__main__":
    main()
