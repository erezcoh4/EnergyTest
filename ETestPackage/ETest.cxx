#ifndef ETEST_CXX
#define ETEST_CXX

#include "ETest.h"

ETest::ETest(const int Nbins , bool flag_UNDERFLOW_OVERFLOW){

    N       = (flag_UNDERFLOW_OVERFLOW) ? Nbins + 2 : Nbins;
    Low     = (flag_UNDERFLOW_OVERFLOW) ? 0         : 0;
    High    = (flag_UNDERFLOW_OVERFLOW) ? Nbins + 1 : Nbins ;
    step    = 1./(N-2);
    stepsq  = pow(step,2);
    d000    = log(0.66170*step);                    //"cube line picking" - avg. dist between 2 points
}


ETest::~ETest(){}






double ETest::Histo3DETest(const TH3* hD, const TH3* hMC){
    // Initilization
    nD = nMC = phiD = phiMC = phiDMC = Dpart   = MCpart    = DMCpart =  0;
    for (int i1 = Low; i1 < High; i1++){    // move to arrays instead of histogram to reduce expensive GetBinContent() calculation time
        for (int i2 = Low; i2 < High; i2++) {
            for (int i3 = Low; i3 < High; i3++) {
                D[i1][i2][i3] = hD -> GetBinContent(i1+1,i2+1,i3+1);
                MC[i1][i2][i3] = hMC -> GetBinContent(i1+1,i2+1,i3+1);
                psi[i1][i2][i3] = (i1==0 && i2==0 && i3==0) ? d000 : 0.5*log((i1*i1 + i2*i2 + i3*i3)*stepsq) ;
                nD    += hD -> GetBinContent(i1+1,i2+1,i3+1);
                nMC   += hMC -> GetBinContent(i1+1,i2+1,i3+1);
            }
        }
    }
    // Calculation...
    Dpart = MCpart = DMCpart = 0;
    for (int i1 = 0; i1 < N; i1++){
        for (int i2 = 0; i2 < N; i2++) {
            for (int i3 = 0; i3 < N; i3++) {
                double nDi = D[i1][i2][i3], nMCi = MC[i1][i2][i3];
                
                if (nDi!=0 || nMCi!=0) { // skip empty cells
                    Dpart   += 0.5*nDi*nDi*psi[0][0][0];
                    MCpart  += 0.5*nMCi*nMCi*psi[0][0][0];
                    
                    for (int j3 = 0; j3 < N; j3++){
                        if((j3 < i3) && (D[i1][i2][j3]!=0 || MC[i1][i2][j3]!=0)){
                            Dpart   += nDi*D[i1][i2][j3]*psi[0][0][i3-j3];
                            MCpart  += nMCi*MC[i1][i2][j3]*psi[0][0][i3-j3];
                        }
                        for (int j2 = 0; j2 < N; j2++){
                            if( (j2 < i2) && (D[i1][j2][j3]!=0 || MC[i1][j2][j3]!=0)){
                                Dpart   += nDi*D[i1][j2][j3]*psi[0][i2-j2][abs(i3-j3)];
                                MCpart  += nMCi*MC[i1][j2][j3]*psi[0][i2-j2][abs(i3-j3)];
                            }
                            for (int j1 = 0; j1 < N; j1++){
                                if (D[j1][j2][j3]!=0 || MC[j1][j2][j3]!=0) {
                                    if(j1 < i1 ){
                                        Dpart   += nDi*D[j1][j2][j3]*psi[i1-j1][abs(i2-j2)][abs(i3-j3)];
                                        MCpart  += nMCi*MC[j1][j2][j3]*psi[i1-j1][abs(i2-j2)][abs(i3-j3)];
                                    }
                                    DMCpart += nDi*MC[j1][j2][j3]*psi[abs(i1-j1)][abs(i2-j2)][abs(i3-j3)];
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    // normalization
    phiD    = -Dpart  /(nD  * nD);
    phiMC   = -MCpart /(nMC * nMC);
    phiDMC  = DMCpart /(nD  * nMC);
    //        Printf("ø(D) = %f, ø(MC) = %f, ø(D-MC) = %f",phiD,phiMC,phiDMC);

    return ( phiD + phiMC + phiDMC );
}







TString  ETest::ETestPower (TH1F * hPhi , float CL95){
    float power = 1 - (hPhi->Integral( 0 , hPhi->GetXaxis()->FindBin(CL95))/ hPhi->Integral());
    TString res = Form("ETest power = %.3f",power);
    std::cout << res << std::endl;
    return res;
}



TGraphErrors * ETest::cutoff_graph(){
    const int        N  = 10;
    double CutoffPar[N] = {0.1   , 0.2   , 0.3   , 0.4   , 0.5   , 0.6   , 0.7   , 0.8   , 0.9   , 1.0   };
    double  COParErr[N] = {0.01  , 0.01  , 0.01  , 0.01  , 0.01  , 0.01  , 0.01  , 0.01  , 0.01  , 0.01  };
    // discrimination power for Uniform / Unifrom with Gaussian contamination of 0.1% trivariate (0.5,0.1) gaussian
    double      CL95[N] = {6.25  , 5.55  , 5.15  , 4.85  , 4.65  , 4.45  , 4.35  , 4.15  , 4.05  , 3.95 }; // x 10^{-6}
    double     Power[N] = {0.13  , 0.132  , 0.129  , 0.132  , 0.124  , 0.129  , 0.115  , 0.132  , 0.129  , 0.127 };
    double  PowerErr[N] = {0.01 , 0.01 , 0.01 , 0.01 , 0.01 , 0.01 , 0.01 , 0.01 , 0.01 , 0.01 };
//    TCanvas * c = new TCanvas("cutoff","cutoff");
    TGraphErrors * g = new TGraphErrors( N, CutoffPar, Power, COParErr, PowerErr );
    g -> SetTitle("ETest discrimination power as a function of <r>");
    g -> GetXaxis() -> SetTitle("cutoff parameter <r>");
    g -> GetYaxis() -> SetTitle("Discrimination Power");
    g -> GetYaxis() -> SetRangeUser(0.05,0.2);
    return g;
//    c -> SaveAs("~/Desktop/CutoffParameter.pdf");
}


#endif
