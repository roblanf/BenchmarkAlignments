#!/usr/bin/env python3
"""Create <Name>.tar.gz archives for upload to figShare.

Usage:
    python gzip_datasets.py [--data-dir DIR] [--out DIR] [NAME ...]

Each archive contains the folder <Name>/ with alignment.nex (from the data dir) plus
README.yaml, charset.csv and the two AMAS summary files (from the repository). With no
NAME arguments every dataset is archived.
"""
import argparse
import glob
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..")
TRACKED = ["README.yaml", "charset.csv", "alignment.nex-summary.txt", "alignment.nex-seq-summary.txt"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*")
    ap.add_argument("--data-dir", default=os.environ.get("BENCHALN_DATA"), required=False)
    ap.add_argument("--out", default=os.path.join(REPO, "zips"))
    args = ap.parse_args()
    if not args.data_dir:
        ap.error("--data-dir or $BENCHALN_DATA is required")
    names = args.names or sorted(os.path.basename(d) for d in glob.glob(os.path.join(REPO, "datasets", "*")))
    os.makedirs(args.out, exist_ok=True)
    for n in names:
        with tempfile.TemporaryDirectory() as tmp:
            d = os.path.join(tmp, n)
            os.mkdir(d)
            for f in TRACKED:
                shutil.copy(os.path.join(REPO, "datasets", n, f), d)
            shutil.copy(os.path.join(args.data_dir, n, "alignment.nex"), d)
            out = os.path.join(args.out, n + ".tar.gz")
            subprocess.run(["tar", "-czf", out, "-C", tmp, n], check=True)
            print("wrote", out)


if __name__ == "__main__":
    main()
