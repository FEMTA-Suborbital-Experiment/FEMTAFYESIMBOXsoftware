# File holding physical constants for use by the virtual environment
# simulation functions. Use "import constants" or "from constants import *".

from math import pi

R = 8.3145 #[kJ/kmol-K]                 Universal Gas Constant
kB = 1.380649e-23 #[J/K]                Boltzmann constant
N_a = 6.02214e23 #[# of particles/mol]  Avogadros number

#Air Properties
gammaAir = 1.4 #[]             Ratio of specific heats for air
MW_Air = 29 #[kg/kmol]         Molecular Weight of Air
R_air = R / MW_Air #[kJ/kg-K]  Specific Gas Constant for Air
Cp_Air = 1.005 #[kJ/kg-K]      Specific Heat of Air
 
#Water Properties
rho_water = 997 #[kg/m^3]       Density of liquid water
m_H2O = 2.988e-26 #[kg]         Mass of one water molecule
MW_Water = 18.0135 #[kg/kmol]   Molecular weight of water
Cp_water_liquid = 4 #[kJ/kg-K]  Specific heat of liquid water
Cp_water_vapor = 2 #[kJ/kg-K]   Specific heat of water vapor
Ce_water = 1 #[]                Evaporation Coefficient of water
Cc_water = 0.75 #[]             Condensation Coefficient of water

#HFE Properties
MW_HFE = 250 #[kg/kmol]                Molecular Weight of HFE
R_HFE = R / MW_HFE #[kJ/kg-K]          Specific Gas Constant for HFE
h_evap_HFE = 0.0308 / MW_HFE #[kJ/kg]  Heat of Vaporization of HFE
Cp_HFEliquid = 1.172303 #[kJ/kg-K]     Specific Heat of HFE liquid
m_HFE = MW_HFE / (N_a * 1000) #[kg]    Mass of one HFE molecule
Ce_HFE = 1 #[]                         Evaporation Coefficient of HFE
Cc_HFE = 1 #[]                         Condensation Coefficient of HFE

#Propellant Tank
P0_tank = 101325 #[Pa]                                                  Initial pressure in prop tank (1 atm)
T0_tank = 300 #[K]                                                      Initial temperature in prop tank
V_tank = 14e-6 #[m^3]                                                   Total volume of prop tank (30mL)
volWater0_tank = 9.5e-6 #[m^3]                                          Initial volume of water in prop tank (14mL)
volHFE_liquid0_tank = 2.294e-6 #[m^3]                                   Initial volume of HFE in prop tank (10mL)
volAir0 = (2 * (V_tank - volWater0_tank)) - volHFE_liquid0_tank #[m^3]  Initial volume of air in prop tank
n_Air = (P0_tank * volAir0) / (R * T0_tank) #[mol]                      Number of moles of air in prop tank
A_HFE = 3.167e-5 #[m^2]                                                 Area from which HFE condenses and evaporates

#Collection Chamber
P0_CC = 0 #[Pa]           initial pressure in collection chamber
T0_CC = 300 #[K]          initial temperature in collection chamber
V_CC = 542.248e-6 #[m^3]  volume of CC (227.75mL) 

#Piping network
D_pipe = (1/8) / 39.37 #[m]        Pipe diameter
A = pi * ((D_pipe / 2)**2) #[m^2]  Area of pipe cross section

#Orifice
D_O = 0.000127 #[m]               Orifice diameter
A_O = pi * ((D_O / 2)**2) #[m^2]  Area of orifice
Beta = D_O / D_pipe #[]           Ratio of orifice to pipe diameter
CD_orifice = 0.6 #[]              Discharge coefficient of orifice
