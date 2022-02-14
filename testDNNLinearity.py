import uproot
import sys
import TensorflowEvaluatorRun2Legacy as TFEval
import numpy as np
import matplotlib.pyplot as plt

cfg = "../VHbbAnalysis/cfg/dnn_1lep_2017_Run2Legacy.txt"

def getBranchNames(cfg):
    with open(cfg) as f:
        inputvars = []
        for line in f:
            if line.startswith("name="):
                inputvar = line.removeprefix("name=").split(" ")[0]
                inputvars.append(inputvar)
    return inputvars

def getCkptPath(cfg):
    with open(cfg) as f:
        for line in f:
            if line.startswith("xmlFile="):
                return line.removeprefix("xmlFile=").replace("\n","")


branchNames = getBranchNames(cfg)
dnn = TFEval.TensorflowDNNEvaluator("../VHbbAnalysis/"+getCkptPath(cfg))


with uproot.open(sys.argv[1]) as f:

    for syst in ["MergedAbsoluteUp","MergedAbsoluteDown","MergedAbsolute_2017Up","MergedAbsolute_2017Down","MergedBBEC1Up","MergedBBEC1Down","MergedBBEC1_2017Up","MergedBBEC1_2017Down","MergedEC2_2017Up","MergedEC2_2017Down","MergedHFUp","MergedHFDown","MergedEC2Up","MergedEC2Down","MergedFlavorQCDUp","MergedFlavorQCDDown","MergedHF_2017Up","MergedHF_2017Down","MergedRelativeBalUp","MergedRelativeBalDown","MergedRelativeSample_2017Up","MergedRelativeSample_2017Down","JERUp","JERDown","MSD_JMSDown","MSD_JMSUp","MSD_JMRDown","MSD_JMRUp","Reg_ScaleUp","Reg_ScaleDown","Reg_SmearUp","Reg_SmearDown"]:


        x = np.linspace(-1,1,3)
        scoreRanges = np.linspace(0,.9,10)

        for score in [0.8]: 
            #print(score)
            sel = "(controlSample==0) & (isWenu + isWmunu>0) & (Pass_nominal) & (CMS_vhbb_DNN_Wln_13TeV>{}) & (CMS_vhbb_DNN_Wln_13TeV<{})".format(score,score+0.1)
            nompd = f["Events"].arrays(branchNames,sel  ,library="pd")
            nom = nompd.to_numpy()[0]
            #UpBranches = [branch+"_"+syst  if (branch+"_"+syst in  f["Events"].keys() and "MET" not in branch) else branch for branch in branchNames]
            UpBranches = [branch+"_"+syst  if (branch+"_"+syst in  f["Events"].keys()) else branch for branch in branchNames]
            #print(branchNames)
            #print(UpBranches)
            uppd = f["Events"].arrays(UpBranches, sel,library="pd")
            up = uppd.to_numpy()[0]
            
            y = []
            for scale in x:

                inputs = nom+scale*(up-nom)
                y.append(dnn.EvaluateDNN(inputs))
                print(inputs,scale,y[-1])

            nomscore = dnn.EvaluateDNN(nom)

            plt.scatter(x,y-nomscore,label="{:.2f}".format(score))
            plt.ylabel("dnn score - nominal")
            plt.xlabel("scale")

            if "Down" in syst:
                continue
            
            DownBranches = [branch+"_"+syst[:-2]+"Down"  if branch+"_"+syst in  f["Events"].keys() else branch for branch in branchNames]
            downpd = f["Events"].arrays(DownBranches, sel,library="pd")
            down = downpd.to_numpy()[0]
            print("up+down-2*nom", (up-nom)+(down-nom))


            
        plt.legend()
        plt.title(syst)
        #plt.savefig("FIXMET_"+syst+".png")
        plt.clf()


        
        
        
        #if "Down" in syst:
        #    continue
        #print(syst)
        #scoreRanges = np.linspace(0,.9,10)

        #for score in [0.8]: 
        #    sel = "(controlSample==0) & (isWenu + isWmunu>0) & (Pass_nominal) & (CMS_vhbb_DNN_Wln_13TeV>{}) & (CMS_vhbb_DNN_Wln_13TeV<{})".format(score,score+0.1)

        #    nom = f["Events"].arrays(branchNames,sel  ,library="pd")
        #    nom = nom.to_numpy()[0]
        #    UpBranches = [branch+"_"+syst  if branch+"_"+syst in  f["Events"].keys() else branch for branch in branchNames]
        #    up = f["Events"].arrays(UpBranches, sel,library="pd")
        #    DownBranches = [branch+"_"+syst[:-2]+"Down"  if branch+"_"+syst in  f["Events"].keys() else branch for branch in branchNames]
        #    print(DownBranches)
        #    down = f["Events"].arrays(DownBranches, sel,library="pd")
        #    up = up.to_numpy()[0]
        #    down = down.to_numpy()[0]
        #    print(score)
        #    print(up-nom)
        #    print(down-nom)

        #break

