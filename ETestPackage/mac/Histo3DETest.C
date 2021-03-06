// The 3-dimensional Energy Test (Aslan & Zech) applied to 3D ROOT histograms.
// Written by Erez O Cohen & Ivan D Reid, 2015
// ---------------------------------------------------------------------------
// To operate it:
// (1) create shared library
// gROOT -> ProcessLine(".L Histo3DETest.C++O");
// (2) in your application call it as you wish
// phi = Histo3DETest( Nbins , hD , hMC );
// ---------------------------------------------------------------------------

#include "Histo3DETest.h"

#include <cmath>
#include <iostream>

double Histo3DETest(const int Nbins, const TH3* hD, const TH3* hMC , bool flag_UNDERFLOW_OVERFLOW){

    //    std::cout << "flag_UNDERFLOW_OVERFLOW = " << flag_UNDERFLOW_OVERFLOW << std::endl;
    // Definitions
    const int N     = (flag_UNDERFLOW_OVERFLOW) ? Nbins + 2 : Nbins;
    int     Low     = (flag_UNDERFLOW_OVERFLOW) ? 0         : 0;
    int     High    = (flag_UNDERFLOW_OVERFLOW) ? Nbins + 1 : Nbins ;
    double  phiD    = 0.    , phiMC=0.      , phiDMC=0.;
    double step     = 1./(N-2);
    double stepsq   = pow(step,2);
    double d000     = log(0.66170*step);                    //"cube line picking" - avg. dist between 2 points
    double nD       = 0.    , nMC = 0.;
    // Declared variables are allocated on the stack, which has a fixed size. Allocated variables are put in the heap which is basically the rest of memory. So manually emulate the 3D arrays
    double *** D    = new double **[N];
    double *** MC   = new double **[N];
    double *** psi  = new double **[N];
    for (int ialloc=0; ialloc<N; ++ialloc) {
        D[ialloc]   = new double*[N];
        MC[ialloc]  = new double*[N];
        psi[ialloc] = new double*[N];
        for (int jalloc=0; jalloc<N; ++jalloc) {
            D[ialloc][jalloc]   = new double[N];
            MC[ialloc][jalloc]  = new double[N];
            psi[ialloc][jalloc] = new double[N];
        }
    }
    // Initilization
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
    double Dpart = 0,  MCpart = 0, DMCpart = 0;
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
                                    if((j1 < i1) ){
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
    // delete them before the end of the routine (at the same level of scope as the allocates) to avoid memory leaks
    for (int ialloc=N; --ialloc>=0;) {
        for (int jalloc=N; --jalloc>=0;) {
            delete [] psi[ialloc][jalloc];
            delete [] MC[ialloc][jalloc];
            delete [] D[ialloc][jalloc];
        }
        delete [] psi[ialloc];
        delete [] MC[ialloc];
        delete [] D[ialloc];
    }
    delete [] psi;
    delete [] MC;
    delete [] D;
    
    return ( phiD + phiMC + phiDMC );
}
