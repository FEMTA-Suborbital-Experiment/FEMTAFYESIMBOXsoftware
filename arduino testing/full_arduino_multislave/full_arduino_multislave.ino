/***************************************************************
 *  twi_slave_emulator
 **************************************************************/

#include "TwoWireSimulator.h"
#define BAUDRATE 115200 //  Serial port baud rate

TwoWireSimulator Wiresim;

byte data_buffer[3];  //  Data buffer
int index = 0;
int error_state = 0;

void serialHandler(void);

void setup(void){
  Serial.begin(BAUDRATE);
  WireSim.begin(0x8, 0x19);
  WireSim.onRequest(requestEvent);
}

void loop(void){
  serialHandler();
}

void serialHandler(void){
  if (Serial.available()){ //  Nonzero number of bytes in buffer
    if (index == 3){
      updateMask(Serial.read());
      index = 0;
    }
    else {
      data_buffer[index] = Serial.read();
      index++;
    }
  }
}

void updateMask(int state){
  if (error_state != state){
    switch (state){
      case 0:
        Wiresim.updateAddresses(0x8,0x19);
        error_state = 0;
        break;
      case 1:
        Wiresim.updateAddresses(0x8,0x1);
        error_state = 1;
        break;
      case 2:
        Wiresim.updateAddresses(0x8,0x10);
        error_state = 2;
        break;
      case 3:
        Wiresim.updateAddresses(0x8,0x1);
        error_state = 3;
        break;
      case 5:
        Wiresim.updateAddresses(0x9,0x0);
        error_state = 5;
        break;
      case 6:
        Wiresim.updateAddresses(0x10,0x0);
        error_state = 6;
        break;
      case 7:
        Wiresim.updateAddresses(0xA,0x0);
        error_state = 7;
        break;
      default:
        break; //Note that error state 4 is invalid
    }
  }
}

void requestEvent(void){
  switch (WireSim.lastAddress()){
    case (0x8): //Flow Sensor #1
      WireSim.write(data_buffer[0]);
      break;

    case (0x9): //Flow Sensor #2
      WireSim.write(data_buffer[1]);
      break;

    case (0x10): //UV Sensor
      WireSim.write(data_buffer[2]);
      break;

    default:
      WireSim.write(-1);
      break;
  }
}
