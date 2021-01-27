/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * blinkLED_types.h
 *
 * Code generation for function 'blinkLED'
 *
 */

#ifndef BLINKLED_TYPES_H
#define BLINKLED_TYPES_H

/* Include files */
#include "rtwtypes.h"

/* Custom Header Code */
#include "MW_raspi_init.h"
#include "MW_Pyserver_control.h"

/* Type Definitions */
#ifndef struct_emxArray_char_T
#define struct_emxArray_char_T

struct emxArray_char_T
{
  char *data;
  int *size;
  int allocatedSize;
  int numDimensions;
  bool canFreeData;
};

#endif                                 /*struct_emxArray_char_T*/

#ifndef typedef_emxArray_char_T
#define typedef_emxArray_char_T

typedef struct emxArray_char_T emxArray_char_T;

#endif                                 /*typedef_emxArray_char_T*/
#endif

/* End of code generation (blinkLED_types.h) */
