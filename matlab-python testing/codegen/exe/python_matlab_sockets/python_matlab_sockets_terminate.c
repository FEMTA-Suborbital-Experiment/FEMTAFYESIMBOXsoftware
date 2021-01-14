/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * python_matlab_sockets_terminate.c
 *
 * Code generation for function 'python_matlab_sockets_terminate'
 *
 */

/* Include files */
#include "python_matlab_sockets_terminate.h"
#include "python_matlab_sockets_data.h"
#include "rt_nonfinite.h"

/* Function Definitions */
void python_matlab_sockets_terminate(void)
{
  /* user code (Terminate function Body) */
  {
    MW_killPyserver();
    mwRaspiTerminate();
  }

  isInitialized_python_matlab_sockets = false;
}

/* End of code generation (python_matlab_sockets_terminate.c) */
