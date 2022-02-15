import ROOT
import os
import sys

fname = sys.argv[1]
f = ROOT.TFile(fname,"UPDATE")

def convertToTH1F(f,key):
    print(key)
    #obj = getattr(f,key)
    obj=f.Get(key)
    if isinstance(obj,ROOT.TDirectoryFile):
        #print("TD")
        #directory, so call recursively on each subsequent object
        for subkey in obj.GetListOfKeys():
            convertToTH1F(obj,subkey.GetName())
    
    if isinstance(obj,ROOT.TH1D):
        #print("TH1D")
        h1F = ROOT.TH1F()
        obj.Copy(h1F)
        f.cd()
        h1F.Write("",ROOT.TObject.kOverwrite)
        #f.Delete(obj.GetName()+";1")

    

for key in f.GetListOfKeys():
    print(key)
    convertToTH1F(f,key.GetName())

f.Close()
