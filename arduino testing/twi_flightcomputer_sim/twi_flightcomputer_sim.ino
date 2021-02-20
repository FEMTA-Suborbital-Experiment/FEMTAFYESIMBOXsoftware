
#include <Wire.h>

// Defined Constants
#define BAUDRATE 115200 //  Serial port baud rate
#define FLOW_BYTES  9   //  Number of bytes to get from each flow sensor
#define UV_BYTES    2   //  Number of bytes to get from UV sensor in each catagory

// Global Declarations
enum Devices : uint8_t  // Digital sensors the flight computer interacts with
{
  FLOW_0  = 0x08, // Flow sensor #1
  FLOW_1  = 0x09, // Flow sensor #2
  UV_SENS = 0x10  // UV sensor
};

enum UV_CommandCodes : uint8_t  // Command codes for requesting data from UV sensors
{
  UV_CONF   = 0x00, // Configuration/settings register. Unused.
  UVA_DATA  = 0x07, // Raw UVA sensor reading
  UVB_DATA  = 0x09, // Raw UVB sensor reading
  UVC1_DAT  = 0x0A, // Ultraviolet/broad-spectrum compensator sensor reading 1
  UVC2_DAT  = 0x0B  // Ultraviolet/broad-spectrum compensator sensor reading 2
};

// Function Declarations
void printWireBuffer(void);

void setup()
{
  // Start serial communication protocol
  Serial.begin(BAUDRATE);
  Serial.println("[!] Arduino FC Simulator connected to serial port...");

  Wire.begin(); // Join as master
}

void loop()
{
  // Request data from the flow sensors
  Serial.print("\nGetting data from Flow Sensor 0:");
  Wire.requestFrom(FLOW_0, FLOW_BYTES);
  printWireBuffer();
  Serial.println();
  delay(2000);

  Serial.print("Getting data from Flow Sensor 1:");
  Wire.requestFrom(FLOW_1, FLOW_BYTES);
  printWireBuffer();
  Serial.println();
  delay(2000);
  
  // Request data from the UV sensors
  Serial.print("Getting data from UV Sensor:    ");

  // UVA
//  Wire.beginTransmission(UV_SENS);
//  Wire.write(0x07); // Initiate a request for UVA data
//  Wire.endTransmission(false);  // Send, do not send a stop
//  Wire.requestFrom(UV_SENS, UV_BYTES);  // Get the requested data back
////  Wire.endTransmission();
//  printWireBuffer();
//  Serial.print(" :");
//  delay(1000);
  
  // UVB
  Wire.beginTransmission(UV_SENS);
  Wire.write(UVB_DATA); // Initiate a request for UVB data
  Wire.endTransmission(false);  // Send, do not send a stop
  Wire.requestFrom(UV_SENS, UV_BYTES);  // Get the requested data back
//  Wire.endTransmission();
  printWireBuffer();
  Serial.print(" :");
  delay(1000);
  
  // UV Comp 1
  Wire.beginTransmission(UV_SENS);
  Wire.write(UVC1_DAT); // Initiate a request for UV Comp 1
  Wire.endTransmission(false);  // Send, do not send a stop
  Wire.requestFrom(UV_SENS, UV_BYTES);  // Get the requested data back
//  Wire.endTransmission();
  printWireBuffer();
  Serial.print(" :");
  delay(1000);

  // UV Comp 2
  Wire.beginTransmission(UV_SENS);
  Wire.write(UVC2_DAT); // Initiate a request for UV Comp 2
  Wire.endTransmission(false);  // Send, do not send a stop
  Wire.requestFrom(UV_SENS, UV_BYTES);  // Get the requested data back
//  Wire.endTransmission();
  printWireBuffer();
  Serial.println();
  delay(1000);

  Wire.beginTransmission(UV_SENS);
  Wire.write(0x07); // Initiate a request for UVA data
  Wire.endTransmission(false);  // Send, do not send a stop
  Wire.requestFrom(UV_SENS, UV_BYTES);  // Get the requested data back
//  Wire.endTransmission();
  printWireBuffer();
  Serial.print(" :");
  delay(1000);

  Serial.println("Waiting...");
  delay(10000);
}

//  printWireBuffer
//    in/out: none
//    Dumps the Wire buffer in hex format like 0x??
void printWireBuffer(void)
{
  uint8_t read_byte;
  
  while (Wire.available())
  {
    read_byte = Wire.read();
    Serial.print(" 0x");
    if (read_byte < 0x10)
    {
      Serial.print("0");
    }
    Serial.print(read_byte, HEX);
  }
}
