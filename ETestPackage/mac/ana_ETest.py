# run:
# > python mac/ana_ppp.py <target A>

import ROOT
import os, sys
from ROOT import TPlots
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoUniFlat   = True

Nbins   = 100

Path    = "/Users/erezcohen/Desktop/EnergyTest/EnergyTestResults"

if len(sys.argv)>1:
    N = int(sys.argv[1])
else:
    print "operate using python ana_ETest.py <ETest Nbins = 30>"
    N = 30

FileName= "ETest%d"%N
ana     = TPlots(Path+"/"+FileName+".root" ,"ETestTree")




if DoUniFlat:
    canvas = ana.CreateCanvas("uniform vs constant comparison" )
    h = ana.H1("phiFlatUni" , ROOT.TCut() , "HIST" , Nbins , 0 , 1e-3
              , "ETest statistic uniform vs. constant at %dx%dx%d binning"%(N,N,N),"#phi")
    integral = h.Integral()
    CL95     = 0
    for bin in range (1,Nbins):
        if (h.Integral(1,bin) > 0.95*integral):
            CL95 = h.GetXaxis().GetBinCenter(bin)
            break
    ana.Line(CL95 , 0 , CL95 , h.GetMaximum()  , 2 , 2)
    ana.Text(CL95 , h.GetMaximum() , "CL_{95} = %g"%CL95 )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/ETestUniFlat_%d_bins.pdf"%N)


