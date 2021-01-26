/****************************************************************************************************
twi_slave_emulator

Written by Ethan Kessel (mailto:eqkessel@gmail.com)

This code has the purpose of emulating multiple I2C sensors using a single Arduino device. The
header file included handles the neccesary address masking to respond to multiple addresses as a
Two Wire Interface slave and also keeps track of whether an address was enabled intentionally or
not.

This code will be used in the testing of the FEMTA Subortbital Flight Experiment
(https://engineering.purdue.edu/CubeSat/missions/femta) in order to validate the flight computer's
ability to poll the I2C sensors used to monitor the experiment and it's ability to handle sensor
failures. As noted in the header file, not all addresses may be properly removed from the mask due to
address permutations, so certain failures are impossible to properly simulate due to the Arduino
automatically ACKnowleding the poll.

*****************************************************************************************************

MIT License

Copyright (c) 2020 Ethan Kessel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

*****************************************************************************************************/

#include "twi_slave_emulator.h"
#include "circular_buffer.h"

// Useful Macros
#define LEN(x) static_cast<size_t>(sizeof(x) / sizeof(x[0]))
#define GET_BIT(b, x) ((x >> b) & 1)

// Defined Constants
#define BAUDRATE 115200 //  Serial port baud rate
#define BUFFER_SIZE 64  //  Number of elements to store in the buffer
#define NUM_DEV 3       //  Number of devices we are emulating
#define MSG_SIZE 27     //  Number of bytes in a command message: 1 byte for states, 2x 9 bytes for flow sensors, 8 bytes for UV sensor

// Global Declarations
enum Addresses : uint8_t  // Enumerated device addresses
{
  DEV_1 = 0x08, // Flow sensor #1
  DEV_2 = 0x09, // Flow sensor #2
  DEV_3 = 0x10  // UV sensor
};

CircularBuffer<char, BUFFER_SIZE> serial_buffer;        // Serial buffer, used to help process command messages

const uint8_t addr_list[] = {DEV_1, DEV_2, DEV_3};      // List of addresses of devices used to construct TWI Slave Emulator
TWI_SlaveEmulator<NUM_DEV> devices(addr_list);          // TWI Slave Emulator using above addresses

bool device_states[NUM_DEV] = {true, true, true};       //  Enable states of the devices

uint8_t flow_sensor_data[2][9] = {0};   //  Data arrays for the output of the two flow sensors
//  See pp. 10-11: https://developer.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/4_Liquid_Flow_Meters/Liquid_Flow/Sensirion_Liquid_Flow_Sensor_SLF3S-1300F_Datasheet_EN_D1.pdf
uint8_t uv_sensor_data[8] = {0};        //  Data array for values returnable by UV sensor
//  See pp. 6-8: https://cdn.sparkfun.com/assets/3/c/3/2/f/veml6075.pdf

enum UV_CommandCodes : uint8_t  // Enumerated command codes for the UV sensor
{
  UV_CONF      = 0x00,  //  Configuration/settings register, used here as a placeholder
  UVA_Data     = 0x07,  //  Raw UVA sensor reading
  UVB_Data     = 0x09,  //  Raw UVB sensor reading
  UVCOMP1_Data = 0x0A,  //  Ultraviolet/broad-spectrum compensator sensor reading 1
  UVCOMP2_Data = 0x0B   //  Ultraviolet/broad-spectrum compensator sensor reading 2
};
uint8_t UV_command_code = UV_CONF;  // UV sensor command code

//  Function Declarations
void serialRXHandler(void);
void commandHandler(void);
void parseByteInvBoolArray(uint8_t, bool*, size_t);
void onDeviceRequest(address_t);
void onDeviceReceive(size_t, address_t);
void reportAddressCall(address_t);
void serialPrintHexByte(uint8_t);

// Main Functions
void setup(void)
{
  //  Start serial communication protocol
  Serial.begin(BAUDRATE);
  Serial.println("[!] Arduino TWI Emulator connected to serial port...");
  Serial.println(serial_buffer.eomSignal());

  devices.attachAddressRequest(onDeviceRequest);
  devices.attachAddressReceive(onDeviceReceive);

  devices.begin();
}

void loop(void)
{
  // put your main code here, to run repeatedly:
  serialRXHandler();
  commandHandler();
}
// End of Main Functions

// Function Definitions

//  serialRXHandler
//    in/out: none
//    Polls the serial port buffer to see if a character is available and loads it into
//    the custom serial buffer for EOM detection. Does not loop, so depends on an external
//    loop to capture the entire message.
void serialRXHandler(void)
{
  if (Serial.available()) //  Nonzero number of bytes in buffer
  {
    serial_buffer.write(Serial.read());
  }
}

//  commandHandler
//    in/out: none
//    Processes the serial command data in the buffer once enough data has come in. Enables
//    the correct TWI devices and places updated message data for each device into memory.
void commandHandler(void)
{  
  if (serial_buffer.available() >= MSG_SIZE)  //  Parse the command once the full thing has been recieved
  {
    size_t i; // Loop variables
    size_t j;
    
    //  Echo command back
    Serial.print("CMD RX: ");
    for (i = 0; i < serial_buffer.available(); ++i)
    {
      Serial.print(serial_buffer.peek(i));
    }

    //  Parse the first byte into device enabled states
    parseByteInvBoolArray(serial_buffer.read(), device_states, NUM_DEV);
    devices.enableAddresses(device_states);

    //  Fill in the data for the two flow sensors
    for (i = 0; i < LEN(flow_sensor_data); ++i)
    {
      for (j = 0; j < LEN(flow_sensor_data[i]); ++j)
      {
        flow_sensor_data[i][j] = serial_buffer.read();
      }
    }

    //  Fill in the data for the UV sensor
    for (i = 0; i < LEN(uv_sensor_data); ++i)
    {
      uv_sensor_data[i] = serial_buffer.read();
    }
    
    Serial.println(" processed!");
  }
}

//  parseByteInvBoolArray
//    in:
//      uint8_t data_byte   - byte to parse into boolean array
//      bool* p_array       - pointer to array to put boolean values in
//      size_t array_size   - size of array to fill
//    out: none
//    Parses a byte into an array of boolean values where each item corresponds to a bit in
//    the byte. This function inverts the values so 'true' corresponds to a 0, and 'false'
//    corresponds to a 1. i.e. 0b000 becomes {true, true, true}
void parseByteInvBoolArray(uint8_t data_byte, bool* p_array, size_t array_size)
{
  for(size_t i = 0; i < array_size; ++i)
  {
    p_array[i] = !static_cast<bool>(GET_BIT(i, data_byte));
  }
}

//  onDeviceRequest
//    in:
//      address_t address   - address struct containing address and state of polled address
//    out: none
//    Handles when data is requested from a specific address on the TWI bus.
void onDeviceRequest(address_t address)
{
  Serial.print("Data REQUESTED from ");
  reportAddressCall(address);

  if (address.state == addressState::ENABLED)
  {
    size_t flow_sensor_index = 1;
    switch(address.address)
    {
      // Flow Sensors
      case DEV_1:
        --flow_sensor_index;
      case DEV_2:
        Serial.print("Sending data from flow sensor #");
        Serial.println(flow_sensor_index);
        devices.write(flow_sensor_data[flow_sensor_index], LEN(flow_sensor_data[flow_sensor_index]));
        break;

      // UV Sensor
      case DEV_3:
        size_t uv_data_index;
        switch(UV_command_code)
        {
          case UVA_Data:
            Serial.println("Sending UVA data from UV sensor");
            uv_data_index = 0;            
            break;
          case UVB_Data:
            Serial.println("Sending UVB data from UV sensor");
            uv_data_index = 2;            
            break;
          case UVCOMP1_Data:
            Serial.println("Sending UV COMP1 data from UV sensor");
            uv_data_index = 4;            
            break;
          case UVCOMP2_Data:
            Serial.println("Sending UV COMP2 data from UV sensor");
            uv_data_index = 6;            
            break;
          default:
            Serial.println("Invalid command code for data, sending zeros");
            uv_data_index = LEN(uv_sensor_data);  //  Sentinel value
            break;
        }
        if (uv_data_index < LEN(uv_sensor_data))
        {
          devices.write(&uv_sensor_data[uv_data_index], 2);
        }
        else
        {
          devices.write("\0\0");  //  Write two null characters equiv to 0x00 0x00 for invalid command code
        }
        break;
      default:
        Serial.println("Unknown device polled\a");
        break;
    }
  }
  else if (address.state == addressState::SHADOW)
  {
    Serial.println("Address is in shadow, ignoring...");
  }
  else
  {
    Serial.println("Bad address state, ignoring...");
  }
  Serial.println();
}

//  onDeviceReceive
//    in:
//      size_t num_bytes    - number of bytes recieved. required by TWI Slave Emulator
//      address_t address   - address struct containing address and state of polled address
//    out: none
//    Handles when data is sent to a specific address on the TWI bus.
void onDeviceReceive(size_t num_bytes, address_t address)
{
  Serial.print("Data RECEIVED (");
  Serial.print(num_bytes);
  Serial.print(" bytes) to ");
  reportAddressCall(address);

  if (address.state == addressState::ENABLED)
  {
    size_t flow_sensor_index = 1;
    switch(address.address)
    {
      // Flow Sensors
      case DEV_1:
        --flow_sensor_index;
      case DEV_2:
        Serial.print("Flow sensor #");
        Serial.print(flow_sensor_index);
        Serial.println(" written to");
        break;

      // UV Sensor
      case DEV_3:
        UV_command_code = devices.read();
        Serial.print("UV sensor command code updated: ");
        serialPrintHexByte(UV_command_code);
        Serial.println();
        break;
      default:
        Serial.println("Unknown device polled\a");
        break;
    }
  }
  else if (address.state == addressState::SHADOW)
  {
    Serial.println("Address is in shadow, ignoring...");
  }
  else
  {
    Serial.println("Bad address state, ignoring...");
  }

  if (devices.available())
  {
    uint8_t read_val;
    Serial.print("  Remaining data in buffer:");
    do
    {
      read_val = devices.read();
      Serial.print(" ");
      serialPrintHexByte(read_val);
    } while (devices.available());
    Serial.println();
  }
}

//  reportAddressCall
//    in:
//      address_t address   - address struct containing address and state of polled address
//    out: none
//    Prints info about a called address to the serial port
void reportAddressCall(address_t address)
{
  Serial.print("ADDRESS ");
  serialPrintHexByte(address.address);
  Serial.print(" (state is ");
  switch(address.state)
  {
    case addressState::ENABLED:
      Serial.println("ENABLED)");
      break;
    case addressState::SHADOW:
      Serial.println("SHADOW)");
      break;
    case addressState::DISABLED:  //  This should never run, is here for redundancy and error checking
      Serial.println("DISABLED)");
      break;
    case addressState::ERR:       //  Error states here and below
      Serial.println("ERR)");
      break;
    default:
      Serial.println("unknown)");
      break;
  }
}

//  serialPrintHexByte
//    in:
//      uint8_t value       - single byte to print to the serial port
//    out: none
//    Prints a byte like 0x??, always including 2 digits
void serialPrintHexByte(uint8_t value)
{
  Serial.print("0x");
  if (value < 0x10)
  {
    Serial.print('0');  //  Add a leading zero if the value is a single digit in hex
  }
  Serial.print(value, HEX);
}
