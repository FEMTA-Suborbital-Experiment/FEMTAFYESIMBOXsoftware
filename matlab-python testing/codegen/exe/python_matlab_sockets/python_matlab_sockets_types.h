/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * python_matlab_sockets_types.h
 *
 * Code generation for function 'python_matlab_sockets'
 *
 */

#ifndef PYTHON_MATLAB_SOCKETS_TYPES_H
#define PYTHON_MATLAB_SOCKETS_TYPES_H

/* Include files */
#include "rtwtypes.h"

/* Custom Header Code */
#include "MW_raspi_init.h"
#include "MW_Pyserver_control.h"

/* Type Definitions */
#ifndef struct_emxArray_uint8_T
#define struct_emxArray_uint8_T

struct emxArray_uint8_T
{
  unsigned char *data;
  int *size;
  int allocatedSize;
  int numDimensions;
  bool canFreeData;
};

#endif                                 /*struct_emxArray_uint8_T*/

#ifndef typedef_emxArray_uint8_T
#define typedef_emxArray_uint8_T

typedef struct emxArray_uint8_T emxArray_uint8_T;

#endif                                 /*typedef_emxArray_uint8_T*/
#endif

/* End of code generation (python_matlab_sockets_types.h) */
