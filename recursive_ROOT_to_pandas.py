#recursively combine root files to pandas by sample
import glob
from root_pandas import read_root
import pandas as pd
import sys
import os
from tqdm import tqdm

#NOTE: Accessing an element of a vector seems to return a list with one element (e.g. Jet_pt[0] will be [250.0], not 250), so each column of this sort needs to be converted via .str[0]
cols = ['V_pt']#,'noexpand:Jet_pt[hJetInd1]']#,'Jet_pt']#,'FatJet_pt']
if not os.path.exists("pandas_files"):
    os.mkdir("pandas_files")

stop=False
count = 0
for n,sample in enumerate(glob.glob(sys.argv[1]+"*/")):
    if stop==True:
        break
    head, tail = os.path.split(sample)
    samplename = head.split(os.sep)[-1]
    print(samplename)
    
    dfs = []
    for m,filename in tqdm(enumerate(glob.glob(sample+"*.root"))):
        count+=1
        if count>100:
            print("stopping...")
            stop=True
            break
        head, tail = os.path.split(filename)
        #print(tail)
        dfs.append(read_root(filename,"Events", columns=cols))

    df = pd.concat(dfs)
    df.to_hdf("pandas_files/"+samplename+".h5",key="Events")
