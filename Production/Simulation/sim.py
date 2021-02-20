# Main virtual environment simulation file.

import multiprocessing.shared_memory as sm

import numba

from .constants import *
from .helpers import nvcVP, nvcRho, waterVP, HerKnu, waterHV, mDotThruOrifice

# Variable initializations
volWater_tank = volWater0_tank                      #Initial volume of water in one Prop Tank [m^3]
volWater_CC = 0                                     #Initial volume of water in Collection Chamber [m^3]
volHFE_liquid = volHFE_liquid0_tank                 #Volume of HFE liquid in Prop Tank [m^3]
tankPress = P0_tank                                 #Pressure in Prop Tank [Pa]
CCPress = P0_CC                                     #Pressure in Collection Chamber [Pa]
tankTempGas = T0_tank                               #Temperature of gas in Prop Tank [K]
tankTempLiquid_HFE = T0_tank                        #Temperature of HFE Liquid in Prop Tank [K]
CCTempGas = T0_CC                                   #Temperature of gas in CC [K]
CCTempLiquid = T0_CC                                #Temperature of water liquid in CC [K]
m_HFE_vapor = 0                                     #Initial mass of HFE vapor in prop tank
m_HFE_liquid = volHFE_liquid0_tank*nvcRho(T0_tank)  #Initial mass of HFE liquid in prop tank
m_water_vapor = 0                                   #Initial mass of water vapor in CC
m_water_liquid = 0                                  #Initial mass of water liquid in CC
n_Gas = nAir_tank                                   #Initial moles of gas in tank
n_HFE_vapor = 0                                     #Initial moles of HFE vapor in tank
volGas = volAir0                                    #Initial volume of gas in tank [m^3]
volWater_shut = 0                                   #Initial volume of water in prop tank when valve shuts [m^3]
n_air_lost = 0
A_HFE_cond = A_HFE
A_HFE_evap = A_HFE

time = 0
dt = 1e-4    #timestep [s] (will not run accurately at more than 1e-5)


def loop():
    pass

while altitude:
    loop()
