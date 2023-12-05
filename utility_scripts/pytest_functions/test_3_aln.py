import os
from Bio.Nexus import Nexus


folder = "processing\\nex\\datasets" # prettier 
alignment_file = os.path.join(folder, "alignment.nex")


def test_read_aln():
    aln = Nexus.Nexus()
    try:
        aln.read(alignment_file)
    except:
        raise AssertionError("Couldn't read nexus file, please check and try again.")
    print('\n\talignment.nex file correct')