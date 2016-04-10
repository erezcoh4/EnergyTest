# run:
# > python ana_ETest.py <ETest Nbins = 30> <Cutoff parameter = 0.6617>

import ROOT , os, sys
from ROOT import TPlots , ETest
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoUniFlat               = False
DoUniUni                = False
DoUniUniCutOffParameter = False
DoUniUniContamination   = False
DoUniUniContCutoffPar   = False
DoUniUniContCOPgraph    = False
DoCompareGausCont       = True


Nbins   = 100
Path    = "/Users/erezcohen/Desktop/EnergyTest/EnergyTestResults"
plot    = TPlots()

if len(sys.argv)>1:
    N = int(sys.argv[1])
else:
    print "run: \n > python ana_ETest.py <ETest Nbins = 30> <Cutoff parameter = 0.6617>"
    sys.exit(0)


if DoUniFlat:
    FileName = "ETest%d"%N

elif DoUniUni:
    Path = Path + "/" + "DifferentBinning"
    FileName    = "UniUni%d"%(N)

elif DoUniUniCutOffParameter:
    CutOffParameter = float(sys.argv[2])
    FileName    = "UniUni%d_Cutoff_%.1f"%(N,CutOffParameter)

elif DoUniUniContamination:
    Path = Path + "/" + "DifferentBinning"
    CutOffParameter = 0.6617
    nContamination = 0.1    # [%] of contammination
    FileName = "UniGaus%.1fCont_Nbins%d"%(nContamination,N)

elif DoUniUniContCutoffPar:
    Path        = Path+"/"+"DifferentCutoff"
    CutOffParameter = float(sys.argv[2])
    nContamination = 0.1    # [%] of contammination
    FileName    = "Uni_Cutoff%.1f_Gaus%.1fCont"%(CutOffParameter,nContamination) # only for N=30




if DoUniUniContCOPgraph==False and DoCompareGausCont==False :
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
    h = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 10 , "ETest statistic uniform/uniform, %dx%dx%d binning"%(N,N,N),"#phi x 10^{6}")
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
    h = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 10 , "ETest uni/uni, %dx%dx%d binning, cutoff = %.4f"%(N,N,N,CutOffParameter),"#phi [x 10^{6}]")
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
    # 95% confidence levels for uniform/uniform comparisons [x 10^{-6}] (Nbins:CL95)
    CL95list = {10:3.35 , 20:4.05 , 30:4.10 ,40:4.65 , 50:4.85} # 50 still missing.... also have 70....
    # 95% confidence levels for uniform/constant comparisons [x 10^{-6}] (Nbins:CL95)
    #    CL95list = {10:1.675 , 20:1.975, 30:2.175 ,40:3.675 , 50:3.475}
    for key,val in CL95list.items():
        if key == N:
            CL95 = val
    print "CL95 = %g"%CL95
    etest   = ETest(N)
    canvas  = ana.CreateCanvas("uni./uni. + contamination" )
    hPhi    = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 8. , "uni./uni. + %.2f%% contamination at %d binning"%(nContamination,N),"#phi x 10^{6}")
    ana.Line(CL95 , 0 , CL95 , hPhi.GetMaximum()  , 2 , 2)
    ana.Text(CL95 , hPhi.GetMaximum() , etest.ETestPower (hPhi , CL95) )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/UniUni%.2fCont_%d.pdf"%(nContamination,N))


if DoUniUniContCutoffPar:
    #  95% confidence levels for uniform/uniform comparisons [x 10^{-6}] (cutoff : CL95)
    CL95list = {0.1:6.25 , 0.2:5.55 , 0.3:5.15 ,0.4:4.85 , 0.5:4.65 , 0.6:4.45 , 0.7:4.35 , 0.8:4.15 , 0.9:4.05 , 1.0:3.95} # x 10^{-6}
    for key,val in CL95list.items():
        if key == CutOffParameter:
            CL95 = val
    print "CL95 = %g"%CL95
    etest   = ETest(N)
    canvas  = ana.CreateCanvas("uni./uni. + contamination" )
    hPhi    = ana.H1("1e6*phi" , ROOT.TCut() , "HIST" , Nbins , 0 , 10. , "uni./uni. + %.2f%% cont. at %d binning, cutoff=%g"%(nContamination,N,CutOffParameter),"#phi x 10^{6}")
    ana.Line(CL95 , 0 , CL95 , hPhi.GetMaximum()  , 2 , 2)
    ana.Text(CL95 , hPhi.GetMaximum() , etest.ETestPower (hPhi , CL95) )
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/"+FileName+".pdf")


if DoUniUniContCOPgraph:
    etest   = ETest(30)
    canvas  = plot.CreateCanvas("uni./uni. + contamination at different cutoffs" )
    g = etest.cutoff_graph()
    g.Draw("apc")
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/CutoffParameter.pdf")



if DoCompareGausCont:
    etest   = ETest(N)
    CL95    = 4.10
    canvas  = plot.CreateCanvas("uni./uni. + n% contamination" )
    anaCont = []
    hPhi    = []
    n       = [ 0.0 , 0.01  , 0.1   , 0.7   , 1.0   , 1.3   , 3.0   , 5.0   ]
    color   = [ 1   , 2     , 3     , 4     , 6     , 7     , 8     , 9     ]
    MAX     = 0.31
    for i in range(len(n)):
        FileName = "UniGaus%.2fCont_Nbins%d"%(n[i],N)
        anaCont.append(TPlots(Path+"/"+FileName+".root" ,"ETestTree"))
        hPhi.append(anaCont[i].H1("1e6*phi",ROOT.TCut(),"hist same",175,0,70,"","ETest statistic, #phi x 10^{6}","",color[i],color[i]))
        if hPhi[i].Integral():
            hPhi[i].Scale(1./hPhi[i].Integral())
        hPhi[i].GetYaxis().SetRangeUser(0,MAX)
        anaCont[i].Text(hPhi[i].GetMean()+hPhi[i].GetRMS(),MAX*(1-float(i)/len(n)),"%.2f%%, ETest power=%.3f"%(n[i],etest.ETestPower(hPhi[i] , CL95)) ,color[i],0.03)
#        anaCont[i].Text(1,0.1,"%.2f%% contamination" ,1)
    plot.Line(CL95 , 0 , CL95 , MAX , 2 , 2 , 2)
    canvas.Update()
    wait()
    canvas.SaveAs("~/Desktop/UniUniGausContNbins30.pdf")


