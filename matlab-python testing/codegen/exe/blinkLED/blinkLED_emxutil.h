/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * blinkLED_emxutil.h
 *
 * Code generation for function 'blinkLED_emxutil'
 *
 */

#ifndef BLINKLED_EMXUTIL_H
#define BLINKLED_EMXUTIL_H

/* Include files */
#include "blinkLED_types.h"
#include "rtwtypes.h"
#include <stddef.h>
#include <stdlib.h>

/* Custom Header Code */
#include "MW_raspi_init.h"
#include "MW_Pyserver_control.h"
#ifdef __cplusplus

extern "C" {

#endif

  /* Function Declarations */
  extern void emxEnsureCapacity_char_T(emxArray_char_T *emxArray, int oldNumel);
  extern void emxFree_char_T(emxArray_char_T **pEmxArray);
  extern void emxInit_char_T(emxArray_char_T **pEmxArray, int numDimensions);

#ifdef __cplusplus

}
#endif
#endif

/* End of code generation (blinkLED_emxutil.h) */
