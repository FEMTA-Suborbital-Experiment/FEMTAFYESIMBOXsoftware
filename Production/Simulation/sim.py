# Main virtual environment simulation file.

import numpy as np
import multiprocessing.shared_memory as sm

import numba

from .constants import *
from .helpers import nvcVP, nvcRho, waterVP, HerKnu, waterHV, mDotThruOrifice, StandardAtm

# Set up shared memory
sensor_mem = sm.SharedMemory(name="sensors") 
valve_mem = sm.SharedMemory(name="valves")
sensor_data = np.ndarray(shape=(15,), dtype=np.float64, buffer=sensor_mem.buf) #Edit with correct size
valve_states = np.ndarray(shape=(6,), dtype=np.bool, buffer=valve_mem.buf)

# Variable initializations
volWater_tank = volWater0_tank                        #Initial volume of water in one Prop Tank [m^3]
volWater_CC = 0                                       #Initial volume of water in Collection Chamber [m^3]
volHFE_liquid = volHFE_liquid0_tank                   #Volume of HFE liquid in Prop Tank [m^3]
tankPress = P0_tank                                   #Pressure in Prop Tank [Pa]
CCPress = P0_CC                                       #Pressure in Collection Chamber [Pa]
tankTempGas = T0_tank                                 #Temperature of gas in Prop Tank [K]
tankTempLiquid_HFE = T0_tank                          #Temperature of HFE Liquid in Prop Tank [K]
CCTempGas = T0_CC                                     #Temperature of gas in CC [K]
CCTempLiquid = T0_CC                                  #Temperature of water liquid in CC [K]
m_HFE_vapor = 0                                       #Initial mass of HFE vapor in prop tank
m_HFE_liquid = volHFE_liquid0_tank * nvcRho(T0_tank)  #Initial mass of HFE liquid in prop tank
m_water_vapor = 0                                     #Initial mass of water vapor in CC
m_water_liquid = 0                                    #Initial mass of water liquid in CC
n_Gas = nAir_tank                                     #Initial moles of gas in tank
n_HFE_vapor = 0                                       #Initial moles of HFE vapor in tank
volGas = volAir0                                      #Initial volume of gas in tank [m^3]
volWater_shut = 0                                     #Initial volume of water in prop tank when valve shuts [m^3]
n_air_lost = 0
A_HFE_cond = A_HFE
A_HFE_evap = A_HFE

time = 0
dt = 2e-4    #timestep [s] (maximum: 2e-4)


def loop():
        #alt=interp1(t,h,time); do this from main.py and put altitude in shared array
        _, ambientP, _ = StandardAtm(altitude)
        
        if volWater_tank - volWater_shut < 0:
            raise Exception("Tank Volume Empty") #TODO: incorporate this into logging scheme
        
        # Conditions for loop termination
        if flowSol == 1 and  volWater_shut == 0:
            volWater_shut = 0.5 * volWater_tank
        elif flowSol == 2:
            volWater_shut = 0

        # Volumetric Flow Rate of Liquid Water Propellant through one orifice [m^3/s]
        flo_water = flowSol * CD_orifice * A_O * np.sqrt(2 * np.abs(tankPress - CCPress) / (rho_water * (1 - Beta**4)))
        if tankPress < CCPress:
            flo_water *= -1

        # Update of Liquid Water Propellant Volumes in Tank & CC [m^3]
        volWater_tank -= flo_water * dt
        volWater_CC += flo_water * dt

        # -=-=- PROPELLANT TANK -=-=-
        # Mass of Gas in the tank [kg]
        mAir_tank = (nAir_tank * MW_Air) / 1000
        xAir2_tank = nAir_tank / (nAir_tank + n_HFE_vapor)
        xHFEvapor2_tank = n_HFE_vapor / (nAir_tank + n_HFE_vapor)
        yAir2_tank = mAir_tank / (mAir_tank + m_HFE_vapor)
        yHFEvapor2_tank = m_HFE_vapor / (mAir_tank + m_HFE_vapor)
        MWGas2_tank = (MW_Air * xAir2_tank) + (MW_HFE * xHFEvapor2_tank)
        mGas2_tank = (n_Gas * MWGas2_tank) / 1000
            
        # Specific Heat of Gas in Tank before HFE transfer (state 2) [kJ/kg-K]
        CpGas2_tank = (Cp_Air * yAir2_tank) + (Cp_HFEliquid * yHFEvapor2_tank)
            
        # Vapor Pressure of HFE [Pa]
        Pvap_HFE = nvcVP(tankTempLiquid_HFE)

        # Density of HFE liquid [kg/m^3]
        rho_HFE = nvcRho(tankTempLiquid_HFE)

        # Pressure of Gas [Pa]
        tankPress = (n_Gas * R * tankTempGas) / volGas

        # Amount of HFE either condensing or evaporating [kg]
        if m_HFE_liquid == 0:
            A_HFE_evap = 0
        elif m_HFE_vapor == 0:
            A_HFE_cond = 0

        m_HFE_transfer = HerKnu(Pvap_HFE, tankTempLiquid_HFE, tankTempGas, tankPress, m_HFE, A_HFE_evap, A_HFE_cond, Ce_HFE, Cc_HFE) * dt
        if tankPress > Pvap_HFE and m_HFE_transfer > 0:
            m_HFE_transfer = 0
            
        # Update mass of HFE liquid and vapor [kg]
        m_HFE_liquid = m_HFE_liquid - m_HFE_transfer
        m_HFE_vapor = m_HFE_transfer + m_HFE_vapor
            
        # Update moles/volume of HFE vapor/liquid 
        vol_HFE_liquid = m_HFE_liquid / rho_HFE
        n_HFE_vapor = (m_HFE_vapor * 1000) / MW_HFE
            
        # Temperature of Gas [K]
        tankTempGas = ((m_HFE_transfer * Cp_HFEliquid * tankTempLiquid_HFE) + (mGas2_tank * CpGas2_tank * tankTempGas)) / ((Cp_HFEliquid * m_HFE_transfer) + (mGas2_tank * CpGas2_tank))

        # Update total amount of Gas (Air + HFE)
        n_Gas = n_HFE_vapor + nAir_tank
        volGas = V_tank - volWater_tank - vol_HFE_liquid

        # Temperatrue Update [K]
        Q_HFE = m_HFE_transfer * h_evap_HFE
        tankTempLiquid_HFE += (-Q_HFE / (m_HFE_liquid * Cp_HFEliquid))

        # -=-=- COLLECTION CHAMBER -=-=-
        # Surface Area of Collected Water [m^2]
        r = ((3 * volWater_CC) / (4 * pi)) ** (1 / 3)
        A_water = 4 * pi * r * r

        # Vapor Pressure of Water [Pa]
        Pvap_water = waterVP(CCTempLiquid)

        # Evaporation Heat of Water [kJ/kg]
        h_evap_water = waterHV(CCTempLiquid) / 1000

        # Mass of water either evaporating or condensing at current timestep [kg]
        m_water_transfer = HerKnu(Pvap_water, CCTempLiquid, CCTempGas, CCPress, m_H2O, A_water, A_water, Ce_water, Cc_water) * dt
        if CCPress > Pvap_water and m_water_transfer > 0:
            m_water_transfer = 0
            
        # Mass of gas lost through vent solenoid [kg]
        nWaterVapor_CC = (m_water_vapor * 1000) / MW_Water
        rhoGas_CC = (((nAir_CC * MW_Air) / 1000) + ((nWaterVapor_CC * MW_Water) / 1000)) / (V_CC - (m_water_liquid / rho_water))
        xAir_CC = nAir_CC / (nAir_CC + nWaterVapor_CC)
        xWaterVapor_CC = nWaterVapor_CC / (nWaterVapor_CC + nAir_CC)
        gammaGas_CC = 1 + (1 / ((xWaterVapor_CC / (gammaWV - 1)) + (xAir_CC / (gammaAir - 1))))
        m_lost = mDotThruOrifice(CCPress, ambientP, rhoGas_CC, gammaGas_CC, 0.1, ventSolenoidDiam * ventSol) * dt
        m_water_lost = m_lost * xWaterVapor_CC
        n_Air_lost = ((m_lost * 1000) * xAir_CC) / MW_Air
            
        # Moles of Air in CC 
        nAir_CC = nAir_CC - n_Air_lost

        # Total mass of water vapor and liquid at current time [kg]
        m_water_vapor = m_water_transfer - m_water_lost + m_water_vapor
        m_water_liquid = (volWater_CC * rho_water) - m_water_vapor

        # Pressure Update [Pa]
        CCPress = ((nAir_CC + nWaterVapor_CC) * R * CCTempGas) / (V_CC - (m_water_liquid / rho_water))
            
        # Liquid Temperature Update [K]
        if m_water_liquid != 0:
            Q_water = m_water_transfer * h_evap_water
            mwn = flo_water * rho_water * dt
            T1 = ((m_water_liquid - mwn) / m_water_liquid) * CCTempLiquid
            T2= (mwn / m_water_liquid) * 300
            T3 = -Q_water / (m_water_liquid * Cp_water_liquid)
            CCTempLiquid = T1 + T2 + T3

        time += dt

def run():
    try:
        while altitude:
            loop()
    finally:
        #Close shared memory
        sensor_mem.close()
        valve_mem.close()
