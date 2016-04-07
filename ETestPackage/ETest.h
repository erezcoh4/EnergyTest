/**
 * \file ETest.h
 *
 * \ingroup ETestPackage
 * 
 * \brief The 3-dimensional Energy Test (Aslan & Zech) applied to 3D ROOT histograms. Written by Erez O Cohen & Ivan D Reid, 2015
 *
 * @author erezcohen
 */

// ---------------------------------------------------------------------------
// To operate it:
// phi = Histo3DETest( Nbins , hD , hMC );
// ---------------------------------------------------------------------------

/** \addtogroup ETestPackage

    @{*/
#ifndef ETEST_H
#define ETEST_H

#include <iostream>
#include "TH3.h"
#include "TError.h"
#include <cmath>
#include <iostream>
//#include "MySoftwarePackage/TPlots.h"
#define MAX 50
/**
   \class ETest
   User defined class ETest ... these comments are used to generate
   doxygen documentation!
 */
class ETest{

public:

    
    int N;
    int     Low  , High   ;
    double phiD  , phiMC    , phiDMC    , step , stepsq    , d000  , nD    , nMC;
//    double *** D , *** MC   , *** psi;
    double D[MAX][MAX][MAX] , MC[MAX][MAX][MAX]   , psi[MAX][MAX][MAX];
    double Dpart,  MCpart, DMCpart;

    
    /// Default constructor
    ETest (const int, bool flag_UNDERFLOW_OVERFLOW=false);
    
    /// Default destructor
    ~ETest();
    
    
    double  Histo3DETest (const TH3*, const TH3*);
    double          SetD (const TH3* hD);
    double ETestKnowingD (const TH3* hMC);
    TString   ETestPower (TH1F * hPhi , float CL95);
    
};

#endif
/** @} */ // end of doxygen group 

