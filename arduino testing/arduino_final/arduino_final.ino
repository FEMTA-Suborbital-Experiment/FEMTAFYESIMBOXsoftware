/* 
 * This program runs the interface between the Pi and the flight computer, transmitting
 * digital sensor data. With each transmission over serial, the Pi will send 29 bytes of
 * data:
 * - 9 for each flow sensor (big-endian): 2 bytes for flow; a CRC; 2 bytes for temp; 
 *                                        a CRC; 2 bytes for flags; and a CRC.
 * - 10 for the UV sensor (little-endian): 2 bytes each for UVA, UVB, UVC1, UVC2, and UVD.
 * - 1 for the error state.
 * 
 * The flight computer will poll this Arduino differently for each sensor.
 * -- FLOW SENSOR --
 * The flight computer will "activate" each flow sensor by writing 0x3608.
 * Once activated, the flight computer will simply poll each sensor in the 
 * traditional I2C way. As a response, the Arduino will reply with all nine
 * bytes corresponding to the sensor polled.
 * 
 * -- UV SENSOR --
 * The flight computer will "poll" each of the five channels of the UV sensor independently.
 * It will do this by writing one byte, corresponding to the channel, then by polling the 
 * sensor (in the traditional way).
 */

#include "TwoWireSimulator.h"
#define BAUDRATE 115200

TwoWireSimulator WireSim;

byte data_buffer[28];
int db_index = 0;
int error_state = 0;

int flow1_active = 0;
int flow2_active = 0;
int uv_to_write;

void serialHandler(void);

void setup(void){
  Serial.begin(BAUDRATE);
  WireSim.begin(0x8, 0x19); //Starting address and mask corresponding to error state 0
  WireSim.onRequest(requestEvent);
  WireSim.onReceive(receiveEvent);
}

void loop(void){
  serialHandler();
}

void serialHandler(void){
  if (Serial.available()){ //  Nonzero number of bytes in serial buffer
    if (index == 29){ //If reading error state byte, update address and mask
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
        WireSim.updateAddresses(0x8,0x19);
        error_state = 0;
        break;
      case 1:
        WireSim.updateAddresses(0x8,0x1);
        error_state = 1;
        break;
      case 2:
        WireSim.updateAddresses(0x8,0x18);
        error_state = 2;
        break;
      case 3:
        WireSim.updateAddresses(0x8,0x1);
        error_state = 3;
        break;
      case 5:
        WireSim.updateAddresses(0x9,0x0);
        error_state = 5;
        break;
      case 6:
        WireSim.updateAddresses(0x10,0x0);
        error_state = 6;
        break;
      case 7:
        WireSim.updateAddresses(0xA,0x0);
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
      if (flow1_active)
        WireSim.write(data_buffer[0], 9);
      break;

    case (0x9): //Flow Sensor #2
      if (flow2_active)
        WireSim.write(data_buffer[9], 9);
      break;

    case (0x10): //UV Sensor
      WireSim.write(data_buffer[18 + uv_to_write], 2);
      break;

    default:
      WireSim.write(-1); //Send the flight computer an error if an invalid address is polled
      break;
  }
}

void receiveEvent(int howMany) {
  int b;
  switch (WireSim.lastAddress()){
    case (0x8): //Flow Sensor #1
      b = Wire.read();
      b <<= 8;
      b &= Wire.read();
      if (b == 0x3608)
        flow1_active = 1;
      break;

    case (0x9): //Flow Sensor #2
      b = Wire.read();
      b <<= 8;
      b &= Wire.read();
      if (b == 0x3608)
        flow2_active = 1;
      break;

    case (0x10): //UV Sensor
      switch (Wire.read()){
        case (0x7): //UVA
          uv_to_write = 0;
          break;

        case (0x9): //UVB
          uv_to_write = 1;
          break;

        case (0xA): //UVC1
          uv_to_write = 2;
          break;

        case (0xB): //UVC2
          uv_to_write = 3;
          break;

        case (0x8): //UVD
          uv_to_write = 4;
          break;

        default:
          break;
      }
      break;

    default:
      break;
  }
}
