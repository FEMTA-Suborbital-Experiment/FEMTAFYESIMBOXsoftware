# Set of functions called from sim.py

import numpy as np
from numba import jit, float32, guvectorize
from constants import *


# fastmath allows floating-point operations to be performed in an unsafe matter, sacrificing accuracy for speed
toggle_fastmath = True

# Vapor Pressure of NV 7100 (T in K, vp in Pa)
@jit(float32(float32), fastmath=toggle_fastmath, nopython=True)
def nvcVP(T):
    return np.exp(22.415 - 3641.9 * (1 / T))


# Density of NV 7100 Liquid (T in K)
@jit(float32(float32), fastmath=toggle_fastmath, nopython=True)
def nvcRho(T):
    dD = 1.5383 - 0.002269 * (T - 273.15)
    dD /= (1000 * 0.000001) #kg/m^3
    return dD


# Vapor Pressure of Water (T in K, vp in Pa)
@jit(float32(float32), fastmath=toggle_fastmath, nopython=True)
def waterVP(T):
    vp = 10 ** (8.07131 - (1730.63 / (233.426 + (T - 273)))) #pressure in mmHg
    vp *= 133 #conversion to Pa from mmHg
    return vp


# Mass transfer from gas to liquid [kg/s] (HERTZ-KNUDSEN EQUATION)
# Negative denotes vapor to liquid (condensation), Positive denotes liquid to vapor
# (evaporation)
@jit(float32(float32, float32, float32, float32, float32, float32, float32, float32, float32), fastmath=True, nopython=True)
def HerKnu(Ps, T_liquid, T_vapor, Pg, m, A_evap, A_cond, C_evap, C_cond):
    m_transfer = np.sqrt(m / (2 * pi * kB)) * ((A_evap * C_evap * (Ps / np.sqrt(T_liquid))) - (A_cond * C_cond * (Pg / np.sqrt(T_vapor))))
    return m_transfer


# Heat of Vaporization of Water [J/kg]
@guvectorize(float32(float32[:]), nopython=True)
def waterHV(T):
    Hvs = np.array([2500.9, 2496.2, 2491.4, 2477.2, 2467.7, 2458.3, 2453.5, 2441.7, 2429.8, 2420.3, 2406, 2396.4, 2381.9, 2372.3, 2357.7, 2333, 2308, 2282.5, 2266.9, 2256.4, 2229.6, 2202.1, 2144.3, 2082, 2014.2, 1939.7, 1857.4, 1765.4, 1661.6, 1543, 1404.6, 1238.4, 1027.3, 719.8])
    Ts = 273 + np.array([0.00, 2, 4, 10, 14, 18, 20, 25, 30, 34, 40, 44, 50, 54, 60, 70, 80, 90, 96, 100, 110, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360])
    return 1000 * np.interp(T, Ts, Hvs)


# mDotThruOrifice calculates mass flow (mDot) in kg/s through an orifice
# given pressures and working fluid properties
@jit(float32(float32, float32, float32, float32, float32, float32), fastmath=toggle_fastmath, nopython=True)
def mDotThruOrifice(in1, in2, rho, gamma, outletCD, outletDia):
#   Variable description:
#       in1: pressure upstream (Pa)
#       in2: pressure downstream (Pa)
#       rho: fluid density (kg/m^3)
#       gamma:= (fluidCP/fluidCV)
#       outletCD: orifice discharge coefficient
#       outletDia: orifice diameter (m)
#
#   Note on in1 and in2 variables:
#       The sign convention used in this function assumes normal (positive)
#       fluid movement from the in1 region to the in2 region (in1 is
#       upstream, in2 is downstream). However, these variables may be 
#       reversed so that there is flow from in2 to in1, however, the
#       resulting mDot will be negative.

    direction = 1 if in1 > in2 else -1
    if direction == 1:
        upP = in1
        downP = in2
    else:
        downP = in1
        upP = in2

    outletArea = pi * (outletDia / 2) ** 2
    gamma_const = np.pow(2 / (gamma + 1), gamma / (gamma - 1))
    criticalP = upP * gamma_const

    if(downP < criticalP): #Choked
        r = downP / criticalP
        r = gamma_const
    else: #Subsonic
        r = downP / upP

    mDot = outletCD * outletArea * np.sqrt(upP * rho * (2 * gamma / (gamma-1)) * np.pow(r, (2 / gamma)) * (1 - np.pow(r, ((gamma - 1) / gamma)))) #kg/s
    return mDot * direction #Corrects sign on mDot to follow stated convention above


@jit(float32[:])
def StandardAtm(h):
    
    rho_sea = 1.2250;     # density at sea level, kg/ m^3
    p_sea   = 1.01325*pow(10,5);  # pressure at sea level, N/m^2
    R       = 287;        # gas constant, J/kg/K
    g_zero  = 9.81;       # gravitatoinal acceleration, m/s^2

    T_set   = [288.16,216.66,216.66,282.66,282.66,165.66,165.66,225.66]; # list of temperature points that define endpoints of each layer (starting at the ground), K
    h_set   = [0,11000,25000,47000,53000,79000,90000,105000]; #list of altitude points that define endpoints of each layer (starting at the ground), m
    a_set   = [-6.5*pow(10,-3),0,3*pow(10,-3),0,-4.5*pow(10,-3),0,4*pow(10,-3)];#list of gradient layer slopes (starting at the ground), K/m
    p_set   = [p_sea, 2.27*pow(10,4), 2.5273*pow(10,3), 1.2558*pow(10,2), 61.493, 1.2595, 0.162723]; # list of pressure at each layer endpoint, N/m^2
    rho_set = [rho_sea, 3.648*pow(10,-1), 4.0639*pow(10,-2), 1.5535*pow(10,-3), 7.5791*pow(10,-4), 2.184*pow(10,-5), 1.84114*pow(10,-6)]; # list of density at each layer endpoint, kg/m^3
            
    if h <= h_set[1]:
        layer = 0;
    elif h <= h_set[2]:
        layer = 1;
    elif h <= h_set[3]:
        layer = 2;
    elif h <= h_set[4]:
        layer = 3;
    elif h <= h_set[5]:
        layer = 4;
    elif h <= h_set[6]:
        layer = 5;
    else:
        layer = 6;
    
    
    if (layer+1)%2 == 1:
        #Gradient layer
        T = T_set[layer] + (a_set[layer] * (h - h_set[layer])); # temperature equation for gradient layer, K
        p = p_set[layer] * (pow((T / T_set[layer]), (-g_zero / (a_set[layer] * R)))); # pressure equation for gradient layer, N/m^2
        rho = rho_set[layer]* pow((T / T_set[layer]),((-g_zero / (a_set[layer]*R))+1)); # density equation for gradient layer, kg/m^3
        
    else:
        #Isothermal layers
        T = T_set[layer]; # temperature for isothermal layer, K
        p = p_set[layer] * exp((-g_zero * (h - h_set[layer])) / (R * T)); # pressure equation for isothermal layer, N/m^2
        rho = (p * rho_set[layer]) / p_set[layer]; # density equation for isothermal layer, kg/m^3
    
    return [T,p,rho]

