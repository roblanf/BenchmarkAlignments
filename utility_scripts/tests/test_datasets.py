"""pytest suite: validate every dataset folder in datasets/.

Run from utility_scripts/:
    BENCHALN_DATA=/path/to/alignments pytest -q tests/
    pytest -q tests/ --no-network          # skip DOI and NCBI lookups
    pytest -q tests/ -k Zuntini            # one dataset

If BENCHALN_DATA is unset and a folder has no alignment.nex, the alignment checks are
skipped for that folder (only the metadata is checked).
"""
import glob
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from validate_dataset import find_alignment, validate  # noqa: E402

DATASETS = sorted(glob.glob(os.path.join(HERE, "..", "..", "datasets", "*", "")))


@pytest.mark.parametrize("folder", DATASETS, ids=[os.path.basename(d.rstrip("/")) for d in DATASETS])
def test_dataset(folder, request):
    data_dir = os.environ.get("BENCHALN_DATA")
    network = not request.config.getoption("--no-network")
    errors, warnings = validate(folder, data_dir, network=network)
    if find_alignment(folder, data_dir) is None:
        errors = [e for e in errors if "alignment.nex" not in e]
        warnings.append("alignment.nex not available: alignment checks skipped")
    for w in warnings:
        print("WARNING:", w)
    assert not errors, "\n" + "\n".join(errors)
