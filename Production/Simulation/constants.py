# File holding physical constants for use by the virtual environment
# simulation functions. Use "import constants" or "from constants import *".

from math import pi

R = 8.3145 #[J/mol-K]                   Universal Gas Constant
kB = 1.380649e-23 #[J/K]                Boltzmann constant
N_a = 6.02214e23 #[# of particles/mol]  Avogadros number

#Air Properties
gammaAir = 1.4 #[]           Ratio of specific heats for air
MW_Air = 29 #[g/mol]         Molecular Weight of Air
R_air = R / MW_Air #[J/g-K]  Specific Gas Constant for Air
Cp_Air = 1.005 #[kJ/kg-K]    Specific Heat of Air
 
#Water Properties
gammaWV = 1.33 #[]              Ratio of specific heats for water vapor
rho_water = 997 #[kg/m^3]       Density of liquid water
m_H2O = 2.988e-26 #[kg]         Mass of one water molecule
MW_Water = 18.0135 #[g/mol]     Molecular weight of water
R_wv = R / MW_Water #[J/g-K]    Specific gas constant for water vapor
Cp_water_liquid = 4 #[kJ/kg-K]  Specific heat of liquid water
Cp_water_vapor = 2 #[kJ/kg-K]   Specific heat of water vapor
Ce_water = 1 #[]                Evaporation Coefficient of water
Cc_water = 1 #[]                Condensation Coefficient of water

#HFE Properties
MW_HFE = 250 #[g/kmol]               Molecular Weight of HFE
R_HFE = R / MW_HFE #[J/g-K]          Specific Gas Constant for HFE
h_evap_HFE = 125.6 #[kJ/kg]          Heat of Vaporization of HFE
Cp_HFEliquid = 1.172303 #[kJ/kg-K]   Specific Heat of HFE liquid
m_HFE = MW_HFE / (N_a * 1000) #[kg]  Mass of one HFE molecule
Ce_HFE = 1 #[]                       Evaporation Coefficient of HFE
Cc_HFE = 0.1 #[]                     Condensation Coefficient of HFE

#Propellant Tank
P0_tank = 101325 #[Pa]                                          Initial pressure in prop tank (1 atm)
T0_tank = 300 #[K]                                              Initial temperature in prop tank
V_tank = 142.567e-6 #[m^3]                                      Total volume of prop tank (30mL)
volAir0 = 0.328e-6 #[m^3]                                       Initial volume of air in both prop tanks
nAir_tank = (P0_tank * volAir0) / (R * T0_tank) #[mol]          Number of moles of air in both prop tanks
volHFE_liquid0_tank = 0.983e-6 #[m^3]                           Initial volume of HFE in both prop tanks (0.983mL)
volWater0_tank = V_tank - volAir0 - volHFE_liquid0_tank #[m^3]  Initial volume of water in both prop tanks
A_HFE = 3.167e-5 #[m^2]                                         Area from which HFE condenses and evaporates

#Collection Chamber
P0_CC = 101325 #[Pa]                     Initial pressure in collection chamber
T0_CC = 300 #[K]                         Initial temperature in collection chamber
V_CC = 542.248e-6 #[m^3]                 Volume of CC (542.248mL) 
ventSolenoidDiam = 2.18e-3 #[m]          Diameter of vent solenoid
CCBeta = ventSolenoidDiam / 0.09398 #[]  Ratio of vent solenoid orifice to CC cross section

#Piping network
D_pipe = (1/8) / 39.37 #[m]        Pipe diameter
A = pi * ((D_pipe / 2)**2) #[m^2]  Area of pipe cross section

#Orifice
D_O = 0.3e-3 #[m]                 Orifice diameter
A_O = pi * ((D_O / 2)**2) #[m^2]  Area of orifice
Beta = D_O / D_pipe #[]           Ratio of orifice to pipe diameter
CD_orifice = 0.6 #[]              Discharge coefficient of orifice
