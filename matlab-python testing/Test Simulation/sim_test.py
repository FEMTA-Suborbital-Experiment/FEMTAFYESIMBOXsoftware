import matplotlib.pyplot as plt
import numpy as np
import sys

from numba import jit, void

from constants import *
from test_helpers import *

h = np.load("altitude.npy").reshape((99840,))
t = np.load("time.npy").reshape((99840,))

# Variable initialization
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
count = 0
dt = 2e-4    #timestep [s] (maximum: 2e-4)

num_samples = int((max(t) / dt) // 100)

# Array initialization
tankVolWater_array = np.empty((num_samples,))
tankPress_array = np.empty((num_samples,))
tankTempGas_array = np.empty((num_samples,))
tankTempLiquid_array = np.empty((num_samples,))
CCVolWater_array = np.empty((num_samples,))
CCPress_array = np.empty((num_samples,))
CCPress_preExp_array = np.empty((num_samples,))
CCTempGas_array = np.empty((num_samples,))
CCTempLiquid_array = np.empty((num_samples,))
PvapHFE_array = np.empty((num_samples,))
PvapWater_array = np.empty((num_samples,))
QHFE_array = np.empty((num_samples,))
Qwater_array = np.empty((num_samples,))
time_array = np.empty((num_samples,))
m_HFE_transfer_array = np.empty((num_samples,))
m_HFE_vapor_array = np.empty((num_samples,))
m_HFE_liquid_array = np.empty((num_samples,))
tankVolGas_array = np.empty((num_samples,))
n_Gas_array = np.empty((num_samples,))
m_water_vapor_array = np.empty((num_samples,))
m_water_liquid_array = np.empty((num_samples,))
m_water_transfer_array = np.empty((num_samples,))
m_water_unaltered_array = np.empty((num_samples,))
h_evap_water_array = np.empty((num_samples,))
m_HFE_unaltered_array = np.empty((num_samples,))
volGas_array = np.empty((num_samples,))
nGas_array = np.empty((num_samples,))
m_HFE_total_array = np.empty((num_samples,))
m_water_total_array = np.empty((num_samples,))
m_water_liquid_tank_array = np.empty((num_samples,))
nAir_CC_array = np.empty((num_samples,))
m_water_lost_array = np.empty((num_samples,))
n_Air_lost_array = np.empty((num_samples,))
m_lost_array = np.empty((num_samples,))
nWaterVapor_CC_array = np.empty((num_samples,))
altitude_array = np.empty((num_samples,))
flo_water_array = np.empty((num_samples,))

#while time < max(t) and count < num_samples:

@jit(nopython=True, parallel=True, fastmath=True)
def loop():
    if not count % 5000: print(count)
        
    alt = np.interp(time, t, h)
    _, ambientP, _ = StandardAtm(alt)
    
    if volWater_tank - volWater_shut < 0:
        raise Exception("Tank Volume Empty") #TODO: incorporate this into logging scheme
    
    # Condition for beginning experiment -> for testing only
    if alt < 80000:
        ventSol = 1
        flowSol = 0
    else:
        flowSol = 1 if time > 200 else 2
        ventSol = 1
    
    # Conditions for loop termination
    if flowSol == 1 and volWater_shut == 0:
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
    m_water_liquid_tank = volWater_tank * rho_water

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

    # Check total mass of HFE in Prop Tank [kg]
    m_HFE_total = m_HFE_liquid + m_HFE_vapor

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
        T2 = (mwn / m_water_liquid) * 300
        T3 = -Q_water / (m_water_liquid * Cp_water_liquid)
        CCTempLiquid = T1 + T2 + T3

    # Update total mass of water in the system [kg]
    m_water_total = m_water_vapor + m_water_liquid + (volWater_tank * rho_water)

    # -=-=- Array Update -=-=-
    if not count % 100:
        # Propellant Tank
        tankVolWater_array[count // 100] = volWater_tank
        tankPress_array[count // 100] = tankPress
        tankTempGas_array[count // 100] = tankTempGas
        tankTempLiquid_array[count // 100] = tankTempLiquid_HFE
        tankVolGas_array[count // 100] = volGas
        m_HFE_vapor_array[count // 100] = m_HFE_vapor
        m_HFE_liquid_array[count // 100] = m_HFE_liquid
        n_Gas_array[count // 100] = n_Gas
        volGas_array[count // 100] = volGas
        nGas_array[count // 100] = n_Gas
        m_HFE_total_array[count // 100] = m_HFE_total
        m_water_liquid_tank_array[count // 100] = m_water_liquid_tank
        m_HFE_transfer_array[count // 100] = m_HFE_transfer

        # Collection Chamber
        CCVolWater_array[count // 100] = volWater_CC
        CCPress_array[count // 100] = CCPress
        CCTempGas_array[count // 100] = CCTempGas
        CCTempLiquid_array[count // 100] = CCTempLiquid
        m_water_vapor_array[count // 100] = m_water_vapor
        m_water_liquid_array[count // 100] = m_water_liquid
        m_water_transfer_array[count // 100] = m_water_transfer
        h_evap_water_array[count // 100] = h_evap_water
        m_water_total_array[count // 100] = m_water_total
        nAir_CC_array[count // 100] = nAir_CC
        m_water_lost_array[count // 100] = m_water_lost
        n_Air_lost_array[count // 100] = n_Air_lost
        m_lost_array[count // 100] = m_lost
        nWaterVapor_CC_array[count // 100] = nWaterVapor_CC

        # Miscellaneous
        PvapHFE_array[count // 100] = Pvap_HFE
        QHFE_array[count // 100] = Q_HFE
        PvapWater_array[count // 100] = Pvap_water
        flo_water_array[count // 100] = flo_water
        time_array[count // 100] = time
        altitude_array[count // 100] = alt

    time += dt
    count += 1

while (time < max(t)) and (count < num_samples):
    loop()


# -=-=- PLOTS -=-=-
# Volumes of both Prop Tank and CC
plt.figure(1)
plt.plot(time_array[:count], tankVolWater_array[:count] * 10**6, linewidth=3)
#hold on
plt.plot(time_array[:count], CCVolWater_array[:count] * 10**6, linewidth=3)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Volume of Water [mL]", fontsize=17)
plt.legend(("Propellant Tank", "Collection Chamber"), fontsize=15)
plt.title("Volumes of Collection Chamber and Propellant Tank", fontsize=22)

# Temperature in Prop Tank
plt.figure(2)
plt.plot(time_array[:count], tankTempGas_array[:count], linewidth=3)
#hold on
plt.plot(time_array[:count],tankTempLiquid_array[:count], linewidth=3)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Temperature [K]", fontsize=17)
plt.legend(("Gas (Air + HFE Vapor)", "Liquid HFE"), fontsize=15)
plt.title("Temperature in Propellant Tank", fontsize=22)

# Temperature in CC
plt.figure(3)
plt.plot(time_array[:count], CCTempGas_array[:count], linewidth=3)
#hold on
plt.plot(time_array[:count], CCTempLiquid_array[:count], linewidth=3)
plt.legend(("Water Vapor", "Liquid Water"), fontsize=15)
plt.title("Temperature in Collection Chamber", fontsize=22)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Temperature [K]", fontsize=17)

# Pressure in Prop Tank
plt.figure(4)
plt.plot(time_array[:count], tankPress_array[:count]/1000, linewidth=3)
#hold on
plt.plot(time_array[:count],PvapHFE_array[:count]/1000, linewidth=3)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Pressure [kPa]", fontsize=17)
plt.legend(("Propellant Tank Pressure", "Vapor Pressure of HFE"), fontsize=15)
plt.title("Pressures in Propellant Tank", fontsize=22)

# Pressures in CC
plt.figure(5)
plt.plot(time_array[:count], CCPress_array[:count]/1000, linewidth=3)
#hold on
plt.plot(time_array[:count], PvapWater_array[:count]/1000, linewidth=3)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Pressure [kPa]", fontsize=17)
plt.legend(("Collection Chamber Pressure", "Vapor Pressure of Water"), fontsize=15)
plt.title("Pressures in Collection Chamber", fontsize=22)

# Mass of HFE in All States
plt.figure(6)
plt.plot(time_array[:count], m_HFE_vapor_array[:count]*1000, linewidth=2)
#hold on
plt.plot(time_array[:count], m_HFE_liquid_array[:count]*1000, linewidth=2)
plt.plot(time_array[:count], m_HFE_total_array[:count]*1000, linewidth=2)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Mass of HFE [g]", fontsize=17)
plt.title("Amount of HFE in Each State", fontsize=22)
plt.legend(("HFE Vapor", "HFE Liquid", "HFE Total"), fontsize=15)

# Mass of Water in All States
plt.figure(7)
plt.plot(time_array[:count], m_water_vapor_array[:count]*1000, linewidth=2)
#hold on
plt.plot(time_array[:count], m_water_liquid_array[:count]*1000, linewidth=2)
plt.plot(time_array[:count], m_water_total_array[:count]*1000, linewidth=2)
plt.plot(time_array[:count], tankVolWater_array[:count]*rho_water*1000, linewidth=2)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Mass of Water [g]", fontsize=17)
plt.title("Amount of Water in Each State", fontsize=22)
plt.legend(("Water Vapor", "Water Liquid", "Water Total", "Water in One Prop Tank"), fontsize=15)

# Altitude vs Time
plt.figure(8)
plt.plot(time_array[:count], altitude_array[:count], linewidth=2)
plt.xlabel("Time [s]", fontsize=17)
plt.ylabel("Altitude [m]", fontsize=17)
plt.title("Flight Altitude", fontsize=22)

plt.show()
