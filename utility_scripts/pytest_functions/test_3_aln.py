# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
# python -m pytest > ..path\pytest_log.txt, record the output. Mine: C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\pytest_log.txt
import os
from Bio.Nexus import Nexus


folder = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets" # prettier    
alignment_file = os.path.join(folder, "alignment.nex")


def test_read_aln():
    aln = Nexus.Nexus()
    try:
        aln.read(alignment_file)
    except:
        raise AssertionError("Couldn't read nexus file, please check and try again.")
    print('\n\talignment.nex file correct')