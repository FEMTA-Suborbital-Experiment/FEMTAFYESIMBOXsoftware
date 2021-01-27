/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * blinkLED_terminate.c
 *
 * Code generation for function 'blinkLED_terminate'
 *
 */

/* Include files */
#include "blinkLED_terminate.h"
#include "blinkLED_data.h"

/* Function Definitions */
void blinkLED_terminate(void)
{
  /* user code (Terminate function Body) */
  {
    MW_killPyserver();
    mwRaspiTerminate();
  }

  isInitialized_blinkLED = false;
}

/* End of code generation (blinkLED_terminate.c) */
