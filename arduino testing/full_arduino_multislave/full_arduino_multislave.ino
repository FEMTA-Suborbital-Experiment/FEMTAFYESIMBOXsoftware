/***************************************************************
 *  twi_slave_emulator
 **************************************************************/

#define BAUDRATE 115200 //  Serial port baud rate

byte data_buffer[3];  //  Data buffer
int index = 0;

void serialHandler(void);

void setup(void){
  //  Start serial communication protocol
  Serial.begin(BAUDRATE);
}

void loop(void){
  serialHandler();
}

void serialHandler(void){
  if (Serial.available()){ //  Nonzero number of bytes in buffer
    data_buffer[index] = Serial.read();
    if (index == 2){
      index = 0;
    }
    else {
      index++;
    }
  }
}
