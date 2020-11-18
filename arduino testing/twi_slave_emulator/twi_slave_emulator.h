////////////////////////////////////////////////////////////////////////////////////
//  
//  twi_slave_emulator.h
//  
//  Written by Ethan Kessel (mailto:eqkessel@gmail.com).
//  
//  Enables safe, scalable, and trackable use of an Arduino to act as multiple slaves on the same
//  Two-Wire Interface bus utilizing the Wire.h library.
//  
//  This software is loosely based on a simpler TWI simulator written by github user alexisgaziello
//  https://github.com/alexisgaziello/TwoWireSimulator
//
////////////////////////////////////////////////////////////////////////////////////
//
//  MIT License
//  
//  Copyright (c) 2020 Ethan Kessel
//  
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//  
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//  
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
////////////////////////////////////////////////////////////////////////////////////

#ifndef TWI_SLAVE_EMULATOR_H  //  #include protection
#define TWI_SLAVE_EMULATOR_H

#include <Wire.h> //  Arduino library for twi interface

///////////////////////////////////////////////////////////////////////////////
//  TYPE AND CLASS DECLARATIONS ///////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

//  Enumerated type for internal address states
enum class addressState
{
  ENABLED,    //  Address is enabled intentionally
  DISABLED,   //  Address is disabled and ATmega TWI will not awake to this address
  SHADOW,     //  Address is unintentionally enabled by concequence of current mask
  ERR         //  Error or bad address
};

struct address_t    //  Data structure for containing addresses and states based on mask data
{
  uint8_t address;
  addressState state;
};

//  TWI Slave Emulator class declaration
template <size_t N>
class TWI_SlaveEmulator: public TwoWire
{
protected:  //  PROTECTED MEMBER VARIABLES / FUNCTIONS
  //size_t      _num_given_addresses;     // Count of the given addresses we are wanting to emulate
  bool        _began;               // Keep track of whether the TWI has been begun or not, so we can disable only if needed
  uint8_t     _given_addresses[N];  // Array of the given addresses we are wanting to emulate
  uint8_t     _same_bits;           // All of the bits that are the same between all of the given addresses
  uint8_t     _diff_bits;           // All of the bits that are different between the given addresses
  uint8_t     _addr_byte;           // Address byte for the TWI Address Register. Changes depending on if addresses are enabled or not
  uint8_t     _addr_mask;           // Address mask byte for the TWI Address Mask Register. Also changes with enabled addresses
  static uint8_t     _num_bits;            // Number of bits that change between addresses
  static uint8_t     _bit_positions[7];    // Array storing the bit positions of all of the bits that change between addresses (LSB = 0)
  static size_t     _num_addresses;       // Count of the total number of address permutations we could end up covering, i.e. 2^n
  static address_t  _addresses[128];      // Array of structures to keep track of address permuations w/ their state
  
  static void (*user_onAddressRequest)(address_t);  // Function pointer to user-defined request handler
  static void (*user_onAddressReceive)(size_t, address_t); // Function pointer to user-defined receiving handler
  
  static void requestHandler(void);  //  Internal functions to hook to TwoWire system
  static void receiveHandler(int nBytes);

  void setRegisters(void);
  void updatePermutations(const bool* enabled_array);
  static uint8_t indexOfAddress(uint8_t address);
  
public:   //  PUBLIC MEMBER VARIABLES / FUNCTIONS
  //  CONSTRUCTOR
  TWI_SlaveEmulator(const uint8_t* addresses);
  //  DESTRUCTOR
  ~TWI_SlaveEmulator(void);

  void begin(void);

  void attachAddressRequest(void (*function)(address_t));
  void attachAddressReceive(void (*function)(size_t, address_t));

  void enableAddresses(const bool* enabled_array);
  
  size_t getNumAddresses(void);
//  uint8_t getLastByte(void);
};

///////////////////////////////////////////////////////////////////////////////
//  STATIC INITIALIZATIONS of Template Members  ///////////////////////////////
///////////////////////////////////////////////////////////////////////////////

template <size_t N> uint8_t   TWI_SlaveEmulator<N>::_num_bits = 0;
template <size_t N> uint8_t   TWI_SlaveEmulator<N>::_bit_positions[7] = {0};
template <size_t N> size_t    TWI_SlaveEmulator<N>::_num_addresses = 0;
template <size_t N> address_t TWI_SlaveEmulator<N>::_addresses[128] = {0, addressState::ERR};
template <size_t N> void      (*TWI_SlaveEmulator<N>::user_onAddressRequest)(address_t) = NULL;
template <size_t N> void      (*TWI_SlaveEmulator<N>::user_onAddressReceive)(size_t, address_t) = NULL;

///////////////////////////////////////////////////////////////////////////////
// CLASS FUNCTION DEFINITIONS  ////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

//  CONSTRUCTOR
//  Usage:
//    TWI_SlaveEmulator<NUMBER_OF_ADDRESSES> emulator(ADDRESS_ARRAY);
//
//    Uses a template parameter N to determine the number of given addresses and
//    takes in an array of uint8_t addresses. These addresses are truncated to
//    seven (7) bits in accordance with how the TWI functions. Computes all of the
//    address permutations given the bits that change in the addresses and prepares
//    the software to handle enabling or disabling of the given addresses. By
//    default, all of the given addresses are enabled, and by concequence all of
//    the address permutations are active in the mask shadow.
//    
template <size_t N>
TWI_SlaveEmulator<N>::TWI_SlaveEmulator(const uint8_t* addresses)
  : _began(false)
{
  //  Copy the given list of addresses into our own private memory for future reference
  for (uint8_t i = 0; i < N; ++i)
  {
    _given_addresses[i] = addresses[i] & 0x7F;  //  Chop off the MSB, not used for TWI
  }
  
  //  Determine a default address/mask based on the given addresses. Use this to compute all permutations
  //  of the bits we need to mask to create our full address array.
  _same_bits = _given_addresses[0];   // Address is all of the bits common to all addresses
  _diff_bits = 0b00000000;            // Address mask is all of the bits that change
  for (uint8_t i = 1; i < N; ++i) //  Start at 2nd item since above already inits for first item
  {
    _same_bits &= _given_addresses[i];  //  Leaves only the common bits in the end
    _diff_bits |= _given_addresses[0] ^ _given_addresses[i];  //  Bitwise-or in all of the different bits
  }
  _addr_byte = _same_bits;
  _addr_mask = _diff_bits;

  //  Now count the number of bits set in the mask, i.e. the number of bits changed.
  //  The number of addresses we will end up responding to is equal to 2 ^ number of bits that change.
  _num_bits = 0;
  uint8_t temp_diff = _diff_bits;
  while (temp_diff) //  The temporary mask will be nonzero while there are still set bits
  {
    _num_bits += temp_diff & 0x01;  // Slice out the LSB and add to the counter
    temp_diff >>= 1;  //  Shift the mask byte to the next bit
  }
  //  Store an array of the changed bit positions
  temp_diff = _diff_bits;
  uint8_t index = 0;  //  Index in array of bit positions
  uint8_t pos = 0;    //  Bit position in the mask (LSB = 0)
  while (temp_diff)
  {
    if (temp_diff & 0x01) //  Position bit of mask is nonzero
    {
      _bit_positions[index] = pos;
      ++index;
    }
    temp_diff >>= 1;  //  Shift over the mask
    ++pos;            //  Move to the next position
  }

  //  Now we can determine all of the addresses we can respond to
  _num_addresses = 1 << _num_bits;  //  Each masked bit doubles the number of addresses covered, use a bit shift to perform this
  for (uint8_t i = 0; i < _num_addresses; ++i)
  {
    _addresses[i].address = _addr_byte; //  Set all of the common bits
    for (uint8_t j = 0; j < _num_bits; ++j)
    {
      _addresses[i].address |= ((i >> j) & 0x01) << _bit_positions[j];
      /**********************************************************************************************************
       *    Okay, this code *does* warrant some explanation. Basically, we want to associate a number from
       *   0 to 2^n-1 with some permuation of n bits (of which there will be a total of 2^n permutations).
       *   Let's say we need the permutations of the following bit positions: 0b000XX00X, so n = 3 and the
       *   number of permutations is 2^3 = 8. We can associate some value from 0 to 7 (8-1) with one of the
       *   permutations, and in fact the state of the 3 least-significant bits in that value can correspond
       *   with the states of each of the bits we are permuting. I.E. 5 - 0b101 becomes 0b00010001 by taking
       *   the bits of 5 and associating them with the positions in our permutation byte. This conveniently
       *   gives us a way to programatically find the index of an address permutation simply by slicing out
       *   the permuted bits of the address and turning them into a number!
       *   
       *   In order to do this, we first need to loop through all values from 0 to n^2-1 (the number of
       *   permutations of addresses). This will be the index of the address we are working on as well as the
       *   value who's bits we'll use to determine the bits of the current permutation. We then loop through
       *   each of the different bit positions that change between all the permutaions (n) so we can set that
       *   number of bits. Then, we shift the value a number of bits to the right such that the current location
       *   falls into the least-significant bit position before chopping off all of the larger bits with a
       *   bitwise and with 1. This leaves a single value either 0 or 1 depending on if the value had a bit set
       *   or not in the position we were considering. We then shift this left into the correct position in the
       *   permutation, and bitwise or it into the address permutation to insert that bit.
      **********************************************************************************************************/  
    }
    _addresses[i].state = addressState::SHADOW; //  By default the address is enabled by as a SHADOW. Fix this for the actual address in a bit.
  }

  //  Fix the states of the given addresses to the correct ENABLED state
  for (uint8_t i = 0; i < N; ++i)
  {
    _addresses[indexOfAddress(_given_addresses[i])].state = addressState::ENABLED;
  }

  //  Link the internal handler functions
  TwoWire::onRequest( requestHandler );
  TwoWire::onReceive( receiveHandler );
}

//  DESTRUCTOR
template <size_t N>
TWI_SlaveEmulator<N>::~TWI_SlaveEmulator(void)
{
  if (_began)
  {
    TwoWire::end();
  }
}

//////////////////////////
//  PROTECTED FUNCTIONS //
//////////////////////////

//  requestHandler()
//  Performs internal handling of a TWI bus request at an address we are listening to when called
//  by Wire.h. See attachAddressRequest() for more information on how this is used.
template <size_t N>
void TWI_SlaveEmulator<N>::requestHandler(void)
{
  address_t address;  // Default argument to user handler is a bad address
  address.address = 0xFF;
  address.state = addressState::ERR;
  
  if(user_onAddressRequest) // Only handle if function is given
  {
    uint8_t last_addr = TWDR >> 1;  //  Get the address that was called (sitting in the data register)
    uint8_t index = indexOfAddress(last_addr);
    if (index < _num_addresses)
    {
      address = _addresses[index];
    }

    user_onAddressRequest(address); //  Call the user's function
  }
}

//  receiveHandler()
//  Performs internal handling of a TWI bus recieve at an address we are listening to when called
//  by Wire.h. See attachAddressReceive() for more information on how this is used.
template <size_t N>
void TWI_SlaveEmulator<N>::receiveHandler(int nBytes)
{
  address_t address;  // Default argument to user handler is a bad address
  address.address = 0xFF;
  address.state = addressState::ERR;
  
  if(user_onAddressRequest) // Only handle if function is given
  {
    uint8_t last_addr = TWDR >> 1;  //  Get the address that was called (sitting in the data register)
    uint8_t index = indexOfAddress(last_addr);
    if (index < _num_addresses)
    {
      address = _addresses[index];
    }

    user_onAddressReceive(static_cast<size_t>(nBytes), address); //  Call the user's function
  }
}

//  setRegisters()
//  Internal function for updating the address and mask registers based on calculated info. Also will
//  enable or disable the TWI output if no addresses are enabled by using begin() and end(). This gets
//  called whenever the enabled state is update for any addresses and when begin() is called.
template <size_t N>
void TWI_SlaveEmulator<N>::setRegisters(void)
{
  if (_addr_byte != 0xFF) // Address of 0xFF has an internal meaning of "no addresses enabled" so only enable if we need to
  {
    if (!_began)
    {
      TwoWire::begin(); // Init the TWI w/out address. Sets the neccesary address registers for enabling the TWI module, ACKs, and interupt service
      _began = true;
    }
    TWAR  = _addr_byte << 1;  // Address register (LSB is occupied by R/W bit so shift is neccesary)
    TWAMR = _addr_mask << 1;  // Address mask register (also needs to be shifted to align
  }
  else if (_began)
  {
    TwoWire::end(); // Disable the response of the TWI module, ACKs, and interupts
    _began = false;
  }
}

//  updatePermutations(boolean array for enabled given addresses)
//  Determines which of the address permuations covered in the address/mask combination are active and
//  updates their internal states accordingly. This gets called whenever the address/mask combination
//  is updated.
template <size_t N>
void TWI_SlaveEmulator<N>::updatePermutations(const bool* enabled_array)
{
  uint8_t match;  // Keeps track of matched bits in the addresses
  // Check all of the tracked addresses to see if they will match the combo of address and mask
  for (uint8_t i = 0; i < _num_addresses; ++i)
  {
    // These two lines emulate the hardware check for the address. Use this to see if any of our tracked addresses match
    match = ~(_addresses[i].address ^ _addr_byte); // Find all bits that match
    match |= _addr_mask;  // Set any bits that are covered by the mask, regardless if they match
    if (match ^ static_cast<uint8_t>(-1)) //  If any bits are 0 then we did not match, so the address will be DISABLED
    {
      _addresses[i].state = addressState::DISABLED;
    }
    else
    {
      _addresses[i].state = addressState::SHADOW; // Default to SHADOW and fix addresses we want ID'd as ENABLED separately
    }
  }

  //  Fix the states of the given addresses to the correct ENABLED state if they are supposed to be enabled
  //  Given addresses that are active but not enabled maintain the SHADOW state.
  uint8_t index;
  for (uint8_t i = 0; i < N; ++i)
  {
    index = indexOfAddress(_given_addresses[i]);
    if (enabled_array[i])
    {
      _addresses[index].state = addressState::ENABLED;
    }
  }
}

//  indexOfAddress(address)
//  Returns the index of a given address in the list of address permutations. This has undefined behavior if
//  an address not in the permutation list is passed, and thus would produce bad indecies.
template <size_t N>
uint8_t TWI_SlaveEmulator<N>::indexOfAddress(uint8_t address)
{
  uint8_t index = 0;
  //address ^= _same_bits;  //  Remove all of the common bit positions
  for (uint8_t i = 0; i < _num_bits; ++i)
  {
    // Extract the bits in the designated positions and piece them into the index number
    index |= ((address >> _bit_positions[i]) & 0x01) << i;
  }

  return(index);
}

////////////////////////
//  PUBLIC FUNCTIONS  //
////////////////////////

//  begin()
//  Activates the TWI bus. This function should only be used once when first starting the
//  slave emulator. It does not need to be run at all if the addresses enabled states are
//  updated first, as that will automatically start the devices if neccesary.
template <size_t N>
void TWI_SlaveEmulator<N>::begin(void)
{
  setRegisters();
}

//  attachAddressRequest(user request handler function)
//  Attaches a given void function taking an address_t address struct to the TWI system.
//  When the Arduino acknowledges an address the master is requesting data from, the function 
//  given here is called, recieving as a parameter a struct with the address that was called
//  and the state it was in.
template <size_t N>
void TWI_SlaveEmulator<N>::attachAddressRequest(void (*function)(address_t))
{
  user_onAddressRequest = function;
}

//  attachAddressRecieve(user request handler function)
//  Attaches a given void function taking a size_t and an address_t address struct to the TWI system.
//  When the Arduino acknowledges an address the master sent data to, the function given here
//  is called, recieving as a parameter the number of bytes recieved and a struct with the address
//  that was called and the state it was in.
template <size_t N>
void TWI_SlaveEmulator<N>::attachAddressReceive(void (*function)(size_t, address_t))
{
  user_onAddressReceive = function;
}

//  enableAddresses(boolean array for given addresses)
//  Given an array of booleans corresponding to the given addresses on construction, recalculates
//  the address and mask bytes, updates the states of all of the address permutations accordingly,
//  and updates the registers to enable the functionality as specified.
template <size_t N>
void TWI_SlaveEmulator<N>::enableAddresses(const bool* enabled_array)
{
  //  Update the address and mask data
  _addr_byte = 0xFF;
  _addr_mask = 0;
  //  Count through the originally given addresses until we run out or we find one that we want enabled
  uint8_t index = 0;
  while (index < N && !enabled_array[index])
  {
    ++index;
  }

  //  Start with the first address we want enabled (if any) and compute the common/different bits
  for (uint8_t i = index; i < N; ++i)
  {
    if (enabled_array[i])
    {
      _addr_byte &= _given_addresses[i];
      _addr_mask |= _given_addresses[index] ^ _given_addresses[i];
    }
  }

  updatePermutations(enabled_array);  //  Recalculate what state each address is in
  setRegisters(); //  Set the TWI registers to enable the operation we want
}

//  getNumAddresses()
//  Returns the number of addresses covered by the mask when all addresses are enabled
template <size_t N>
size_t TWI_SlaveEmulator<N>::getNumAddresses(void)
{
  return(_num_addresses);
}

#endif //TWI_SLAVE_EMULATOR_H
