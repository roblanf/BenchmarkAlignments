#!/usr/bin/env python3
"""Fetch a paper's PDF and supplementary files from PubMed Central's open-access bucket.

Usage:
    python fetch_paper.py DOI DATASET_NAME [--out DIR] [--email you@example.org]

    python fetch_paper.py 10.1038/s41586-024-07324-0 Zuntini_2024

Publisher websites (and Europe PMC's PDF renderer) block scripted downloads, but NLM
mirrors the PMC Open Access Subset and author manuscripts to a public AWS bucket with no
login: https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/. This script:

  1. resolves the DOI to a PMCID with NCBI's ID converter,
  2. lists the article's package in the bucket (https://pmc-oa-opendata.s3.amazonaws.com),
  3. downloads the article PDF as <Name>_paper.pdf and every supplementary file, keeping
     the publisher's file names (supplementary PDFs are prefixed <Name>_supplement_).

Files go to --out (default datasets/<Name>/ in this repository, which is gitignored for
PDFs). If the paper is not in PMC the script says so and exits non-zero; those papers
have to be fetched by a person. --email is passed to NCBI as a courtesy identifier.
"""
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET

import requests

BUCKET = "https://pmc-oa-opendata.s3.amazonaws.com"
IDCONV = "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/"
HERE = os.path.dirname(os.path.abspath(__file__))


def doi_to_pmcid(doi, email=None):
    params = {"ids": doi, "idtype": "doi", "format": "json", "tool": "BenchmarkAlignments"}
    if email:
        params["email"] = email
    r = requests.get(IDCONV, params=params, timeout=30)
    r.raise_for_status()
    rec = r.json()["records"][0]
    if "pmcid" not in rec:
        return None, rec.get("errmsg", "not in PMC")
    return rec["pmcid"], None


def list_package(pmcid):
    """Return (version_prefix, [keys]) for the latest version of the article in the bucket."""
    r = requests.get(BUCKET, params={"prefix": pmcid + ".", "max-keys": "1000"}, timeout=60)
    r.raise_for_status()
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    keys = [k.text for k in ET.fromstring(r.text).findall(".//s3:Contents/s3:Key", ns)]
    versions = sorted({k.split("/")[0] for k in keys}, key=lambda v: int(v.rsplit(".", 1)[1]))
    if not versions:
        return None, []
    v = versions[-1]
    return v, [k for k in keys if k.startswith(v + "/")]


def download(key, dest):
    with requests.get(f"{BUCKET}/{key}", stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    return os.path.getsize(dest)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("doi")
    ap.add_argument("name", help="dataset name, e.g. Zuntini_2024")
    ap.add_argument("--out", help="output folder (default datasets/<name>/)")
    ap.add_argument("--email", help="contact email passed to NCBI (optional)")
    ap.add_argument("--no-supplements", action="store_true")
    args = ap.parse_args()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", args.doi.strip())
    out = args.out or os.path.join(HERE, "..", "datasets", args.name)
    os.makedirs(out, exist_ok=True)

    pmcid, err = doi_to_pmcid(doi, args.email)
    if not pmcid:
        sys.exit(f"{doi}: {err}. Not in PubMed Central; fetch this one by hand into pdfs/.")
    version, keys = list_package(pmcid)
    if not keys:
        sys.exit(f"{doi}: {pmcid} is in PMC but not in the open-access bucket (probably not OA); fetch by hand into pdfs/.")
    print(f"{doi} -> {pmcid} ({version}), {len(keys)} files in bucket")

    main_pdf = f"{version}/{version}.pdf"
    if main_pdf in keys:
        dest = os.path.join(out, f"{args.name}_paper.pdf")
        print(f"  paper      -> {dest} ({download(main_pdf, dest)} bytes)")
    else:
        txt = f"{version}/{version}.txt"
        if txt in keys:
            dest = os.path.join(out, f"{args.name}_paper.txt")
            print(f"  no article PDF in the package; saved the full text instead -> {dest} ({download(txt, dest)} bytes)")
        else:
            print("  no article PDF or text in the package")

    if not args.no_supplements:
        for k in keys:
            base = k.split("/", 1)[1]
            if base.startswith(version) or re.search(r"\.(jpg|jpeg|gif|png)$", base, re.I):
                continue  # article xml/txt/json and figure images
            dest = os.path.join(out, f"{args.name}_supplement_{base}")
            print(f"  supplement -> {dest} ({download(k, dest)} bytes)")
    print("done; remember these files are gitignored")


if __name__ == "__main__":
    main()
