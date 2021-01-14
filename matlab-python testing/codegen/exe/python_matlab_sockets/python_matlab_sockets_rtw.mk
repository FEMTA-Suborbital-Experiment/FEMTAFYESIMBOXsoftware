###########################################################################
## Makefile generated for component 'python_matlab_sockets'. 
## 
## Makefile     : python_matlab_sockets_rtw.mk
## Generated on : Wed Dec 16 16:58:14 2020
## Final product: $(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing/python_matlab_sockets.elf
## Product type : executable
## 
###########################################################################

###########################################################################
## MACROS
###########################################################################

# Macro Descriptions:
# PRODUCT_NAME            Name of the system to build
# MAKEFILE                Name of this makefile

PRODUCT_NAME              = python_matlab_sockets
MAKEFILE                  = python_matlab_sockets_rtw.mk
MATLAB_ROOT               = $(MATLAB_WORKSPACE)/C/Program_Files/MATLAB/R2020b
MATLAB_BIN                = $(MATLAB_WORKSPACE)/C/Program_Files/MATLAB/R2020b/bin
MATLAB_ARCH_BIN           = $(MATLAB_BIN)/win64
START_DIR                 = $(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing/codegen/exe/python_matlab_sockets
TGT_FCN_LIB               = ISO_C
SOLVER_OBJ                = 
CLASSIC_INTERFACE         = 0
MODEL_HAS_DYNAMICALLY_LOADED_SFCNS = 
RELATIVE_PATH_TO_ANCHOR   = .
C_STANDARD_OPTS           = 
CPP_STANDARD_OPTS         = 

###########################################################################
## TOOLCHAIN SPECIFICATIONS
###########################################################################

# Toolchain Name:          GNU GCC Raspberry Pi
# Supported Version(s):    
# ToolchainInfo Version:   2020b
# Specification Revision:  1.0
# 

#-----------
# MACROS
#-----------

CCOUTPUTFLAG = --output_file=
LDOUTPUTFLAG = --output_file=

TOOLCHAIN_SRCS = 
TOOLCHAIN_INCS = 
TOOLCHAIN_LIBS = -lm -lm -lstdc++

#------------------------
# BUILD TOOL COMMANDS
#------------------------

# Assembler: GNU GCC Raspberry Pi Assembler
AS = as

# C Compiler: GNU GCC Raspberry Pi C Compiler
CC = gcc

# Linker: GNU GCC Raspberry Pi Linker
LD = gcc

# C++ Compiler: GNU GCC Raspberry Pi C++ Compiler
CPP = g++

# C++ Linker: GNU GCC Raspberry Pi C++ Linker
CPP_LD = g++

# Archiver: GNU GCC Raspberry Pi Archiver
AR = ar

# MEX Tool: MEX Tool
MEX_PATH = $(MATLAB_ARCH_BIN)
MEX = "$(MEX_PATH)/mex"

# Download: Download
DOWNLOAD =

# Execute: Execute
EXECUTE = $(PRODUCT)

# Builder: Make Tool
MAKE = make


#-------------------------
# Directives/Utilities
#-------------------------

ASDEBUG             = -g
AS_OUTPUT_FLAG      = -o
CDEBUG              = -g
C_OUTPUT_FLAG       = -o
LDDEBUG             = -g
OUTPUT_FLAG         = -o
CPPDEBUG            = -g
CPP_OUTPUT_FLAG     = -o
CPPLDDEBUG          = -g
OUTPUT_FLAG         = -o
ARDEBUG             =
STATICLIB_OUTPUT_FLAG =
MEX_DEBUG           = -g
RM                  =
ECHO                = echo
MV                  =
RUN                 =

#--------------------------------------
# "Faster Runs" Build Configuration
#--------------------------------------

ARFLAGS              = -r
ASFLAGS              = -c \
                       $(ASFLAGS_ADDITIONAL) \
                       $(INCLUDES)
CFLAGS               = -c \
                       -MMD -MP -MF"$(@:%.o=%.dep)" -MT"$@"  \
                       -O2
CPPFLAGS             = -c \
                       -MMD -MP -MF"$(@:%.o=%.dep)" -MT"$@"  \
                       -fpermissive  \
                       -O2
CPP_LDFLAGS          = -lrt -lpthread -ldl
CPP_SHAREDLIB_LDFLAGS  = -shared  \
                         -lrt -lpthread -ldl
DOWNLOAD_FLAGS       =
EXECUTE_FLAGS        =
LDFLAGS              = -lrt -lpthread -ldl
MEX_CPPFLAGS         =
MEX_CPPLDFLAGS       =
MEX_CFLAGS           =
MEX_LDFLAGS          =
MAKE_FLAGS           = -f $(MAKEFILE)
SHAREDLIB_LDFLAGS    = -shared  \
                       -lrt -lpthread -ldl



###########################################################################
## OUTPUT INFO
###########################################################################

PRODUCT = $(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing/python_matlab_sockets.elf
PRODUCT_TYPE = "executable"
BUILD_TYPE = "Executable"

###########################################################################
## INCLUDE PATHS
###########################################################################

INCLUDES_BUILDINFO = -I$(START_DIR) -I$(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing -I$(MATLAB_ROOT)/toolbox/eml/externalDependency/timefun -I$(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/include -I$(START_DIR)/examples -I$(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/server -I$(MATLAB_ROOT)/toolbox/coder/rtiostream/src/utils -I$(MATLAB_ROOT)/extern/include

INCLUDES = $(INCLUDES_BUILDINFO)

###########################################################################
## DEFINES
###########################################################################

DEFINES_ = -D_POSIX_C_SOURCE=199309L -D__MW_TARGET_USE_HARDWARE_RESOURCES_H__ -DMW_MATLABTARGET
DEFINES_CUSTOM = 
DEFINES_SKIPFORSIL = -D__linux__ -DARM_PROJECT -D_USE_TARGET_UDP_ -D_RUNONTARGETHARDWARE_BUILD_ -DSTACK_SIZE=200000
DEFINES_STANDARD = -DMODEL=python_matlab_sockets

DEFINES = $(DEFINES_) $(DEFINES_CUSTOM) $(DEFINES_SKIPFORSIL) $(DEFINES_STANDARD)

###########################################################################
## SOURCE FILES
###########################################################################

SRCS = $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/MW_TCPSendReceive.c $(START_DIR)/python_matlab_sockets_main_terminate.c $(START_DIR)/python_matlab_sockets_data.c $(START_DIR)/rt_nonfinite.c $(START_DIR)/rtGetNaN.c $(START_DIR)/rtGetInf.c $(START_DIR)/python_matlab_sockets_initialize.c $(START_DIR)/python_matlab_sockets_terminate.c $(START_DIR)/python_matlab_sockets.c $(START_DIR)/examples/main.c $(START_DIR)/python_matlab_sockets_emxutil.c $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/server/MW_raspi_init.c $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/MW_Pyserver_control.c

ALL_SRCS = $(SRCS)

###########################################################################
## OBJECTS
###########################################################################

OBJS = MW_TCPSendReceive.c.o python_matlab_sockets_main_terminate.c.o python_matlab_sockets_data.c.o rt_nonfinite.c.o rtGetNaN.c.o rtGetInf.c.o python_matlab_sockets_initialize.c.o python_matlab_sockets_terminate.c.o python_matlab_sockets.c.o main.c.o python_matlab_sockets_emxutil.c.o MW_raspi_init.c.o MW_Pyserver_control.c.o

ALL_OBJS = $(OBJS)

###########################################################################
## PREBUILT OBJECT FILES
###########################################################################

PREBUILT_OBJS = 

###########################################################################
## LIBRARIES
###########################################################################

LIBS = 

###########################################################################
## SYSTEM LIBRARIES
###########################################################################

SYSTEM_LIBS = 

###########################################################################
## ADDITIONAL TOOLCHAIN FLAGS
###########################################################################

#---------------
# C Compiler
#---------------

CFLAGS_BASIC = $(DEFINES) $(INCLUDES)

CFLAGS += $(CFLAGS_BASIC)

#-----------------
# C++ Compiler
#-----------------

CPPFLAGS_BASIC = $(DEFINES) $(INCLUDES)

CPPFLAGS += $(CPPFLAGS_BASIC)

###########################################################################
## INLINED COMMANDS
###########################################################################


DERIVED_SRCS = $(subst .o,.dep,$(OBJS))

build:

%.dep:



-include codertarget_assembly_flags.mk
-include *.dep


###########################################################################
## PHONY TARGETS
###########################################################################

.PHONY : all build buildobj clean info prebuild download execute


all : build
	echo "### Successfully generated all binary outputs."


build : prebuild $(PRODUCT)


buildobj : prebuild $(OBJS) $(PREBUILT_OBJS)
	echo "### Successfully generated all binary outputs."


prebuild : 


download : $(PRODUCT)


execute : download
	echo "### Invoking postbuild tool "Execute" ..."
	$(EXECUTE) $(EXECUTE_FLAGS)
	echo "### Done invoking postbuild tool."


###########################################################################
## FINAL TARGET
###########################################################################

#-------------------------------------------
# Create a standalone executable            
#-------------------------------------------

$(PRODUCT) : $(OBJS) $(PREBUILT_OBJS)
	echo "### Creating standalone executable "$(PRODUCT)" ..."
	$(LD) $(LDFLAGS) -o $(PRODUCT) $(OBJS) $(SYSTEM_LIBS) $(TOOLCHAIN_LIBS)
	echo "### Created: $(PRODUCT)"


###########################################################################
## INTERMEDIATE TARGETS
###########################################################################

#---------------------
# SOURCE-TO-OBJECT
#---------------------

%.c.o : %.c
	$(CC) $(CFLAGS) -o "$@" "$<"


%.s.o : %.s
	$(AS) $(ASFLAGS) -o "$@" "$<"


%.cpp.o : %.cpp
	$(CPP) $(CPPFLAGS) -o "$@" "$<"


%.c.o : $(RELATIVE_PATH_TO_ANCHOR)/%.c
	$(CC) $(CFLAGS) -o "$@" "$<"


%.s.o : $(RELATIVE_PATH_TO_ANCHOR)/%.s
	$(AS) $(ASFLAGS) -o "$@" "$<"


%.cpp.o : $(RELATIVE_PATH_TO_ANCHOR)/%.cpp
	$(CPP) $(CPPFLAGS) -o "$@" "$<"


%.c.o : $(START_DIR)/%.c
	$(CC) $(CFLAGS) -o "$@" "$<"


%.s.o : $(START_DIR)/%.s
	$(AS) $(ASFLAGS) -o "$@" "$<"


%.cpp.o : $(START_DIR)/%.cpp
	$(CPP) $(CPPFLAGS) -o "$@" "$<"


%.c.o : $(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing/%.c
	$(CC) $(CFLAGS) -o "$@" "$<"


%.s.o : $(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing/%.s
	$(AS) $(ASFLAGS) -o "$@" "$<"


%.cpp.o : $(MATLAB_WORKSPACE)/C/Users/evanr/Documents/GitHub/FEMTAFYESIMBOXsoftware/matlab-python_testing/%.cpp
	$(CPP) $(CPPFLAGS) -o "$@" "$<"


%.c.o : $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/%.c
	$(CC) $(CFLAGS) -o "$@" "$<"


%.s.o : $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/%.s
	$(AS) $(ASFLAGS) -o "$@" "$<"


%.cpp.o : $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/%.cpp
	$(CPP) $(CPPFLAGS) -o "$@" "$<"


%.c.o : $(START_DIR)/examples/%.c
	$(CC) $(CFLAGS) -o "$@" "$<"


%.s.o : $(START_DIR)/examples/%.s
	$(AS) $(ASFLAGS) -o "$@" "$<"


%.cpp.o : $(START_DIR)/examples/%.cpp
	$(CPP) $(CPPFLAGS) -o "$@" "$<"


MW_TCPSendReceive.c.o : $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/MW_TCPSendReceive.c
	$(CC) $(CFLAGS) -o "$@" "$<"


python_matlab_sockets_main_terminate.c.o : $(START_DIR)/python_matlab_sockets_main_terminate.c
	$(CC) $(CFLAGS) -o "$@" "$<"


python_matlab_sockets_data.c.o : $(START_DIR)/python_matlab_sockets_data.c
	$(CC) $(CFLAGS) -o "$@" "$<"


rt_nonfinite.c.o : $(START_DIR)/rt_nonfinite.c
	$(CC) $(CFLAGS) -o "$@" "$<"


rtGetNaN.c.o : $(START_DIR)/rtGetNaN.c
	$(CC) $(CFLAGS) -o "$@" "$<"


rtGetInf.c.o : $(START_DIR)/rtGetInf.c
	$(CC) $(CFLAGS) -o "$@" "$<"


python_matlab_sockets_initialize.c.o : $(START_DIR)/python_matlab_sockets_initialize.c
	$(CC) $(CFLAGS) -o "$@" "$<"


python_matlab_sockets_terminate.c.o : $(START_DIR)/python_matlab_sockets_terminate.c
	$(CC) $(CFLAGS) -o "$@" "$<"


python_matlab_sockets.c.o : $(START_DIR)/python_matlab_sockets.c
	$(CC) $(CFLAGS) -o "$@" "$<"


main.c.o : $(START_DIR)/examples/main.c
	$(CC) $(CFLAGS) -o "$@" "$<"


python_matlab_sockets_emxutil.c.o : $(START_DIR)/python_matlab_sockets_emxutil.c
	$(CC) $(CFLAGS) -o "$@" "$<"


MW_raspi_init.c.o : $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/server/MW_raspi_init.c
	$(CC) $(CFLAGS) -o "$@" "$<"


MW_Pyserver_control.c.o : $(MATLAB_WORKSPACE)/C/ProgramData/MATLAB/SupportPackages/R2020b/toolbox/realtime/targets/raspi/src/periphs/MW_Pyserver_control.c
	$(CC) $(CFLAGS) -o "$@" "$<"


###########################################################################
## DEPENDENCIES
###########################################################################

$(ALL_OBJS) : rtw_proj.tmw $(MAKEFILE)


###########################################################################
## MISCELLANEOUS TARGETS
###########################################################################

info : 
	echo "### PRODUCT = $(PRODUCT)"
	echo "### PRODUCT_TYPE = $(PRODUCT_TYPE)"
	echo "### BUILD_TYPE = $(BUILD_TYPE)"
	echo "### INCLUDES = $(INCLUDES)"
	echo "### DEFINES = $(DEFINES)"
	echo "### ALL_SRCS = $(ALL_SRCS)"
	echo "### ALL_OBJS = $(ALL_OBJS)"
	echo "### LIBS = $(LIBS)"
	echo "### MODELREF_LIBS = $(MODELREF_LIBS)"
	echo "### SYSTEM_LIBS = $(SYSTEM_LIBS)"
	echo "### TOOLCHAIN_LIBS = $(TOOLCHAIN_LIBS)"
	echo "### ASFLAGS = $(ASFLAGS)"
	echo "### CFLAGS = $(CFLAGS)"
	echo "### LDFLAGS = $(LDFLAGS)"
	echo "### SHAREDLIB_LDFLAGS = $(SHAREDLIB_LDFLAGS)"
	echo "### CPPFLAGS = $(CPPFLAGS)"
	echo "### CPP_LDFLAGS = $(CPP_LDFLAGS)"
	echo "### CPP_SHAREDLIB_LDFLAGS = $(CPP_SHAREDLIB_LDFLAGS)"
	echo "### ARFLAGS = $(ARFLAGS)"
	echo "### MEX_CFLAGS = $(MEX_CFLAGS)"
	echo "### MEX_CPPFLAGS = $(MEX_CPPFLAGS)"
	echo "### MEX_LDFLAGS = $(MEX_LDFLAGS)"
	echo "### MEX_CPPLDFLAGS = $(MEX_CPPLDFLAGS)"
	echo "### DOWNLOAD_FLAGS = $(DOWNLOAD_FLAGS)"
	echo "### EXECUTE_FLAGS = $(EXECUTE_FLAGS)"
	echo "### MAKE_FLAGS = $(MAKE_FLAGS)"


clean : 
	$(ECHO) "### Deleting all derived files..."
	$(RM) $(PRODUCT)
	$(RM) $(ALL_OBJS)
	$(RM) *.c.dep
	$(RM) *.cpp.dep
	$(ECHO) "### Deleted all derived files."


