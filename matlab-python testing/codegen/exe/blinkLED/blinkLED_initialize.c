/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * blinkLED_initialize.c
 *
 * Code generation for function 'blinkLED_initialize'
 *
 */

/* Include files */
#include "blinkLED_initialize.h"
#include "blinkLED_data.h"

/* Function Definitions */
void blinkLED_initialize(void)
{
  /* user code (Initialize function Body) */
  {
    mwRaspiInit();
    MW_launchPyserver();
  }

  isInitialized_blinkLED = true;
}

/* End of code generation (blinkLED_initialize.c) */
