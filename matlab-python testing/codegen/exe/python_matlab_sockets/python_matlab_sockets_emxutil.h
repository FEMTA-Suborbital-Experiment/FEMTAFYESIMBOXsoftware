/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * python_matlab_sockets_emxutil.h
 *
 * Code generation for function 'python_matlab_sockets_emxutil'
 *
 */

#ifndef PYTHON_MATLAB_SOCKETS_EMXUTIL_H
#define PYTHON_MATLAB_SOCKETS_EMXUTIL_H

/* Include files */
#include "python_matlab_sockets_types.h"
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
  extern void emxEnsureCapacity_uint8_T(emxArray_uint8_T *emxArray, int oldNumel);
  extern void emxFree_uint8_T(emxArray_uint8_T **pEmxArray);
  extern void emxInit_uint8_T(emxArray_uint8_T **pEmxArray, int numDimensions);

#ifdef __cplusplus

}
#endif
#endif

/* End of code generation (python_matlab_sockets_emxutil.h) */
