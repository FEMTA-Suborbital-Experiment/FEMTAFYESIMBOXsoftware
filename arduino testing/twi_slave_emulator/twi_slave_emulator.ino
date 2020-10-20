/***************************************************************
 *  twi_slave_emulator
 **************************************************************/

#define BAUDRATE 115200 //  Serial port baud rate
#define BUFFER_SIZE 256 //  Number of bytes to store in the buffer

byte data_buffer[BUFFER_SIZE];  //  Data buffer
uint8_t index = 0;        //  Data index in buffer

void serialHandler(void);

void setup(void)
{
  //  Start serial communication protocol
  Serial.begin(BAUDRATE);
  Serial.println("\nConnected to serial port...");
}

void loop(void)
{
  // put your main code here, to run repeatedly:
  serialHandler();
}

void serialHandler(void)
{
  if (Serial.available()) //  Nonzero number of bytes in buffer
  {
    data_buffer[index] = Serial.read();
    
    Serial.print("  Loaded ");
    Serial.print(data_buffer[index], HEX);
    Serial.print(" into buffer at position ");
    Serial.println(index, DEC);
    
    ++index;  //  Should overflow before exceeding array range
  }
}
