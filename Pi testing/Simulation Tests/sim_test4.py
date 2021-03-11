# Sim test, round four. Trying to implement the synchronicity with a generator
# this time.

import time
import multiprocessing.shared_memory as sm

import numpy as np
from numba import njit, float64

from constants import *
from helpers import *


@njit(signature=(float64[:], float64), fastmath=True, cache=True)
def main(sim_data, dt, duration):
    # Variable initialization
    volWater_tank = VolWater0_tank                        #Initial volume of water in one Prop Tank [m^3]
    volWater_CC = 0                                       #Initial volume of water in Collection Chamber [m^3]
    tankPress = P0_tank                                   #Pressure in Prop Tank [Pa]
    cCPress = P0_CC                                       #Pressure in Collection Chamber [Pa]
    tankTempGas = T0_tank                                 #Temperature of gas in Prop Tank [K]
    tankTempLiquid_HFE = T0_tank                          #Temperature of HFE Liquid in Prop Tank [K]
    cCTempGas = T0_CC                                     #Temperature of gas in CC [K]
    cCTempLiquid = T0_CC                                  #Temperature of water liquid in CC [K]
    m_HFE_vapor = 0                                       #Initial mass of HFE vapor in prop tank
    m_HFE_liquid = VolHFE_liquid0_tank * nvcRho(T0_tank)  #Initial mass of HFE liquid in prop tank
    m_water_vapor = 0                                     #Initial mass of water vapor in CC
    m_water_liquid = 0                                    #Initial mass of water liquid in CC
    n_Gas = N_Air_tank                                    #Initial moles of gas in tank
    n_HFE_vapor = 0                                       #Initial moles of HFE vapor in tank
    volGas = VolAir0                                      #Initial volume of gas in tank [m^3]
    volWater_shut = 0                                     #Initial volume of water in prop tank when valve shuts [m^3]
    a_HFE_cond = A_HFE
    a_HFE_evap = A_HFE
    nAir_CC = N_Air_CC_0

    sim_time = 0
    
    while True:
        ambientP = StandardAtm(sim_data[0])
        
        if volWater_tank - volWater_shut < 0:
            break #TODO: incorporate this into logging scheme

        # Volumetric Flow Rate of Liquid Water Propellant through one orifice [m^3/s]
        flo_water = sim_data[1] * CD_orifice * A_O * np.sqrt(2 * np.abs(tankPress - cCPress) / (Rho_water * (1 - Beta**4)))
        if tankPress < cCPress:
            flo_water *= -1

        # Update of Liquid Water Propellant Volumes in Tank & CC [m^3]
        volWater_tank -= flo_water * dt
        volWater_CC += flo_water * dt


        # -=-=- PROPELLANT TANK -=-=-
        # Mass of Gas in the tank [kg]
        mAir_tank = (N_Air_tank * MW_Air) / 1000
        xAir2_tank = N_Air_tank / (N_Air_tank + n_HFE_vapor)
        xHFEvapor2_tank = n_HFE_vapor / (N_Air_tank + n_HFE_vapor)
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
            a_HFE_evap = 0
        elif m_HFE_vapor == 0:
            a_HFE_cond = 0

        m_HFE_transfer = HerKnu(Pvap_HFE, tankTempLiquid_HFE, tankTempGas, tankPress, M_HFE, a_HFE_evap, a_HFE_cond, Ce_HFE, Cc_HFE) * dt
        if tankPress > Pvap_HFE and m_HFE_transfer > 0:
            m_HFE_transfer = 0
            
        # Update mass of HFE liquid and vapor [kg]
        m_HFE_liquid -= m_HFE_transfer
        m_HFE_vapor += m_HFE_transfer
            
        # Update moles/volume of HFE vapor/liquid 
        vol_HFE_liquid = m_HFE_liquid / rho_HFE
        n_HFE_vapor = (m_HFE_vapor * 1000) / MW_HFE
            
        # Temperature of Gas [K]
        tankTempGas = ((m_HFE_transfer * Cp_HFEliquid * tankTempLiquid_HFE) + (mGas2_tank * CpGas2_tank * tankTempGas)) / ((Cp_HFEliquid * m_HFE_transfer) + (mGas2_tank * CpGas2_tank))

        # Update total amount of Gas (Air + HFE)
        n_Gas = n_HFE_vapor + N_Air_tank
        volGas = V_tank - volWater_tank - vol_HFE_liquid

        # Temperature Update [K]
        Q_HFE = m_HFE_transfer * H_evap_HFE
        tankTempLiquid_HFE += (-Q_HFE / (m_HFE_liquid * Cp_HFEliquid))


        # -=-=- COLLECTION CHAMBER -=-=-
        # Surface Area of Collected Water [m^2]
        r = ((3 * volWater_CC) / (4 * pi)) ** (1 / 3)
        A_water = 4 * pi * r * r

        # Vapor Pressure of Water [Pa]
        Pvap_water = waterVP(cCTempLiquid)

        # Evaporation Heat of Water [kJ/kg]
        h_evap_water = waterHV(cCTempLiquid) / 1000

        # Mass of water either evaporating or condensing at current timestep [kg]
        m_water_transfer = HerKnu(Pvap_water, cCTempLiquid, cCTempGas, cCPress, M_H2O, A_water, A_water, Ce_water, Cc_water) * dt
        if cCPress > Pvap_water and m_water_transfer > 0:
            m_water_transfer = 0
            
        # Mass of gas lost through vent solenoid [kg]
        nWaterVapor_CC = (m_water_vapor * 1000) / MW_Water
        rhoGas_CC = (((nAir_CC * MW_Air) / 1000) + ((nWaterVapor_CC * MW_Water) / 1000)) / (V_CC - (m_water_liquid / Rho_water))
        xAir_CC = nAir_CC / (nAir_CC + nWaterVapor_CC)
        xWaterVapor_CC = nWaterVapor_CC / (nWaterVapor_CC + nAir_CC)
        gammaGas_CC = 1 + (1 / ((xWaterVapor_CC / (GammaWV - 1)) + (xAir_CC / (GammaAir - 1))))
        m_lost = mDotThruOrifice(cCPress, ambientP, rhoGas_CC, gammaGas_CC, 0.1, VentSolenoidDiam * sim_data[2]) * dt
        m_water_lost = m_lost * xWaterVapor_CC
        n_Air_lost = ((m_lost * 1000) * xAir_CC) / MW_Air
            
        # Moles of Air in CC 
        nAir_CC -= n_Air_lost

        # Total mass of water vapor and liquid at current time [kg]
        m_water_vapor += m_water_transfer - m_water_lost
        m_water_liquid = (volWater_CC * Rho_water) - m_water_vapor

        # Pressure Update [Pa]
        cCPress = ((nAir_CC + nWaterVapor_CC) * R * cCTempGas) / (V_CC - (m_water_liquid / Rho_water))
            
        # Liquid Temperature Update [K]
        if m_water_liquid != 0:
            Q_water = m_water_transfer * h_evap_water
            mwn = flo_water * Rho_water * dt
            T1 = ((m_water_liquid - mwn) / m_water_liquid) * cCTempLiquid
            T2 = (mwn / m_water_liquid) * 300
            T3 = -Q_water / (m_water_liquid * Cp_water_liquid)
            cCTempLiquid = T1 + T2 + T3

        sim_time += dt
        if sim_time % duration < dt:
            yield np.array([]) #TODO: fill out with appropriate data


def run(dt, main_freq=100.0): #main_freq is frequency that main.py runs at (needed for synchronization)
    try:
        # Set up shared memory
        sensor_mem = sm.SharedMemory(name="sensors")
        sim_mem = sm.SharedMemory(name="simulation")
        sensor_data = np.ndarray(shape=(10, 15), dtype=np.float64, buffer=sensor_mem.buf) #Edit with correct size
        sim_data = np.ndarray(shape=(4,), dtype=np.float64, buffer=sim_mem.buf)
        # sim_data: [altitude, flowSol, ventSol, time since liftoff]

        start_t = time.time()
        period = 1 / main_freq

        sim = main(sim_data, dt, period)

        while True:
            assert abs((time.time() - start_t) - sim_data[3]) < 20 * period

            start_next = time.time() + 10 * period
            for i in range(10):
                sensor_data[i][:] = next(sim)

            duration = time.time() - start_next
            if duration > 0:
                time.sleep(duration)

    except:
        #Close shared memory
        sensor_mem.close()
        sim_mem.close()