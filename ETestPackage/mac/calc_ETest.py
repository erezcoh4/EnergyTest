import ROOT
from ROOT import ETest , TRandom3
from ROOT import TFile, TTree
from array import array

etest   = ETest()
rand    = TRandom3()

DoUniformUniform    = True


Nbins = 30

FEtest  = ROOT.TFile("~/Desktop/EnergyTest/AnaFiles/ETestResults.root","recreate");
TEtest  = ROOT.TTree("EtestTree","ETest statistic");
Phi = array( 'f', [ 0 ] )
TEtest.Branch("Phi" , Phi , "Phi/F");





if DoUniformUniform:
    Npoints = 135
    Nsamples= 10
    hFlat   = ROOT.TH3F("fFlat","Flat Distribution",Nbins,0,1,Nbins,0,1,Nbins,0,1)
    for i1 in range(1,Nbins) :
        for i2 in range(1,Nbins) :
            for i3 in range(1,Nbins) :
                hFlat.SetBinContent(i1,i2,i3,5);
    for sample in range(0,Nsamples) :
        hSample = ROOT.TH3F("hSample%d"%sample,"Uniform sample",Nbins,0,1,Nbins,0,1,Nbins,0,1)
        for i in range(0,Npoints) :
            hSample.Fill(rand.Rndm(),rand.Rndm(),rand.Rndm())
        Phi = etest.Histo3DETest( Nbins , hSample , hFlat )
        TEtest.Fill()
        print "ETest statistic in sample %d is %.3f"%(sample,Phi)
    TEtest.Write()
    FEtest.Close()




print "done filling %d events in %s"%(TEtest.GetEntries(),TEtest.GetTitle())

