/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * python_matlab_sockets.c
 *
 * Code generation for function 'python_matlab_sockets'
 *
 */

/* Include files */
#include "python_matlab_sockets.h"
#include "python_matlab_sockets_data.h"
#include "python_matlab_sockets_emxutil.h"
#include "python_matlab_sockets_initialize.h"
#include "python_matlab_sockets_types.h"
#include "rt_nonfinite.h"
#include "MW_TCPSendReceive.h"
#include "coder_posix_time.h"
#include <math.h>
#include <stdio.h>

/* Type Definitions */
#ifndef typedef_c_raspi_internal_codegen_TCPRea
#define typedef_c_raspi_internal_codegen_TCPRea

typedef struct {
  int isInitialized;
  double Timeout;
  double ConnectTimeout;
  unsigned short isServer_;
  unsigned short connStream_;
  unsigned char isLittleEnd_;
  short errorNo_;
} c_raspi_internal_codegen_TCPRea;

#endif                                 /*typedef_c_raspi_internal_codegen_TCPRea*/

#ifndef typedef_tcpclient
#define typedef_tcpclient

typedef struct {
  bool matlabCodegenIsDeleted;
  c_raspi_internal_codegen_TCPRea TCPClientObj;
} tcpclient;

#endif                                 /*typedef_tcpclient*/

/* Function Declarations */
static double rt_roundd_snf(double u);

/* Function Definitions */
static double rt_roundd_snf(double u)
{
  double y;
  if (fabs(u) < 4.503599627370496E+15) {
    if (u >= 0.5) {
      y = floor(u + 0.5);
    } else if (u > -0.5) {
      y = u * 0.0;
    } else {
      y = ceil(u - 0.5);
    }
  } else {
    y = u;
  }

  return y;
}

void python_matlab_sockets(void)
{
  static const char b_ipaddr[10] = "127.0.0.1";
  emxArray_uint8_T *data;
  tcpclient t;
  tcpclient *obj;
  struct timespec b_timespec;
  double DataSize;
  int i;
  unsigned short connStream;
  short errorNo;
  char ipaddr[10];
  unsigned char dataIn[5];
  unsigned char isLittleEndian;
  signed char status;
  if (!isInitialized_python_matlab_sockets) {
    python_matlab_sockets_initialize();
  }

  t.matlabCodegenIsDeleted = true;
  t.TCPClientObj.Timeout = 0.0;
  t.TCPClientObj.ConnectTimeout = rtInf;
  t.TCPClientObj.isServer_ = 0U;
  t.TCPClientObj.isInitialized = 0;
  for (i = 0; i < 10; i++) {
    ipaddr[i] = b_ipaddr[i];
  }

  TCPStreamSetup(MAX_uint16_T, 0, &connStream, t.TCPClientObj.isServer_,
                 t.TCPClientObj.ConnectTimeout, &errorNo, &ipaddr[0]);
  t.TCPClientObj.connStream_ = connStream;
  t.TCPClientObj.errorNo_ = errorNo;
  littleEndianCheck(&isLittleEndian);
  t.TCPClientObj.isLittleEnd_ = isLittleEndian;
  t.matlabCodegenIsDeleted = false;
  for (i = 0; i < 5; i++) {
    dataIn[i] = (unsigned char)(i + 11U);
  }

  emxInit_uint8_T(&data, 1);
  TCPStreamStepSend(&dataIn[0], 5U, t.TCPClientObj.connStream_,
                    t.TCPClientObj.isServer_, &errorNo);
  t.TCPClientObj.errorNo_ = errorNo;
  b_timespec.tv_sec = (time_t)0.0;
  b_timespec.tv_nsec = (long)2.5E+8;
  nanosleep(&b_timespec, NULL);
  DataSize = getNumdataAvailable(t.TCPClientObj.connStream_);
  i = data->size[0];
  data->size[0] = (int)DataSize;
  emxEnsureCapacity_uint8_T(data, i);
  MWsetClientTimeout(t.TCPClientObj.connStream_, t.TCPClientObj.Timeout);
  DataSize = rt_roundd_snf(DataSize);
  if (DataSize < 65536.0) {
    if (DataSize >= 0.0) {
      connStream = (unsigned short)DataSize;
    } else {
      connStream = 0U;
    }
  } else if (DataSize >= 65536.0) {
    connStream = MAX_uint16_T;
  } else {
    connStream = 0U;
  }

  TCPStreamStepRecv(&data->data[0], &status, connStream,
                    t.TCPClientObj.connStream_, &errorNo,
                    t.TCPClientObj.isServer_);
  t.TCPClientObj.errorNo_ = errorNo;
  for (i = 0; i < 5; i++) {
    printf("Matlab received %d\n", (short)data->data[i]);
    fflush(stdout);
  }

  emxFree_uint8_T(&data);
  obj = &t;
  if (!t.matlabCodegenIsDeleted) {
    t.matlabCodegenIsDeleted = true;
    TCPStreamTeardown(obj->TCPClientObj.connStream_);
  }
}

/* End of code generation (python_matlab_sockets.c) */
