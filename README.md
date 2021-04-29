# FYESIMBOXsoftware
FYE SIMBOX Software for Pi and Arduino

## Directories:

### simbox
Main package. Run with "python3.8 -m simbox" (make sure the virtual environment is activated; on the current Pi this is aliased to just `activate`.)

If you need to set up a new Pi for the simbox, installing dependencies in the virtual environment can be a pain, especially because the simbox program needs Python >= 3.8, and the default install with Raspbian is 3.7 (you'll probably need to compile from source). Also, Numba has a LLVM dependency that was tricky. If you need to do this, feel free to reach out to some of us for guidance, and depending on when you are reading this, I (Evan Rittner) might still have a .img of the properly set-up Pi.

### experiment_logs
Holds log files from each experiment (NOTE: git doesn't transfer empty directories, so you might want to make this if it's not already on the Pi).

### Production
Files to be used in actual simbox operation (but not on the Pi). In theory, all you need to do to run the main simbox program is to be on the same wifi network as the (powered-on) Pi, and run `run.bat`. If you do it like that, make sure there's a config file that corresponds to your experiment in the same directory as `run.bat`. See `example_config.txt` for how to write a config file for an experiment.

## Arduino I2C Simulator
The Arduino project in the [arduino testing/twi_slave_emulator](arduino%20testing/twi_slave_emulator/) folder performs the I2C sensor simulation by receiving commands over the serial port. Each of the files are described here in brief:
* [twi_slave_emulator/twi_slave_emulator.ino](arduino%20testing/twi_slave_emulator/twi_slave_emulator.ino)
> This is the main project file that runs whenever the Arduino is reset. It contains all of the parameters regarding the device addresses, command codes, startup code, event loop, and two-wire interrupt code.
* [twi_slave_emulator/twi_slave_emulator.h](arduino%20testing/twi_slave_emulator/twi_slave_emulator.h)
> This contains the wrapper class for the Wire library that manages the address and mask registers depending on a inital list of addresses and a list controlling which ones are enabled. This also acts as an intermediary between the default interrupt functions and new custom ones that have code to determine which address triggered the interrupt and whether that address was in an enabled or shaddowed state.
* [twi_slave_emulator/circular_buffer.h](arduino%20testing/twi_slave_emulator/circular_buffer.h)
> A circular buffer that assists in doing the serial command processing by being a little more flexible than the default serial buffer. The event loop in the main code immediately transfers bytes from the serial buffer into a circular buffer, and the command receive event occurs once enough bytes have been buffered.
* [twi_slave_emulator/src/Wire/](arduino%20testing/twi_slave_emulator/src/Wire/)
> This contains a modified version of the Wire library's source code. Modifications needed to be made so the address in the `TWDR` register was not lost when receiving multiple bytes of data. [/src/Wire/Wire.cpp](arduino%20testing/twi_slave_emulator/src/Wire/Wire.cpp) and [/src/Wire/Wire.h](arduino%20testing/twi_slave_emulator/src/Wire/Wire.h) wrap [/src/Wire/utility/twi.c](arduino%20testing/twi_slave_emulator/src/Wire/utility/twi.c) and [/src/Wire/utility/twi.h](arduino%20testing/twi_slave_emulator/src/Wire/utility/twi.h) with the modifictions to the data receive code to store the contents of the `TWDR` register and pass it up the function callback chain as needed so the [twi_slave_emulator.h](arduino%20testing/twi_slave_emulator/twi_slave_emulator.h) code can process it into an address type with an appropriate state.

### arduino testing: 
Scripts for Arduino for testing

### matlab-python testing
Scripts testing interface between Matlab and Python

### Pi testing
Scripts for Pi for testing

### library files
Copies of some Python library files, to read and understand (just for reference)

