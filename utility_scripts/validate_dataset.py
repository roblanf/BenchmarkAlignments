#!/usr/bin/env python3
"""Validate one BenchmarkAlignments dataset folder.

Usage:
    python validate_dataset.py DATASET_FOLDER [--data-dir DIR] [--no-network]

DATASET_FOLDER is e.g. datasets/Anderson_2013. The alignment (alignment.nex) is
looked for in that folder first, then in DIR/<dataset name>/alignment.nex, because
alignments are gitignored and usually live outside the repo.

Every check appends a message to a list of errors. The script exits non-zero and
prints all errors if there are any, so you can fix them in one go. Warnings do not
cause failure.

The checks are also importable: `validate(folder, data_dir, network)` returns
(errors, warnings) so the pytest suite in utility_scripts/tests can run them.
"""
import argparse
import datetime
import os
import re
import sys

import pandas as pd
import yaml
from Bio.Nexus import Nexus

GENOME_NAMES = ["mitochondrial", "nuclear", "chloroplast", "dsDNA", "ssDNA",
                "dsRNA", "ssRNA", "bacterial"]
GENOME_CHARSETS = {g + "_genome" for g in GENOME_NAMES}
CODON_SUFFIXES = ["_1stpos", "_2ndpos", "_3rdpos"]
ALLOWED_FILES = {"README.yaml", "alignment.nex", "charset.csv",
                 "alignment.nex-summary.txt", "alignment.nex-seq-summary.txt"}
CHARSET_CSV_COLUMNS = ["alignment_name", "partition_name", "charset_definition",
                       "partition_start", "partition_end", "partition_skip", "locus_name",
                       "codon_position", "genome", "data_type"]
DIVERGENCE_SOURCES = ["datelife", "timetree.org", "NA"]

YAML_SCHEMA = {
    "study": {"reference", "year", "DOI"},
    "dataset": {"DOI", "license", "figshare", "dataset curation",
                "used for tree inference", "divergence time", "study root age",
                "study clade", "outgroups", "notes"},
    "dataset curation": {"alignment file", "partition information",
                         "justification", "sequence edits"},
    "used for tree inference": {"concatenated", "locus trees"},
    "divergence time": {"source", "query taxa", "date accessed", "median age",
                        "min age", "max age", "N chronograms", "source studies"},
    "study clade": {"latin", "english", "taxon ID"},
}


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _is_na(x):
    return isinstance(x, str) and x.strip() == "NA"


def _check_age(value, label, errors):
    """Ages are 'NA' or '<number> mya'."""
    if _is_na(value):
        return None
    if not isinstance(value, str):
        errors.append(f"{label}: must be 'NA' or '<number> mya', got {value!r}")
        return None
    parts = value.split()
    if len(parts) != 2 or parts[1] != "mya":
        errors.append(f"{label}: must be 'NA' or '<number> mya', got {value!r}")
        return None
    try:
        t = float(parts[0])
    except ValueError:
        errors.append(f"{label}: {parts[0]!r} is not a number")
        return None
    if not 0 < t < 4600:
        errors.append(f"{label}: {t} mya is outside 0-4600 mya")
    return t


def _check_url(url, label, errors, warnings):
    """A DOI-style URL without scheme. Resolution is a warning, not an error,
    because DOI resolvers and journals rate-limit and block bots."""
    import requests
    if not isinstance(url, str) or not url.startswith("doi.org/"):
        errors.append(f"{label}: must be a string starting with 'doi.org/', got {url!r}")
        return
    try:
        r = requests.head("https://" + url, allow_redirects=True, timeout=15,
                          headers={"User-Agent": "BenchmarkAlignments-validator"})
        if r.status_code >= 400 and r.status_code != 403:
            warnings.append(f"{label}: https://{url} returned HTTP {r.status_code}")
    except Exception as e:  # noqa: BLE001
        warnings.append(f"{label}: could not resolve https://{url} ({e})")


def _check_taxon_id(taxid, errors, warnings):
    import requests
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
           f"?db=taxonomy&id={taxid}&retmode=json")
    try:
        r = requests.get(url, timeout=15)
        js = r.json()
        rec = js.get("result", {}).get(str(taxid), {})
        if "error" in rec or not rec.get("scientificname"):
            errors.append(f"study clade / taxon ID: {taxid} does not resolve at NCBI Taxonomy")
        else:
            return rec.get("scientificname")
    except Exception as e:  # noqa: BLE001
        warnings.append(f"study clade / taxon ID: could not query NCBI ({e})")
    return None


# ----------------------------------------------------------------------------
# YAML
# ----------------------------------------------------------------------------
def check_yaml(path, errors, warnings, network=True):
    """Returns the parsed YAML dict (or None)."""
    try:
        y = yaml.safe_load(open(path))
    except Exception as e:  # noqa: BLE001
        errors.append(f"README.yaml: could not parse ({e})")
        return None
    if not isinstance(y, dict):
        errors.append("README.yaml: top level is not a mapping")
        return None

    def keys_ok(d, name, expected):
        if not isinstance(d, dict):
            errors.append(f"README.yaml: '{name}' is not a mapping")
            return False
        if set(d.keys()) != expected:
            missing = expected - set(d.keys())
            extra = set(d.keys()) - expected
            errors.append(f"README.yaml: '{name}' keys wrong. missing={sorted(missing)} extra={sorted(extra)}")
            return False
        return True

    if not keys_ok(y, "top level", {"study", "dataset"}):
        return y
    st, ds = y["study"], y["dataset"]
    ok = keys_ok(st, "study", YAML_SCHEMA["study"])
    ok &= keys_ok(ds, "dataset", YAML_SCHEMA["dataset"])
    if not ok:
        return y
    for sub in ["dataset curation", "used for tree inference", "divergence time", "study clade"]:
        keys_ok(ds[sub], sub, YAML_SCHEMA[sub])

    # any leftover template placeholders?
    raw = open(path).read()
    for line in raw.splitlines():
        if re.search(r":\s*\[.*\]\s*$", line) and not line.strip().startswith("#"):
            errors.append(f"README.yaml: unfilled template placeholder on line: {line.strip()[:80]}")

    # study
    if not isinstance(st.get("reference"), str) or len(st["reference"]) < 20:
        errors.append("study / reference: missing or too short")
    yr = st.get("year")
    if not isinstance(yr, int) or not 1950 <= yr <= datetime.date.today().year + 1:
        errors.append(f"study / year: {yr!r} is not a plausible integer year")
    if network:
        _check_url(st.get("DOI"), "study / DOI", errors, warnings)
    elif not (isinstance(st.get("DOI"), str) and st["DOI"].startswith("doi.org/")):
        errors.append("study / DOI: must start with 'doi.org/'")

    # dataset
    if network:
        _check_url(ds.get("DOI"), "dataset / DOI", errors, warnings)
    elif not (isinstance(ds.get("DOI"), str) and ds["DOI"].startswith("doi.org/")):
        errors.append("dataset / DOI: must start with 'doi.org/'")
    if ds.get("DOI") == st.get("DOI"):
        errors.append("dataset / DOI is identical to study / DOI; the dataset needs its own DOI")
    if ds.get("license") not in ["CC0", "CCBY"]:
        errors.append(f"dataset / license: must be 'CC0' or 'CCBY', got {ds.get('license')!r}")
    fs = ds.get("figshare")
    if not (_is_na(fs) or (isinstance(fs, str) and "figshare.com" in fs)):
        errors.append(f"dataset / figshare: must be 'NA' or a figshare.com URL, got {fs!r}")
    if _is_na(fs):
        errors.append("dataset / figshare is NA: the archive must be on figShare and linked before the dataset is finished")

    cur = ds.get("dataset curation", {})
    if isinstance(cur, dict):
        for k in ["alignment file", "partition information", "justification", "sequence edits"]:
            if not isinstance(cur.get(k), str) or not cur[k].strip():
                errors.append(f"dataset curation / {k}: must be a non-empty string (use 'NA' if unknown)")

    uti = ds.get("used for tree inference", {})
    if isinstance(uti, dict):
        for k in ["concatenated", "locus trees"]:
            if uti.get(k) not in [True, False]:
                errors.append(f"used for tree inference / {k}: must be yes or no")

    dt = ds.get("divergence time", {})
    if isinstance(dt, dict):
        src = dt.get("source")
        if src not in DIVERGENCE_SOURCES:
            errors.append(f"divergence time / source: must be one of {DIVERGENCE_SOURCES}, got {src!r}")
        med = _check_age(dt.get("median age"), "divergence time / median age", errors)
        lo = _check_age(dt.get("min age"), "divergence time / min age", errors)
        hi = _check_age(dt.get("max age"), "divergence time / max age", errors)
        if lo is not None and hi is not None and lo > hi:
            errors.append("divergence time: min age > max age")
        if med is not None and lo is not None and hi is not None and not lo <= med <= hi:
            errors.append("divergence time: median age is outside [min age, max age]")
        n = dt.get("N chronograms")
        if not (_is_na(n) or (isinstance(n, int) and n >= 1)):
            errors.append(f"divergence time / N chronograms: must be 'NA' or a positive integer, got {n!r}")
        da = dt.get("date accessed")
        if not _is_na(da):
            if isinstance(da, datetime.date):
                pass
            elif isinstance(da, str):
                try:
                    datetime.date.fromisoformat(da)
                except ValueError:
                    errors.append(f"divergence time / date accessed: must be YYYY-MM-DD or 'NA', got {da!r}")
            else:
                errors.append(f"divergence time / date accessed: must be YYYY-MM-DD or 'NA', got {da!r}")
        if src == "datelife":
            if med is None:
                errors.append("divergence time: source is 'datelife' but median age is NA")
            for k in ["query taxa", "source studies"]:
                if _is_na(dt.get(k)) or not isinstance(dt.get(k), str):
                    errors.append(f"divergence time / {k}: required when source is 'datelife'")
        if src == "NA" and med is not None:
            errors.append("divergence time: source is NA but an age is given")

    _check_age(ds.get("study root age"), "study root age", errors)

    cl = ds.get("study clade", {})
    if isinstance(cl, dict):
        if not isinstance(cl.get("latin"), str) or not cl["latin"].strip() or _is_na(cl["latin"]):
            errors.append("study clade / latin: must be a non-empty clade name")
        if not isinstance(cl.get("english"), str) or not cl["english"].strip():
            errors.append("study clade / english: must be a non-empty string")
        if not isinstance(cl.get("taxon ID"), int):
            errors.append("study clade / taxon ID: must be an integer")
        elif network:
            _check_taxon_id(cl["taxon ID"], errors, warnings)

    og = ds.get("outgroups")
    if not isinstance(og, str) or not og.strip():
        errors.append("outgroups: must be a comma-separated list of taxon names, or 'NA' only for tip-dated data")

    if not isinstance(ds.get("notes"), str) or not ds["notes"].strip():
        errors.append("notes: must be 'NA' or a non-empty string")
    if _is_na(og) and not re.search(r"tip.dat|sampling date|heterochronous", str(ds.get("notes")), re.I):
        warnings.append("outgroups is NA: notes should say the data are tip-dated")
    return y


# ----------------------------------------------------------------------------
# NEXUS
# ----------------------------------------------------------------------------
def _parse_sets_block(text):
    """Return (charsets, charpartitions, taxsets) parsed from the raw SETS block.
    charsets: {name: definition string}; charpartitions: {name: [charset names]};
    taxsets: {name: [taxa]}."""
    m = re.search(r"begin\s+sets\s*;(.*?)\bend\s*;", text, re.S | re.I)
    if not m:
        return None, None, None
    block = m.group(1)
    block = re.sub(r"\[[^\]]*\]", " ", block)  # strip comments
    stmts = [s.strip() for s in block.split(";") if s.strip()]
    charsets, charpartitions, taxsets = {}, {}, {}
    for s in stmts:
        mm = re.match(r"charset\s+(\S+)\s*=\s*(.*)$", s, re.S | re.I)
        if mm:
            charsets[mm.group(1)] = " ".join(mm.group(2).split())
            continue
        mm = re.match(r"charpartition\s+(\S+)\s*=\s*(.*)$", s, re.S | re.I)
        if mm:
            members = []
            for item in mm.group(2).split(","):
                item = item.strip()
                if not item:
                    continue
                members.append(item.split(":", 1)[1].strip() if ":" in item else item)
            charpartitions[mm.group(1)] = members
            continue
        mm = re.match(r"taxset\s+(\S+)\s*=\s*(.*)$", s, re.S | re.I)
        if mm:
            toks = re.findall(r"'[^']*'|\"[^\"]*\"|\S+", mm.group(2))
            taxsets[mm.group(1)] = [t.strip("'\"") for t in toks]
            continue
    return charsets, charpartitions, taxsets


def _parse_samplingdates(text):
    m = re.search(r"begin\s+samplingdates\s*;(.*?)\bend\s*;", text, re.S | re.I)
    if not m:
        return None
    dates = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.lower().startswith(("dimensions", "units")):
            continue
        m2 = re.match(r"^('[^']*'|\"[^\"]*\"|[^,\s]+)\s*,\s*(\S+)", line)
        if m2:
            dates[m2.group(1).strip("'\"")] = m2.group(2)
    return dates


def check_nexus(path, errors, warnings):
    """Returns dict with parsed alignment info or None."""
    raw = open(path, "rb").read()
    if b"\r" in raw:
        errors.append("alignment.nex: contains carriage returns (\\r); convert to unix line endings")
    text = raw.decode("utf-8", errors="replace")
    if not text.startswith("#NEXUS"):
        errors.append("alignment.nex: must start with '#NEXUS'")
    head = text[:2000]
    if not re.search(r"begin\s+data\s*;", head, re.I):
        errors.append("alignment.nex: first block must be DATA")
    fmt = re.search(r"format\s+([^;]*);", head, re.I)
    if fmt:
        f = fmt.group(1).lower()
        if "datatype=nucleotide" not in f and "datatype=protein" not in f:
            errors.append("alignment.nex: format datatype must be 'nucleotide' or 'protein'")
        if "missing=?" not in f:
            errors.append("alignment.nex: format must have missing=?")
        if "gap=-" not in f:
            errors.append("alignment.nex: format must have gap=-")
        if "interleave" in f:
            errors.append("alignment.nex: must be non-interleaved")
    else:
        errors.append("alignment.nex: no FORMAT line found in DATA block")

    try:
        aln = Nexus.Nexus(path)
    except Exception as e:  # noqa: BLE001
        errors.append(f"alignment.nex: Bio.Nexus could not parse it ({e})")
        return None

    info = {"ntax": aln.ntax, "nchar": aln.nchar, "datatype": aln.datatype,
            "taxa": list(aln.taxlabels), "aln": aln}
    dups = [t[:-5] for t in aln.taxlabels if t.endswith(".copy")]  # Bio.Nexus renames duplicates
    if dups or len(set(aln.taxlabels)) != len(aln.taxlabels):
        errors.append(f"alignment.nex: duplicate taxon names: {sorted(set(dups))[:5]}")
    bad = [t for t in aln.taxlabels if re.search(r"[^A-Za-z0-9_.]", t)]
    if bad:
        warnings.append(f"alignment.nex: {len(bad)} taxon names need quoting in NEXUS (characters outside A-Z a-z 0-9 _ .), e.g. {bad[:3]}; prefer sanitising to underscores and recording it in 'sequence edits'")

    charsets, charpartitions, taxsets = _parse_sets_block(text)
    if charsets is None:
        errors.append("alignment.nex: no SETS block found")
        return info
    info.update({"charsets": charsets, "charpartitions": charpartitions, "taxsets": taxsets})

    # charpartitions
    if set(charpartitions.keys()) != {"loci", "genomes"}:
        errors.append(f"alignment.nex: CHARPARTITIONs must be exactly 'loci' and 'genomes', found {sorted(charpartitions)}")
        return info
    loci_names = charpartitions["loci"]
    genome_names = charpartitions["genomes"]
    all_sites = set(range(aln.nchar))

    for pname, members in [("loci", loci_names), ("genomes", genome_names)]:
        if len(set(members)) != len(members):
            errors.append(f"alignment.nex: CHARPARTITION {pname} lists a charset twice")
        missing = [c for c in members if c not in aln.charsets]
        if missing:
            errors.append(f"alignment.nex: CHARPARTITION {pname} refers to undefined charsets {missing[:5]}")
            continue
        seen = {}
        for c in members:
            for s in aln.charsets[c]:
                if s in seen:
                    errors.append(f"alignment.nex: site {s+1} is in both {seen[s]} and {c} (CHARPARTITION {pname})")
                    break
                seen[s] = c
        covered = set(seen)
        if covered != all_sites:
            miss = sorted(all_sites - covered)
            extra = sorted(covered - all_sites)
            if miss:
                errors.append(f"alignment.nex: CHARPARTITION {pname} does not cover {len(miss)} sites, first: {[m+1 for m in miss[:5]]}")
            if extra:
                errors.append(f"alignment.nex: CHARPARTITION {pname} includes sites beyond nchar, first: {[e+1 for e in extra[:5]]}")

    # every charset belongs to exactly one partition
    stray = set(charsets) - set(loci_names) - set(genome_names)
    if stray:
        errors.append(f"alignment.nex: charsets defined but in no CHARPARTITION: {sorted(stray)[:5]}")
    both = set(loci_names) & set(genome_names)
    if both:
        errors.append(f"alignment.nex: charsets in both loci and genomes partitions: {sorted(both)[:5]}")

    # genome charsets
    bad_g = [g for g in genome_names if g not in GENOME_CHARSETS]
    if bad_g:
        errors.append(f"alignment.nex: genome charsets must be named one of {sorted(GENOME_CHARSETS)}, found {bad_g}")

    # codon positions: every gene with a _1stpos must have all three, step 3, consecutive offsets
    for c in loci_names:
        if c in GENOME_CHARSETS:
            errors.append(f"alignment.nex: '{c}' looks like a genome charset but is in the loci partition")
        for suf in CODON_SUFFIXES:
            if c.endswith(suf):
                base = c[: -len(suf)]
                sibs = [base + s for s in CODON_SUFFIXES]
                present = [s for s in sibs if s in aln.charsets]
                if len(present) < 3:
                    if c == present[0]:
                        warnings.append(f"alignment.nex: {base} has only codon positions {[s[-6:-3] for s in present]}; fine only if the source alignment excludes the others (say so in notes)")
                    for s in present:
                        sites = aln.charsets[s]
                        strides = {b - a for a, b in zip(sites, sites[1:])}
                        if len(sites) > 1 and strides != {len(present)}:
                            errors.append(f"alignment.nex: {s} should be a stride-{len(present)} charset (only {len(present)} codon positions present)")
                    break
                starts = sorted(min(aln.charsets[s]) for s in sibs)
                if starts[1] - starts[0] != 1 or starts[2] - starts[1] != 1:
                    errors.append(f"alignment.nex: codon charsets for {base} do not start on three consecutive sites (starts {[x+1 for x in starts]})")
                for s in sibs:
                    sites = aln.charsets[s]
                    if len(sites) > 1 and any(b - a != 3 for a, b in zip(sites, sites[1:])):
                        errors.append(f"alignment.nex: {s} is not a stride-3 charset")
                        break
                break
    if aln.datatype == "protein" and any(c.endswith(tuple(CODON_SUFFIXES)) for c in loci_names):
        errors.append("alignment.nex: protein alignment has codon-position charsets")

    # outgroups
    if set(taxsets.keys()) != {"outgroups"}:
        errors.append(f"alignment.nex: TAXSETs must be exactly 'outgroups', found {sorted(taxsets)}")
    else:
        og = taxsets["outgroups"]
        if not og:
            if re.search(r"begin\s+samplingdates", text, re.I):
                warnings.append("alignment.nex: TAXSET outgroups is empty; acceptable only because the data are tip-dated (SAMPLINGDATES block present)")
            else:
                errors.append("alignment.nex: TAXSET outgroups is empty (required unless a SAMPLINGDATES block makes the data tip-dated)")
        unknown = [t for t in og if t not in aln.taxlabels]
        if unknown:
            errors.append(f"alignment.nex: outgroup taxa not in alignment: {unknown[:5]}")
        if len(og) >= aln.ntax:
            errors.append("alignment.nex: every taxon is an outgroup")
        info["outgroups"] = og

    sd = _parse_samplingdates(text)
    if sd is not None:
        info["samplingdates"] = sd
        unknown = [t for t in sd if t not in aln.taxlabels]
        if unknown:
            errors.append(f"alignment.nex: SAMPLINGDATES names not in alignment: {unknown[:5]}")
        missing = [t for t in aln.taxlabels if t not in sd]
        if missing:
            errors.append(f"alignment.nex: SAMPLINGDATES lacks {len(missing)} taxa, e.g. {missing[:3]}")
    return info


# ----------------------------------------------------------------------------
# charset.csv
# ----------------------------------------------------------------------------
def check_charset_csv(path, info, dataset_name, errors, warnings):
    try:
        df = pd.read_csv(path)
    except Exception as e:  # noqa: BLE001
        errors.append(f"charset.csv: could not read ({e})")
        return
    if list(df.columns) != CHARSET_CSV_COLUMNS:
        errors.append(f"charset.csv: columns must be exactly {CHARSET_CSV_COLUMNS}")
        return
    if info is None or "charpartitions" not in info or set(info["charpartitions"]) != {"loci", "genomes"}:
        return  # nexus problems already reported
    aln = info["aln"]
    loci_names = info["charpartitions"]["loci"]

    if (df.alignment_name != dataset_name).any():
        errors.append("charset.csv: alignment_name must equal the dataset folder name on every row")
    if list(df.partition_name) != loci_names:
        errors.append("charset.csv: partition_name rows must match CHARPARTITION loci in alignment.nex, in order")
        return

    # site -> genome from nexus
    site_genome = {}
    for g in info["charpartitions"]["genomes"]:
        if g in aln.charsets:
            for s in aln.charsets[g]:
                site_genome[s] = g[: -len("_genome")]

    for i, row in df.iterrows():
        name = row.partition_name
        expected = aln.charsets.get(name, [])
        if " ".join(str(row.charset_definition).split()) != info["charsets"].get(name, "").rstrip(";").strip():
            errors.append(f"charset.csv row {i} ({name}): charset_definition differs from alignment.nex")
        simple = not (pd.isna(row.partition_start) or str(row.partition_start) == "NA")
        skip = 1
        if simple:
            try:
                start, end, skip = int(row.partition_start), int(row.partition_end), int(row.partition_skip)
            except (TypeError, ValueError):
                errors.append(f"charset.csv row {i}: start/end/skip must be integers or all NA")
                continue
            if list(range(start - 1, end, skip)) != expected:
                errors.append(f"charset.csv row {i} ({name}): sites {start}-{end}\\{skip} differ from alignment.nex charset")
        elif expected and expected == list(range(expected[0], expected[-1] + 1, (expected[1] - expected[0]) if len(expected) > 1 else 1)):
            errors.append(f"charset.csv row {i} ({name}): is a simple range, so start/end/skip must be filled in")
        # locus name and codon position
        cp = row.codon_position
        suffix = next((s for s in CODON_SUFFIXES if name.endswith(s)), None)
        if suffix:
            if row.locus_name != name[: -len(suffix)]:
                errors.append(f"charset.csv row {i}: locus_name should be {name[:-len(suffix)]}")
            if not (isinstance(cp, (int, float)) and not pd.isna(cp) and int(cp) == CODON_SUFFIXES.index(suffix) + 1):
                errors.append(f"charset.csv row {i}: codon_position should be {CODON_SUFFIXES.index(suffix)+1}")
        else:
            if row.locus_name != name:
                errors.append(f"charset.csv row {i}: locus_name should equal partition_name for non-codon charsets")
            if not (pd.isna(cp) or str(cp) == "NA"):
                errors.append(f"charset.csv row {i}: codon_position should be NA for non-codon charsets")
        # genome
        if row.genome not in GENOME_NAMES:
            errors.append(f"charset.csv row {i}: genome {row.genome!r} not in {GENOME_NAMES}")
        else:
            gens = {site_genome.get(s) for s in expected}
            if gens != {row.genome}:
                errors.append(f"charset.csv row {i} ({name}): genome {row.genome!r} disagrees with alignment.nex genomes partition {sorted(x for x in gens if x)}")
        # data type
        want = "AA" if aln.datatype == "protein" else "DNA"
        if row.data_type != want:
            errors.append(f"charset.csv row {i}: data_type should be {want}")


# ----------------------------------------------------------------------------
# AMAS summaries
# ----------------------------------------------------------------------------
def check_summaries(folder, info, errors, warnings):
    sumf = os.path.join(folder, "alignment.nex-summary.txt")
    seqf = os.path.join(folder, "alignment.nex-seq-summary.txt")
    try:
        s = pd.read_csv(sumf, sep="\t")
        if info is not None:
            if int(s.No_of_taxa[0]) != info["ntax"] or int(s.Alignment_length[0]) != info["nchar"]:
                errors.append("alignment.nex-summary.txt: ntax/nchar do not match alignment.nex; regenerate summaries")
    except Exception as e:  # noqa: BLE001
        errors.append(f"alignment.nex-summary.txt: unreadable ({e})")
    try:
        q = pd.read_csv(seqf, sep="\t")
        norm = lambda t: re.sub(r"[ .]", "_", str(t))  # AMAS rewrites spaces and dots as underscores
        if info is not None and (len(q) != info["ntax"] or {norm(t) for t in q.Taxon_name} != {norm(t) for t in info["taxa"]}):
            errors.append("alignment.nex-seq-summary.txt: taxon names do not match alignment.nex; regenerate summaries")
    except Exception as e:  # noqa: BLE001
        errors.append(f"alignment.nex-seq-summary.txt: unreadable ({e})")


# ----------------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------------
def find_alignment(folder, data_dir):
    p = os.path.join(folder, "alignment.nex")
    if os.path.isfile(p):
        return p
    if data_dir:
        p = os.path.join(data_dir, os.path.basename(os.path.abspath(folder)), "alignment.nex")
        if os.path.isfile(p):
            return p
    return None


def validate(folder, data_dir=None, network=True):
    errors, warnings = [], []
    folder = os.path.abspath(folder.rstrip("/"))
    name = os.path.basename(folder)
    if not re.match(r"^[A-Z][A-Za-z]+_\d{4}[a-z]?(_(aa|dna))?$", name):
        errors.append(f"folder name '{name}' should look like Author_2013, Author_2013a, or Author_2013_aa")

    files = set(os.listdir(folder))
    unexpected = {f for f in files if f not in ALLOWED_FILES and not f.lower().endswith(".pdf")
                  and not f.startswith(".") and not re.match(rf"{re.escape(name)}_(paper\.|supplement_)", f)}
    if unexpected:
        errors.append(f"unexpected files in dataset folder: {sorted(unexpected)}")
    for f in ["README.yaml", "charset.csv", "alignment.nex-summary.txt", "alignment.nex-seq-summary.txt"]:
        if f not in files:
            errors.append(f"missing {f}")

    aln_path = find_alignment(folder, data_dir)
    info = None
    if aln_path is None:
        errors.append("alignment.nex not found in the dataset folder or the data directory")
    else:
        info = check_nexus(aln_path, errors, warnings)

    y = None
    if "README.yaml" in files:
        y = check_yaml(os.path.join(folder, "README.yaml"), errors, warnings, network=network)
    if "charset.csv" in files:
        check_charset_csv(os.path.join(folder, "charset.csv"), info, name, errors, warnings)
    if info is not None:
        check_summaries(folder, info, errors, warnings)

    # cross-checks between YAML and nexus
    if y and info and "outgroups" in info:
        try:
            yog = [] if _is_na(y["dataset"]["outgroups"]) else [t.strip() for t in y["dataset"]["outgroups"].split(",") if t.strip()]
            if set(yog) != set(info["outgroups"]):
                errors.append("outgroups in README.yaml do not match TAXSET outgroups in alignment.nex")
        except Exception:  # noqa: BLE001
            pass
    if y and info:
        try:
            if y["study"]["year"] and not re.search(str(y["study"]["year"] - 1) + "|" + str(y["study"]["year"]) + "|" + str(y["study"]["year"] + 1), name):
                warnings.append(f"folder name year and study year {y['study']['year']} differ by more than one year")
        except Exception:  # noqa: BLE001
            pass
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="dataset folder, e.g. datasets/Anderson_2013")
    ap.add_argument("--data-dir", default=os.environ.get("BENCHALN_DATA"),
                    help="directory holding <dataset>/alignment.nex files (default: $BENCHALN_DATA)")
    ap.add_argument("--no-network", action="store_true", help="skip DOI and NCBI lookups")
    args = ap.parse_args()
    errors, warnings = validate(args.folder, args.data_dir, network=not args.no_network)
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        print(f"\n{os.path.basename(os.path.abspath(args.folder))}: FAILED with {len(errors)} error(s)")
        sys.exit(1)
    print(f"{os.path.basename(os.path.abspath(args.folder))}: OK ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
