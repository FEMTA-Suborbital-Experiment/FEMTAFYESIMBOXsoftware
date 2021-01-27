/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_python_matlab_sockets_mex.c
 *
 * Code generation for function 'python_matlab_sockets'
 *
 */

/* Include files */
#include "_coder_python_matlab_sockets_mex.h"
#include "_coder_python_matlab_sockets_api.h"

/* Function Definitions */
void mexFunction(int32_T nlhs, mxArray *plhs[], int32_T nrhs, const mxArray
                 *prhs[])
{
  (void)plhs;
  (void)prhs;
  mexAtExit(&python_matlab_sockets_atexit);

  /* Module initialization. */
  python_matlab_sockets_initialize();

  /* Dispatch the entry-point. */
  python_matlab_sockets_mexFunction(nlhs, nrhs);

  /* Module termination. */
  python_matlab_sockets_terminate();
}

emlrtCTX mexFunctionCreateRootTLS(void)
{
  emlrtCreateRootTLS(&emlrtRootTLSGlobal, &emlrtContextGlobal, NULL, 1);
  return emlrtRootTLSGlobal;
}

void python_matlab_sockets_mexFunction(int32_T nlhs, int32_T nrhs)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  st.tls = emlrtRootTLSGlobal;

  /* Check for proper number of arguments. */
  if (nrhs != 0) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:WrongNumberOfInputs", 5, 12, 0, 4,
                        21, "python_matlab_sockets");
  }

  if (nlhs > 0) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:TooManyOutputArguments", 3, 4, 21,
                        "python_matlab_sockets");
  }

  /* Call the function. */
  python_matlab_sockets_api();
}

/* End of code generation (_coder_python_matlab_sockets_mex.c) */
