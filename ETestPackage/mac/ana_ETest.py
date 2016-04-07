# run:
# > python mac/ana_ppp.py <target A>

import ROOT , os, sys
from ROOT import TPlots , ETest
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoUniFlat               = False
DoUniUniContamination   = True
Nbins   = 100

Path    = "/Users/erezcohen/Desktop/EnergyTest/EnergyTestResults"

if len(sys.argv)>1:
    N = int(sys.argv[1])
else:
    print "operate using python ana_ETest.py <ETest Nbins = 30>"
    sys.exit(0)

if DoUniFlat:
    FileName = "ETest%d"%N
elif DoUniUni:
    FileName    = "UniUni_Nbins_%d"%(N)
elif DoUniUniContamination:
    nContamination = 0.1    # [%] of contammination
    FileName    = "UniUni%.2fCont_%d"%(nContamination,N)

ana     = TPlots(Path+"/"+FileName+".root" ,"ETestTree")




if DoUniFlat:
    canvas = ana.CreateCanvas("uniform vs constant comparison" )
    h = ana.H1("phiFlatUni" , ROOT.TCut() , "HIST" , Nbins , 0 , 5e-6
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



if DoUniUni:
    canvas = ana.CreateCanvas("uniform vs constant comparison" )
    h = ana.H1("phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 5e-6 , "ETest statistic uniform/uniform, %dx%dx%d binning"%(N,N,N),"#phi")
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
    canvas.SaveAs("~/Desktop/ETestUniUni_%d_bins.pdf"%N)


if DoUniUniContamination:
#    CL95    = (["10x10x10",1.675e-06],["20x20x20",1.975e-06],["30x30x30",2.175e-06],["40x40x40",3.675e-06],["50x50x50",3.475e-06])
    CL95list = {10:1.675e-06, 20:1.975e-06, 30:2.175e-06 ,40:3.675e-06 , 50:3.475e-06}
    for key,val in CL95list.items():
        if key == N:
            CL95 = val
    print "CL95 = %g"%CL95
    etest   = ETest(N)
    canvas  = ana.CreateCanvas("uni./uni. + contamination" )
    hPhi    = ana.H1("phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 1e-6 , "uni./uni. + %.2f%% contamination at %d binning"%(nContamination,N),"#phi")
    ana.Text(CL95 , hPhi.GetMaximum() , etest.ETestPower (hPhi , CL95) )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/UniUni%.2fCont_%d.pdf"%(N,nContamination))

