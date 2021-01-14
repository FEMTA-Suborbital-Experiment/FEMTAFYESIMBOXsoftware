/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * python_matlab_sockets_initialize.c
 *
 * Code generation for function 'python_matlab_sockets_initialize'
 *
 */

/* Include files */
#include "python_matlab_sockets_initialize.h"
#include "python_matlab_sockets_data.h"
#include "rt_nonfinite.h"

/* Function Definitions */
void python_matlab_sockets_initialize(void)
{
  /* user code (Initialize function Body) */
  {
    mwRaspiInit();
    MW_launchPyserver();
  }

  isInitialized_python_matlab_sockets = true;
}

/* End of code generation (python_matlab_sockets_initialize.c) */
