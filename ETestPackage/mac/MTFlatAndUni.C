// multi-thread ETest calculaiton of constant and uniform distributions, operate only in compilation node
// root -l MTFlatAndUni.C+

#include "TRandom3.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TCanvas.h"
#include <iostream>
#include "TROOT.h"
#include "TStopwatch.h"
#include "TMath.h"
#include "TRandom1.h"
#include "TRandom2.h"
#include "TRandom3.h"
#include "TH2.h"
#include "TSystem.h"
#include "TThread.h"
#include "TMemFile.h"
#include "TTree.h"

#include "Histo3DETest.h"


//____________________________MultiThread__________________________//
const int       Nthreads = 1;
int            i_thread;
TThread *Thread[Nthreads];
typedef struct {
    TString name;
    Int_t id , iMin , iMax , NSamples ;
} Thrd_arg;
Thrd_arg    args[Nthreads];
Double_t     cpu[Nthreads];
Double_t        cputot  = 0;
int             upd     = 1;
TStopwatch      timer;
//_________________________________________________________________________//
int     Nbins               ,   NTotSamples     ,  Npoints = 1e6    ,   PointsInBin ;
Double_t    ETestFlatUni    ,   ETestUniUni;
TString FileName("../ETestResults/ConstAndFlatComparisonsResults.root");
TFile * OutFile;
TTree * OutTree;
TH1F    * hUniVsConst       , * hUniVsUni;
TH3F    * flat              , * huniform ;
//_________________________________________________________________________//





//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void SplitNSamplesIntoThreads(){
    for (i_thread = 0 ; i_thread < Nthreads ; i_thread++ ){
        args[i_thread].name     = Form("Thread %d",i_thread);
        args[i_thread].id       = i_thread;
        args[i_thread].iMin     = i_thread*(NTotSamples/Nthreads);
        args[i_thread].iMax     = (i_thread+1)*(NTotSamples/Nthreads);
        args[i_thread].NSamples = (int)((float)NTotSamples/Nthreads);
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void InitializeFlatAndUniHistograms(){
    
    hUniVsConst  = new TH1F("hUniVsConst"    ,Form("%dk uniform points vs. constant distribution (Nbins=%d)",Npoints/1000,Nbins),1000,0,.00001);
    hUniVsUni    = new TH1F("hUniVsUni"      ,Form("%dk uniform distribution comparison (Nbins=%d)",Npoints/1000,Nbins),1000,0,.00001);
    flat         = new TH3F("Flat"           ,"Flat Reference"       ,Nbins,0.,1.,Nbins,0.,1.,Nbins,0.,1.);
    huniform     = new TH3F("huniform"       ,"Uniform Reference"    ,Nbins,0.,1.,Nbins,0.,1.,Nbins,0.,1.);
    
    Printf("generate contant of (%dx%dx%d) binning with %d points in each bin",Nbins,Nbins,Nbins,PointsInBin);
    TRandom3 * r3   = new TRandom3(0);
    for (int i1 = 1; i1 <= Nbins; i1++ ) //Don't fill the outlier bins!
        for (int i2 = 1; i2 <= Nbins; i2++ )
            for (int i3 = 1; i3 <= Nbins; i3++ )
                flat -> SetBinContent(i1,i2,i3,PointsInBin);
    for (int i = 0; i < Npoints; i++)
        huniform -> Fill(r3->Uniform(),r3->Uniform(),r3->Uniform());
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void *ETestConstAndFlat(void *ptr){
    timer.Start();
    TRandom3 * r3   = new TRandom3(0);
    Thrd_arg * arg  = (Thrd_arg *) ptr;
    Int_t ID = arg->id;
    for (int sample = arg->iMin ; sample < arg->iMax ; sample++){
        TH3F* hsample= new TH3F(Form("hsample%d",ID),"Uniform sample",Nbins,0.,1.,Nbins,0.,1.,Nbins,0.,1.);
        for (int i = 0; i < Npoints; i++)
            hsample -> Fill(r3->Uniform(),r3->Uniform(),r3->Uniform());
        ETestFlatUni = Histo3DETest( Nbins , hsample , flat );
        hUniVsConst -> Fill(ETestFlatUni);
//        ETestUniUni = Histo3DETest( Nbins , hsample , huniform );
//        hUniVsUni   -> Fill(ETestUniUni);
        OutTree     -> Fill();
        hsample -> Delete();
        if ( sample % 10 == 0 )
            TThread::Printf("(%s) [Nbins=%d]: Flat/Uni = %lf, Uni/Uni = %lf [%.0f%%]",arg->name.Data(),Nbins,ETestFlatUni,ETestUniUni,100*(float)(sample-arg->iMin)/arg->NSamples);
        if (sample && (sample%upd)==0)
            gSystem->Sleep(1);
    }
    if(ID==Nthreads-1) TThread::Printf("\n");

    timer.Stop();
    cpu[ID] = timer.CpuTime();
    cputot += cpu[ID];
    return 0;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void CloseCalcualtion(){
    Printf("filled %d events...",(int)OutTree->GetEntries());
    OutTree -> Write();
    OutFile -> Write();
    OutFile -> Close();
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void MTFlatAndUni(int fNbins = 10 , int fNTotSamples = 1e2, int FileNumber=-1){
    FileName = TString(Form("../ETestResults/ETestResults_%d_bins%s.root",fNbins,(FileNumber==-1)?"":Form("%d",FileNumber)));
    Nbins       = fNbins;
    NTotSamples = fNTotSamples;
    system(Form("rm %s",FileName.Data()));
    OutFile = new TFile(FileName.Data(),"recreate");
    OutTree = new TTree("ETestTree","energy test results");
    OutTree -> Branch("phiFlatUni"  ,&ETestFlatUni  ,"phiFlatUni/D");
    OutTree -> Branch("phiUniUni"   ,&ETestUniUni   ,"phiUniUni/D");
    OutTree -> Branch("Nbins"       ,&Nbins         ,"Nbins/I");

    
    
    PointsInBin = (int)((float)Npoints/(Nbins*Nbins*Nbins));
    InitializeFlatAndUniHistograms();
    SplitNSamplesIntoThreads();
    for (i_thread = 0 ; i_thread < Nthreads ; i_thread ++ ) {
        Thread[i_thread] = new TThread(Form("Thread%d",i_thread),ETestConstAndFlat,(void*) &args[i_thread]);
        Thread[i_thread] -> Run();
    }
    for (i_thread = 0 ; i_thread < Nthreads; i_thread ++)
      Thread[i_thread] -> Join();
    for (i_thread = 0 ; i_thread < Nthreads ; i_thread ++ ){
        TThread::Printf("(%s Finished) Cpu=%7.3f s, cputot = %.3f s" ,args[i_thread].name.Data(),cpu[i_thread],cputot);
        delete Thread[i_thread];
    }
    CloseCalcualtion();
}

