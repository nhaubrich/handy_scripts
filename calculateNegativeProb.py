import ROOT
import sys
import glob
import math

def sumProcs(f,SR,procs):

    totHist = None
    for proc in procs:
         procHist = f.Get("vhbb_{}_13TeV/{}".format(SR,proc))
         if procHist != None:
            if totHist == None:
                totHist = procHist.Clone()
            else:
                totHist = totHist + procHist
    return totHist


def PBinNotNeg(binContent,binError):
    if binError>0:
        return math.log(1.0 - 0.5*math.erfc(binContent/(math.sqrt(2)*binError)))
    else:
        return 0.0 #If no error, assume bin can't go negative: log(10)=0


def PNotNegHist(hist):
    lnPNotNeg = 0
    for i in range(1,hist.GetNbinsX()+1):
        lnPNotNeg+=PBinNotNeg(hist.GetBinContent(i),hist.GetBinError(i))
    return lnPNotNeg

datacardfiles = glob.glob(sys.argv[1]+"/vhbb_input*root")


lnPNotNeg = 0.0
for filename in datacardfiles:
    signalprocs = ["ZH_lep_PTV_150_250_0J_hbb","ZH_lep_PTV_75_150_hbb","WH_lep_PTV_75_150_hbb","WH_lep_PTV_0_75_hbb","WH_lep_PTV_150_250_0J_hbb","ZH_lep_PTV_GT400_hbb","WH_lep_PTV_150_250_GE1J_hbb","WH_lep_PTV_250_400_hbb","WH_lep_PTV_GT400_hbb","ZH_lep_PTV_150_250_GE1J_hbb","ZH_lep_PTV_250_400_hbb"]
    bkgprocs = ["s_Top","Zj1b","TT","VVLF","Zj0b","Wj0b","Wj1b","Wj2b","Zj2b","VVHF","Zj0b_udsg","Zj0b_c","Wj0b_udsg","Wj0b_c"]
    SR = filename.replace("_13TeV2017.root","").split("vhbb_input_vhbb_")[-1]
    #print(filename,SR)
    f = ROOT.TFile(filename)
    bkg = sumProcs(f,SR,bkgprocs)
    
    lnPHistNotNeg = PNotNegHist(bkg)
    print(SR,math.exp(lnPHistNotNeg))
    lnPNotNeg+=lnPHistNotNeg

print("Prob no bins are negative from MCStat:",math.exp(lnPNotNeg))






