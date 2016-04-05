import ROOT
from ROOT import ETest , TRandom3
from ROOT import TFile, TTree
from array import array
import numpy as n

rand    = TRandom3()

DoUniformUniform    = True




FEtest  = ROOT.TFile("~/Desktop/EnergyTest/AnaFiles/ETestResults.root","recreate");
TEtest  = ROOT.TTree("EtestTree","ETest statistic");
Nbins = [10 ,20 ,30 ,40 , 50]
Phi10 = n.zeros(1, dtype=float)
TEtest.Branch( "Phi10" , Phi10 , "Phi10/D" )
Phi20 = n.zeros(1, dtype=float)
TEtest.Branch( "Phi20" , Phi20 , "Phi20/D" )
Phi30 = n.zeros(1, dtype=float)
TEtest.Branch( "Phi30" , Phi30 , "Phi30/D" )
Phi40 = n.zeros(1, dtype=float)
TEtest.Branch( "Phi40" , Phi40 , "Phi40/D" )
Phi50 = n.zeros(1, dtype=float)
TEtest.Branch( "Phi50" , Phi50 , "Phi50/D" )

etest = []
hFlat = []
hSmpl = []


if DoUniformUniform:
    
    
    Npoints = 135000
    Nsamples= 1000
    
    for i in range(0,len(Nbins)):
        etest.append(ETest(Nbins[i]))
        
        # for each binning, we create a sample of constant distribution over the unit cube

        hFlat.append(ROOT.TH3F("hFlat_%d"%(Nbins[i]),"Flat Distribution Nbins=%d"%Nbins[i],Nbins[i],0,1,Nbins[i],0,1,Nbins[i],0,1))
        bin_content = Npoints/(Nbins[i]*Nbins[i]*Nbins[i])
        for i1 in range(1,Nbins[i]) :
            for i2 in range(1,Nbins[i]) :
                for i3 in range(1,Nbins[i]) :
                    hFlat[i].SetBinContent(i1,i2,i3,bin_content);



    for sample in range(0,Nsamples) :
        print "Sample %d" %(sample)
        
        for i in range(0,len(Nbins)):
            
            # for each binning, we create a sample of uniform distribution over the unit cube
            
            hSmpl.append(ROOT.TH3F("hSmpl_%d_%d"%(sample,Nbins[i]),"Uniform sample Nbins=%d"%Nbins[i],Nbins[i],0,1,Nbins[i],0,1,Nbins[i],0,1))
        
        for j in range(0,Npoints) :
            
            x = rand.Uniform()
            y = rand.Uniform()
            z = rand.Uniform()
            
            for i in range(0,len(Nbins)):
                
                hSmpl[i].Fill(x,y,z)


        Phi10[0] = etest[0].Histo3DETest( hSmpl[0] , hFlat[0] )
        print "ETest statistic for N=10 bins, sample %d is %g"%(sample,Phi10)
        Phi20[0] = etest[1].Histo3DETest( hSmpl[1] , hFlat[1] )
        print "ETest statistic for N=20 bins, sample %d is %g"%(sample,Phi20)
        Phi30[0] = etest[2].Histo3DETest( hSmpl[2] , hFlat[2] )
        print "ETest statistic for N=30 bins, sample %d is %g"%(sample,Phi30)
        Phi40[0] = etest[3].Histo3DETest( hSmpl[3] , hFlat[3] )
        print "ETest statistic for N=40 bins, sample %d is %g"%(sample,Phi40)
        Phi50[0] = etest[4].Histo3DETest( hSmpl[4] , hFlat[4] )
        print "ETest statistic for N=50 bins, sample %d is %g"%(sample,Phi50)

        TEtest.Fill()

        del hSmpl[:]

print "done filling %d events " % TEtest.GetEntries() + "in " + TEtest.GetTitle()

TEtest.Write()
FEtest.Close()

