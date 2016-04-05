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

/**
   \class ETest
   User defined class ETest ... these comments are used to generate
   doxygen documentation!
 */
class ETest{

public:


    
    /// Default constructor
    ETest(){}
    
    /// Default destructor
    ~ETest(){}
    
    
    double Histo3DETest(const int, const TH3*, const TH3*, bool flag_UNDERFLOW_OVERFLOW=false);
    
    
};

#endif
/** @} */ // end of doxygen group 

