/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_blinkLED_mex.c
 *
 * Code generation for function 'blinkLED'
 *
 */

/* Include files */
#include "_coder_blinkLED_mex.h"
#include "_coder_blinkLED_api.h"

/* Function Definitions */
void blinkLED_mexFunction(int32_T nlhs, int32_T nrhs)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  st.tls = emlrtRootTLSGlobal;

  /* Check for proper number of arguments. */
  if (nrhs != 0) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:WrongNumberOfInputs", 5, 12, 0, 4, 8,
                        "blinkLED");
  }

  if (nlhs > 0) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:TooManyOutputArguments", 3, 4, 8,
                        "blinkLED");
  }

  /* Call the function. */
  blinkLED_api();
}

void mexFunction(int32_T nlhs, mxArray *plhs[], int32_T nrhs, const mxArray
                 *prhs[])
{
  (void)plhs;
  (void)prhs;
  mexAtExit(&blinkLED_atexit);

  /* Module initialization. */
  blinkLED_initialize();

  /* Dispatch the entry-point. */
  blinkLED_mexFunction(nlhs, nrhs);

  /* Module termination. */
  blinkLED_terminate();
}

emlrtCTX mexFunctionCreateRootTLS(void)
{
  emlrtCreateRootTLS(&emlrtRootTLSGlobal, &emlrtContextGlobal, NULL, 1);
  return emlrtRootTLSGlobal;
}

/* End of code generation (_coder_blinkLED_mex.c) */
