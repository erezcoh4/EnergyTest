import ROOT , sys
from ROOT import ETest , TRandom3
from ROOT import TFile , TTree
from array import array
import numpy as n

rand    = TRandom3()

DoUniformUniform    = True


Nbins = 10

FileName    = "ETestResults_Nbins_%d"%Nbins
#Path    = "/home/erez/EnergyTest/ETestResults"
Path    = "/Users/erezcohen/Desktop/EnergyTest/ETestResults"
FileNumber  = int(sys.argv[1])
FEtest  = ROOT.TFile(Path+"/"+FileName+"_%d.root"%FileNumber,"recreate");
TEtest  = ROOT.TTree("ETestTree","ETest statistic");
fNbins  = n.zeros(Nbins, dtype=int)
Phi     = n.zeros(1, dtype=float)
TEtest.Branch( "Nbins"      , fNbins, "Nbins/I" )
TEtest.Branch( "phiFlatUni" , Phi   , "phiFlatUni/D" )

etest = ETest(Nbins)

if DoUniformUniform:
    
    
    Npoints = 135000
    Nsamples= 2
        

    hFlat = ROOT.TH3F("hFlat_%d"%(Nbins),"Flat Distribution Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
    bin_content = Npoints/(Nbins*Nbins*Nbins)
    for i1 in range(1,Nbins) :
        for i2 in range(1,Nbins) :
            for i3 in range(1,Nbins) :
                hFlat.SetBinContent(i1,i2,i3,bin_content);

    etest.SetD(hFlat)

    for sample in range(0,Nsamples) :
        print "Sample %d" %(sample)
        
        hSmpl = ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins),"Uniform sample Nbins=%d"%Nbins,Nbins,0,1,Nbins,0,1,Nbins,0,1)
        
        for j in range(0,Npoints) :
            
            x = rand.Uniform()
            y = rand.Uniform()
            z = rand.Uniform()
            hSmpl.Fill(x,y,z)

        Phi = etest.ETestKnowingD ( hSmpl )
        print "ETest statistic for N=50 bins, sample %d is %g"%(sample,Phi)
        TEtest.Fill()
        del hSmpl

print "done filling %d events " % TEtest.GetEntries() + "in " + TEtest.GetTitle()

TEtest.Write()
FEtest.Close()

