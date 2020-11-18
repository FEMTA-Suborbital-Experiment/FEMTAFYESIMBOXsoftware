/***************************************************************
 *  twi_slave_emulator
 **************************************************************/

#define BAUDRATE 115200 //  Serial port baud rate
#define BUFFER_SIZE 256 //  Number of bytes to store in the buffer
#include <string>
#include <math>

byte data_buffer[BUFFER_SIZE];  //  Data buffer //(byte ~= uint8_t)
uint8_t index = 0;        //  Data index in buffer

void serialHandler(void);

void setup(void){
  //  Start serial communication protocol
  Serial.begin(BAUDRATE);
  //Serial.println("\nConnected to serial port...");
}

void loop(void){
  serialHandler();
}

void serialHandler(void){
  if (Serial.available()){ //  Nonzero number of bytes in buffer
    data_buffer[index] = Serial.read();
    if (!(++index % 4)){  //  Index should overflow before exceeding array range
      //If we've read the 4 bytes that store a complete string (e.g. "2.34")
      //TODO: takemost recent 4 entries in the array (which hold the ascii values of each character)
      //(for example "2.34", the last 4 entries would be {50, 46, 51, 52}
      //We want to re-convert that to a float so that we can use it.
      //For this test, why don't we just floor it (to get back to a nice int) and send it back
    }
  }
}
