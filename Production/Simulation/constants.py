# File holding physical constants for use by the virtual environment
# simulation functions. Write "import constants" or "from constants import *".
# All values here should be in base SI units (kg, m, K, mol, etc.) or
# derived units (J, W, etc.), but not scaled (like cm, g, or kJ).

"""
TODO: un-scale scaled constants (i.e. h_evap is defined using kJ). Maybe
don't do this, though, since the change might cause errors in other code. TBD.
Also, maybe we can just visually separate universal constants (N_a) from
experiment-specific constants, like V_CC, for clarity.
"""

from math import pi

m = 2.988e-26         # Mass of one water molecule [kg]       
kB = 1.380649e-23     # Boltzmann constant [J/K]      
rhol = 997            # Density of liquid water [kg/m^3]    
N_a = 6.02214e23      # Avogadros number [# of particles/mol]
MW = 0.0180153        # Molecular weight of water [kg/mol]
D = (1/8) / 39.37     # Pipe diameter [m]
A = pi * ((D / 2)**2) # Area of pipe cross section [m^2]
R = 8.314             # Universal gas constant of water [J/(mol*K)]
C_evap = 0.01         # Evaporation coefficient
C_cond = 0.01         # Condensation coefficient
V_CC = 38e-6          # Volume of collection chamber [m^3]
h_evap = 2500         # Heat of vaporazitaion of water [kJ/kg]
h_c = 4000            # Convective heat transfer coefficient of water [kW/(m^2*K)]

"etc, to be continued"
