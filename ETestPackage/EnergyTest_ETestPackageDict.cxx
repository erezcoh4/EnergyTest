// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME EnergyTest_ETestPackageDict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "ETest.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *ETest_Dictionary();
   static void ETest_TClassManip(TClass*);
   static void delete_ETest(void *p);
   static void deleteArray_ETest(void *p);
   static void destruct_ETest(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ETest*)
   {
      ::ETest *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ETest));
      static ::ROOT::TGenericClassInfo 
         instance("ETest", "ETest.h", 34,
                  typeid(::ETest), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ETest_Dictionary, isa_proxy, 4,
                  sizeof(::ETest) );
      instance.SetDelete(&delete_ETest);
      instance.SetDeleteArray(&deleteArray_ETest);
      instance.SetDestructor(&destruct_ETest);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ETest*)
   {
      return GenerateInitInstanceLocal((::ETest*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::ETest*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ETest_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ETest*)0x0)->GetClass();
      ETest_TClassManip(theClass);
   return theClass;
   }

   static void ETest_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrapper around operator delete
   static void delete_ETest(void *p) {
      delete ((::ETest*)p);
   }
   static void deleteArray_ETest(void *p) {
      delete [] ((::ETest*)p);
   }
   static void destruct_ETest(void *p) {
      typedef ::ETest current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ETest

namespace {
  void TriggerDictionaryInitialization_libEnergyTest_ETestPackage_Impl() {
    static const char* headers[] = {
"ETest.h",
0
    };
    static const char* includePaths[] = {
"/Users/erezcohen/larlite/UserDev/mySoftware",
"/usr/local/Cellar/root6/6.06.02/include/root",
"/Users/erezcohen/larlite/UserDev/EnergyTest/ETestPackage/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libEnergyTest_ETestPackage dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$ETest.h")))  ETest;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libEnergyTest_ETestPackage dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "ETest.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"ETest", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libEnergyTest_ETestPackage",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libEnergyTest_ETestPackage_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libEnergyTest_ETestPackage_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libEnergyTest_ETestPackage() {
  TriggerDictionaryInitialization_libEnergyTest_ETestPackage_Impl();
}
