/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * blinkLED.c
 *
 * Code generation for function 'blinkLED'
 *
 */

/* Include files */
#include "blinkLED.h"
#include "blinkLED_data.h"
#include "blinkLED_emxutil.h"
#include "blinkLED_initialize.h"
#include "blinkLED_types.h"
#include "LED.h"
#include "MW_raspisystem.h"

/* Function Definitions */
void blinkLED(void)
{
  static const char cv3[15] = "sleep 0.5 2>&1";
  static const char cv1[5] = "none";
  emxArray_char_T *systemOut;
  int count;
  int i;
  char cv2[15];
  char cv[5];
  if (!isInitialized_blinkLED) {
    blinkLED_initialize();
  }

  /*  Create a Raspberry Pi object */
  /*  Blink the LED for 100 cycles */
  emxInit_char_T(&systemOut, 2);
  for (count = 0; count < 100; count++) {
    /*  Turn on the LED */
    for (i = 0; i < 5; i++) {
      cv[i] = cv1[i];
    }

    EXT_LED_setTrigger(0U, &cv[0]);
    EXT_LED_write(0U, 1);

    /*  Pause for 0.5 seconds */
    i = systemOut->size[0] * systemOut->size[1];
    systemOut->size[0] = 1;
    systemOut->size[1] = 16384;
    emxEnsureCapacity_char_T(systemOut, i);
    for (i = 0; i < 16384; i++) {
      systemOut->data[i] = '\x00';
    }

    for (i = 0; i < 15; i++) {
      cv2[i] = cv3[i];
    }

    MW_execSystemCmd(&cv2[0], 16384U, &systemOut->data[0]);

    /*  Turn off the LED */
    for (i = 0; i < 5; i++) {
      cv[i] = cv1[i];
    }

    EXT_LED_setTrigger(0U, &cv[0]);
    EXT_LED_write(0U, 0);

    /*  Pause for 0.5 seconds */
    i = systemOut->size[0] * systemOut->size[1];
    systemOut->size[0] = 1;
    systemOut->size[1] = 16384;
    emxEnsureCapacity_char_T(systemOut, i);
    for (i = 0; i < 16384; i++) {
      systemOut->data[i] = '\x00';
    }

    for (i = 0; i < 15; i++) {
      cv2[i] = cv3[i];
    }

    MW_execSystemCmd(&cv2[0], 16384U, &systemOut->data[0]);
  }

  emxFree_char_T(&systemOut);
}

/* End of code generation (blinkLED.c) */
