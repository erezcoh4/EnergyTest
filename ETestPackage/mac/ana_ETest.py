# run:
# > python mac/ana_ppp.py <target A>

import ROOT , os, sys
from ROOT import TPlots , ETest
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoUniFlat               = False
DoUniUni                = False
DoUniUniCutOffParameter = True
DoUniUniContamination   = False
Nbins   = 100

Path    = "/Users/erezcohen/Desktop/EnergyTest/EnergyTestResults"

if len(sys.argv)>1:
    N = int(sys.argv[1])
else:
    print "operate using python ana_ETest.py <ETest Nbins = 30> <Cutoff parameter = 0.6617>"
    sys.exit(0)

if DoUniFlat:
    FileName = "ETest%d"%N
elif DoUniUni:
    FileName    = "UniUni%d"%(N)
elif DoUniUniCutOffParameter:
    CutOffParameter = float(sys.argv[2])
    FileName    = "UniUni%d_Cutoff_%.4f"%(N,CutOffParameter)
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
    h = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 0.1 , "ETest statistic uniform/uniform, %dx%dx%d binning"%(N,N,N),"#phi [x 10^{-6}]")
    integral = h.Integral()
    CL95     = 0
    for bin in range (1,Nbins):
        if (h.Integral(1,bin) > 0.95*integral):
            CL95 = h.GetXaxis().GetBinCenter(bin)
            break
    ana.Line(CL95 , 0 , CL95 , h.GetMaximum()  , 2 , 2)
    ana.Text(CL95 , h.GetMaximum() , "CL_{95} = %g x 10^{-6}"%CL95 )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/ETestUniUni_%d_bins.pdf"%N)



if DoUniUniCutOffParameter:
    canvas = ana.CreateCanvas("uniform vs uniform comparison" )
    h = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 60 , "ETest uni/uni, %dx%dx%d binning, cutoff = %.4f"%(N,N,N,CutOffParameter),"#phi [x 10^{-6}]")
    integral = h.Integral()
    CL95     = 0
    for bin in range (1,Nbins):
        if (h.Integral(1,bin) > 0.95*integral):
            CL95 = h.GetXaxis().GetBinCenter(bin)
            break
    ana.Line(CL95 , 0 , CL95 , h.GetMaximum()  , 2 , 2)
    ana.Text(CL95 , h.GetMaximum() , "CL_{95} = %g x 10^{-6}"%CL95 )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/ETest"+FileName+".pdf")


if DoUniUniContamination:
#    # 95% confidence levels for uniform/uniform comparisons [x 10^{-6}] (Nbins:CL95)
#    CL95list = {10:0.0755 , 20:0.0795, 30:0.0815 ,40:0.0815 , 50:0.0835}
    # 95% confidence levels for uniform/constant comparisons [x 10^{-6}] (Nbins:CL95)
    CL95list = {10:1.675 , 20:1.975, 30:2.175 ,40:3.675 , 50:3.475}
    for key,val in CL95list.items():
        if key == N:
            CL95 = val
    print "CL95 = %g"%CL95
    etest   = ETest(N)
    canvas  = ana.CreateCanvas("uni./uni. + contamination" )
    hPhi    = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 6. , "uni./uni. + %.2f%% contamination at %d binning"%(nContamination,N),"#phi [x 10^{-6}]")
    ana.Line(CL95 , 0 , CL95 , hPhi.GetMaximum()  , 2 , 2)
    ana.Text(CL95 , hPhi.GetMaximum() , etest.ETestPower (hPhi , CL95) )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/UniUni%.2fCont_%d.pdf"%(nContamination,N))

