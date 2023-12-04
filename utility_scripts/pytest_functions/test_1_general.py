# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
# python -m pytest > ..path\pytest_log.txt, record the output. Mine: C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\pytest_log.txt
import os
 

folder = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets" # prettier    
files = os.listdir(folder)


def test_file_existing():
    assert files.count("README.yaml") == 1, "couldn't find README.yaml file"
    assert files.count("alignment.nex") == 1, "couldn't find alignment.nex"
    assert files.count('charset.csv') == 1, "couldn't find charset.csv"
    print('\n\t3 required files exist')
 
    
def test_extra_file():
    extras = set(files) - set(['alignment.nex',
                               'charset.csv',
                               'README.yaml', 
                               'alignment.nex-seq-summary.txt', 
                               'alignment.nex-summary.txt',
                               'partitions.nex',
                               'loci.nex',
                               'genomes.nex',
                               'pytest_log.txt'])
    assert len(extras) == 0, "There are extra file(s)"
    print('\tno extra file(s)')
