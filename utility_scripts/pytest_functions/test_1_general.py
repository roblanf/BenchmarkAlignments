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


#def test_charpart_keys():
#    aln = Nexus.Nexus()
#    aln.read(alignment_file)
#    assert list(aln.charpartitions.keys()) == ['loci', 'genomes'], "There should be exactly two CHARPARTITIONS: 'loci' and 'genomes'. Check and try again."
    

#def test_charpart_length():
#    aln = Nexus.Nexus()
#    aln.read(alignment_file)
    
#    all_sites = set(range(aln.nchar))
#    loci_sites = [x[1] for x in aln.charpartitions['loci'].items()]
#    loci_sites = list(itertools.chain.from_iterable(loci_sites))

#    assert len(loci_sites) <= len(all_sites), "The loci charpartition has {} more/less site(s) than the number of sites in the alignment".format(len(loci_sites) - len(all_sites))
#    assert len(set(loci_sites)) >= len(all_sites), "The loci charpartition does not cover the following sites, please fix: {}".format(all_sites.difference(set(loci_sites)))

#    geno_sites = [x[1] for x in aln.charpartitions['genomes'].items()]
#    geno_sites = list(itertools.chain.from_iterable(geno_sites))
    
#    assert len(geno_sites) <= len(all_sites), "The genomes charpartition has {} more/less site(s) than the number of sites in the alignment".format(len(loci_sites) - len(all_sites))
#    assert len(set(geno_sites)) >= len(all_sites), "The genomes charpartition does not cover the following sites, please fix: {}".format(all_sites.difference(set(loci_sites)))
    
    
    
    
    
    
    
    
    
    
    
    
    