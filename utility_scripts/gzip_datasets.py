import os
from util_functions import *

# first we get a list of all the datasets
dataset_folders = [x[0] for x in walklevel(os.path.join(os.getcwd(), "../datasets"))][1:]

#os.mkdir("../zips/")

for f in dataset_folders:
    b = os.path.basename(f)
    command = "tar -zcvf ../zips/%s.tar.gz -C ../datasets/ %s" %(b, b)
    print(command)
    os.system(command)