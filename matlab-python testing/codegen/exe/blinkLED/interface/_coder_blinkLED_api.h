/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_blinkLED_api.h
 *
 * Code generation for function 'blinkLED'
 *
 */

#ifndef _CODER_BLINKLED_API_H
#define _CODER_BLINKLED_API_H

/* Include files */
#include "emlrt.h"
#include "tmwtypes.h"
#include <string.h>

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

#ifdef __cplusplus

extern "C" {

#endif

  /* Function Declarations */
  void blinkLED(void);
  void blinkLED_api(void);
  void blinkLED_atexit(void);
  void blinkLED_initialize(void);
  void blinkLED_terminate(void);
  void blinkLED_xil_shutdown(void);
  void blinkLED_xil_terminate(void);

#ifdef __cplusplus

}
#endif
#endif

/* End of code generation (_coder_blinkLED_api.h) */
