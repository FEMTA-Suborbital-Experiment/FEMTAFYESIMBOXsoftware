/***************************************************************
 *  twi_slave_emulator
 **************************************************************/

#include "twi_slave_emulator.h"
#include "circular_buffer.h"

// Useful Macros
#define LEN(x) static_cast<size_t>(sizeof(x) / sizeof(x[0]))

#define BAUDRATE 115200 //  Serial port baud rate
#define BUFFER_SIZE 32  //  Number of elements to store in the buffer

enum Addresses : uint8_t
{
  DEV_1 = 0x08,
  DEV_2 = 0x09,
  DEV_3 = 0x10
};

CircularBuffer<char, BUFFER_SIZE> data_buffers[3] = {{'\n'}, {'\n'}};

uint8_t addr_list[] = {DEV_1, DEV_2, DEV_3};
TWI_SlaveEmulator<LEN(addr_list)> devices(addr_list);

//byte data_buffer[BUFFER_SIZE];  //  Data buffer
uint8_t index = 0;        //  Data index in buffer

void serialRXHandler(void);
void commandHandler(void);
void receiver(address_t);

void setup(void)
{
  //  Start serial communication protocol
  Serial.begin(BAUDRATE);
  Serial.println("\nConnected to serial port...");
  Serial.println(data_buffers[2].eomSignal());

  devices.attachAddressRequest(receiver);

  devices.begin();
}

void loop(void)
{
  // put your main code here, to run repeatedly:
  serialRXHandler();

  commandHandler();
}

void receiver(address_t address)
{
  Serial.print("I was called as 0x");
  Serial.print(address.address, HEX);
  switch(address.state)
  {
    case addressState::ENABLED:
      Serial.println(" which was an enabled address!");
      devices.write(address.address);
      break;
    case addressState::DISABLED:
      Serial.println(" which was a disabled address! Wait... What?");
      break;
    case addressState::SHADOW:
      Serial.println(" which was covered in the mask shadow! Oops!");
      devices.write(0xFF);
      break;
    case addressState::ERR:
      Serial.println(" which was an error??");
      break;
    default:
      Serial.println(" which was not in the list??");
      break;
  }
}

void serialRXHandler(void)
{
  if (Serial.available()) //  Nonzero number of bytes in buffer
  {
    data_buffers[0].write(Serial.read());
    
    Serial.print("  Loaded '");
    Serial.print(data_buffers[0].peek(data_buffers[0].numBuffered() - 1));
    Serial.print("'... there are now ");
    Serial.print(data_buffers[0].numBuffered());
    Serial.println(" buffered values.");
    Serial.print("    Buffer has this many values ready: ");
    Serial.println(data_buffers[0].available());
  }
}

void commandHandler(void)
{
  size_t states = LEN(addr_list);
  bool stateBuffer[states] = {0};
  
  if (data_buffers[0].available())
  {
    for (size_t i = 0; i < data_buffers[0].available(); ++i)
    {
      Serial.print(data_buffers[0].peek(i));
    }

    for (size_t i = 0; i < states; ++i)
    {
      stateBuffer[i] = (data_buffers[0].read() == 'y');
    }
    data_buffers[0].markRead(data_buffers[0].available());  //  Ignore all other data in the buffer

    Serial.println("\nI heard you, updating!");
    devices.enableAddresses(stateBuffer);
  }
}
  /*
  size_t states = LEN(addr_list);
  bool stateBuffer[states] = {0};
  size_t index = 0;
  size_t loop_protect = 5;
  bool ran = false;
  char readVal = (char)0;
  
  while (readVal != '\n' && loop_protect)
  {
//    Serial.print("Bytes available in buffer: ");
//    Serial.print(Serial.available());
    if (Serial.available())
    {
      readVal = Serial.read();
//    Serial.print(" -- The byte is ");
      Serial.print(readVal);

      if (index < states)
      {
        ran = true;
        stateBuffer[index] = (readVal == 'a');
        index++;
      }

      loop_protect--;
    }
  }

  if (ran)
  {
//    Serial.println(Serial.available());
    Serial.println("\n  I heard you, updating!");
    devices.enableAddresses(stateBuffer);
  }
  */
