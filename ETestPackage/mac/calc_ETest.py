import ROOT , sys
from ROOT import ETest , TRandom3
from ROOT import TFile , TTree
from array import array
import numpy as n

# run with:
# > python mac/calc_ETest <Nbins> <Nsamples> <number> <cutoff parameter = 0.66170> <contamination = 0.1%>

if int(len(sys.argv)) < 2 :
    print "run with: \n > python mac/calc_ETest <Nbins> <Nsamples> <number> <cutoff parameter = 0.6617> <contamination = 0.1%>"
    sys.exit(0)

Nbins       = int(sys.argv[1])
Nsamples    = int(sys.argv[2])
FileNumber  = int(sys.argv[3])
rand        = TRandom3(int(sys.argv[3]))

CalculationType = "Uni/Uni + n% Contamination"


Path    = "/home/erez/EnergyTest/ETestResults"
#Path    = "/Users/erezcohen/Desktop/EnergyTest/EnergyTestResults"


if (CalculationType == "Uni vs. Const"):
    FileName    = "ETestResults_Nbins_%d"%Nbins

elif (CalculationType == "Uni vs. Uni"):
    FileName    = "UniUni_Nbins_%d"%(Nbins)

elif (CalculationType == "Uni vs. Uni with different cutoffs"):
    CutOffParameter = float(sys.argv[4])
    FileName    = "UniUni%d_Cutoff%.2f"%(Nbins,CutOffParameter)

elif (CalculationType == "Uni vs. Uni + 0.1% Gauss contamination"):
    nContamination = 0.1    # [%] of contammination
    FileName    = "UniGaus%.2fpercentCont_Nbins_%d"%(nContamination,Nbins)

elif (CalculationType == "Uni vs. Uni + 0.1% Gauss contamination with different cutoffs"):
    CutOffParameter = float(sys.argv[4])
    nContamination = 0.1    # [%] of contammination
    FileName    = "Uni_Cutoff%.2f_Gaus%.2fCont_Nbins_%d"%(CutOffParameter,nContamination,Nbins)

elif (CalculationType == "Uni/Uni + n% Contamination"):
    nContamination = float(sys.argv[5])    # [%] of contammination
    FileName    = "UniGaus%.2fpercentCont_Nbins_%d"%(nContamination,Nbins)



FEtest  = ROOT.TFile(Path+"/"+FileName+"_%d.root"%FileNumber,"recreate");
TEtest  = ROOT.TTree("ETestTree","ETest statistic "+FileName);
fNbins  = n.zeros(1, dtype=int)
Phi     = n.zeros(1, dtype=float)
TEtest.Branch( "Nbins"      , fNbins, "Nbins/I" )
TEtest.Branch( "phi"        , Phi   , "phi/D" )
fNbins[0] = Nbins
etest   = ETest(Nbins)




if (CalculationType == "Uni vs. Const"):
    Npoints = 135000
    hFlat = ROOT.TH3F("hFlat_%d"%(Nbins),"Flat Distribution Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
    bin_content = Npoints/(Nbins*Nbins*Nbins)
    for i1 in range(1,Nbins) :
        for i2 in range(1,Nbins) :
            for i3 in range(1,Nbins) :
                hFlat.SetBinContent(i1,i2,i3,bin_content)    #    etest.SetD(hFlat)
    for sample in range(0,Nsamples) :
        hSmpl = ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins),"Uniform sample Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
        for j in range(0,Npoints) :
            hSmpl.Fill(rand.Uniform(),rand.Uniform(),rand.Uniform())
        Phi[0] = etest.Histo3DETest( hFlat , hSmpl ) #        Phi[0] = etest.ETestKnowingD ( hSmpl )
        if(sample%10==0):
            print "Sample %d" %(sample) +"ETest statistic for N=%d bins, sample %d is %g"%(Nbins,sample,Phi)
        TEtest.Fill()
        del hSmpl


elif (CalculationType == "Uni vs. Uni"):
    Npoints = 1000000
    hUni = ROOT.TH3F("hUni_%d"%(Nbins),"uniform distribution Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
    for i in range(0,Npoints) :
        hUni.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
    for sample in range(0,Nsamples) :
        hSmpl = ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins),"Uniform sample Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
        for j in range(0,Npoints) :
            hSmpl.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
        Phi[0] = etest.Histo3DETest( hUni , hSmpl )
        if(sample%10==0):
            print "Sample %d" %(sample) +" ETest statistic for N=%d bins, sample %d is %g"%(Nbins,sample,Phi)
        TEtest.Fill()
        del hSmpl


elif (CalculationType == "Uni vs. Uni with different cutoffs"):
    etest.SetCutOffPar(CutOffParameter)
    Npoints = 1000000
    hUni = ROOT.TH3F("hUni_%d"%(Nbins),"uniform distribution Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
    for i in range(0,Npoints) :
        hUni.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
    for sample in range(0,Nsamples) :
        hSmpl = ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins),"Uniform sample Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
        for j in range(0,Npoints) :
            hSmpl.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
        Phi[0] = etest.Histo3DETest( hUni , hSmpl )
        if(sample%10==0):
            print "Sample %d" %(sample) +" ETest statistic for N=%d bins, sample %d is %g"%(Nbins,sample,Phi)
        TEtest.Fill()
        del hSmpl


elif (CalculationType == "Uni vs. Uni + 0.1% Gauss contamination" or CalculationType == "Uni/Uni + n% Contamination"):
    
    Npoints = 1000000
    hUni = ROOT.TH3F("hUni_%d"%(Nbins),"Uniform Distribution Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
    for j in range(0,Npoints) :
        hUni.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
    for sample in range(0,Nsamples) :
        hSmpl = ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins),"Uniform sample Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
        for j in range(0,int(Npoints*(1.-nContamination/100.))) : # uniform
            hSmpl.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
        for j in range(0,int(Npoints*(nContamination/100.))) :    # contamination
            hSmpl.Fill(rand.Gaus(0.5,0.1),rand.Gaus(0.5,0.1),rand.Gaus(0.5,0.1))
        Phi[0] = etest.Histo3DETest( hUni , hSmpl )
        if(sample%10==0):
            print "Sample %d" %(sample) +" ETest statistic for N=%d bins, sample %d, is %g"%(Nbins,sample,Phi)
        TEtest.Fill()
        del hSmpl


elif (CalculationType == "Uni vs. Uni + 0.1% Gauss contamination with different cutoffs"):
    etest.SetCutOffPar(CutOffParameter)
    Npoints = 1000000
    hUni = ROOT.TH3F("hUni_%d"%(Nbins),"Uniform Distribution Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
    for j in range(0,Npoints) :
        hUni.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
    for sample in range(0,Nsamples) :
        hSmpl = ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins),"Uniform sample Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
        for j in range(0,int(Npoints*(1.-nContamination/100.))) : # uniform
            hSmpl.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
        for j in range(0,int(Npoints*(nContamination/100.))) :    # contamination
            hSmpl.Fill(rand.Gaus(0.5,0.1),rand.Gaus(0.5,0.1),rand.Gaus(0.5,0.1))
        Phi[0] = etest.Histo3DETest( hUni , hSmpl )
        if(sample%1==0):
            print "Sample %d" %(sample) +" ETest statistic for N=%d bins, sample %d, is %g"%(Nbins,sample,Phi)
        TEtest.Fill()
        del hSmpl



print "done filling %d events " % TEtest.GetEntries() + "in " + TEtest.GetTitle()
TEtest.Write()
FEtest.Close()
