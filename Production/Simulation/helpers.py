#Vapor Pressure of NV 7100 (T in K, vp in Pa)
import numpy as np
from math import pi, sqrt, pow, exp
def nvcVP(T):
    vp = exp(22.415 - 3641.9 * (1/T));
    return vp

#Density of NV 7100 Liquid (T in K)
def nvcRho(T):
    dD = 1.5383 - 0.002269*(T-273.15);
    dD = dD / (1000 * 0.000001); #kg/m^3
    return dD


#Vapor Pressure of Water (T in K, vp in Pa)
def waterVP(T):
    vp=np.power(10,(8.07131-(np.divide(1730.63,(233.426+(T-273))))));        #pressure in mmHg
    vp=vp*133;                                            #conversion to Pa from mmHg
    return vp

#Mass transfer from gas to liquid [kg/s] (HERTZ-KNUDSEN EQUATION)
#Negative denotes vapor to liquid (condensation), Positive denotes liquid to vapor
#(evaporation)
def HerKnu(Ps,T_liquid,T_vapor,Pg,m,A_evap,A_cond,C_evap,C_cond):
    global kB;
    m_transfer=(sqrt(m/(2*pi*kB))*((A_evap*C_evap*(Ps/sqrt(T_liquid)))-(A_cond*C_cond*(Pg/sqrt(T_vapor)))));
    return m_transfer

#Heat of Vaporization of Water [J/kg]
def waterHV(T):
    Hvs=[2500.9, 2496.2, 2491.4, 2477.2, 2467.7, 2458.3, 2453.5, 2441.7, 2429.8, 2420.3, 2406, 2396.4, 2381.9, 2372.3, 2357.7, 2333, 2308, 2282.5, 2266.9, 2256.4, 2229.6, 2202.1, 2144.3, 2082, 2014.2, 1939.7, 1857.4, 1765.4, 1661.6, 1543, 1404.6, 1238.4, 1027.3, 719.8];
    Ts=[0.00, 2, 4, 10, 14, 18, 20, 25, 30, 34, 40, 44, 50, 54, 60, 70, 80, 90, 96, 100, 110, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360]+273;
    #hv=interp1(Ts, Hvs, T, 'linear').*1000;
    hv=np.multiply(np.interp(T,Ts,Hvs),1000)
    if np.isnan(hv):
        hv=0;
    return hv

#mDotThruOrifice calculates mass flow (mDot) in kg/s through an orifice
#given pressures and working fluid properties
def mDotThruOrifice(in1,in2,in3,in4,in5,in6):
#   Variable description:
#       in1: pressure upstream (Pa)
#       in2: pressure downstream (Pa)
#       in3: fluid density (kg/m^3)
#       in4: gamma = (fluidCP/fluidCV)
#       in5: orifice discharge coefficient
#       in6: orifice diameter (m)
#
#   Note on in1 and in2 variables:
#       The sign convention used in this function assumes normal (positive)
#       fluid movement from the in1 region to the in2 region (in1 is
#       upstream, in2 is downstream). However, these variables may be 
#       reversed so that there is flow from in2 to in1, however, the
#       resulting mDot will be negative.
#   
    if in1 < in2:
        downP = in1;
        upP = in2;
        directionSign = -1;
    else:
        upP = in1;
        downP = in2;
        directionSign = 1;

    rho = in3;
    gamma = in4;
    outletCD = in5;
    outletDia = in6;
    outletArea = pi*pow((outletDia/2),2);
    #fprintf("%0.3f, %0.3f, %0.6f, ", upP, downP, rho);
    #
    criticalP = upP * pow(2/(gamma+1),gamma/(gamma-1));
    #fprintf("%0.3f, %0.3f, ", criticalP, downP);
    if(downP < criticalP):
        #Choked
        #fprintf("C\n");
        r = downP/criticalP;
        r = pow((2/(gamma+1)),(gamma/(gamma-1)));
        mDot = outletCD*outletArea*sqrt(upP*rho*(2*gamma/(gamma-1))*pow(r,(2/gamma))*(1-pow(r,((gamma-1)/gamma)))); #kg/s
        #fprintf("%0.20f, ", rho);
    else:
        #Subsonic
        #fprintf("S\n");
        r = downP/upP;
        mDot = outletCD*outletArea*sqrt(upP*rho*(2*gamma/(gamma-1))*pow(r,(2/gamma))*(1-pow(r,((gamma-1)/gamma)))); #kg/s

    #fprintf("\n");
    mDot = mDot * directionSign; #Corrects sign on mDot to follow stated convention above
    return mDot
    #fprintf("%0.3f, %0.3f, ", criticalP, downP);
    if(downP < criticalP):
        #Choked
        #fprintf("C\n");
        r = downP/criticalP;
        r = pow((2/(gamma+1)),(gamma/(gamma-1)));
        mDot = outletCD*outletArea*sqrt(upP*rho*(2*gamma/(gamma-1))*pow(r,(2/gamma))*(1-pow(r,((gamma-1)/gamma)))); #kg/s
        #fprintf("%0.20f, ", rho);
    else:
        #Subsonic
        #fprintf("S\n");
        r = downP/upP;
        mDot = outletCD*outletArea*sqrt(upP*rho*(2*gamma/(gamma-1))*pow(r,(2/gamma))*(1-pow(r,((gamma-1)/gamma)))); #kg/s

    #fprintf("\n");
    mDot = mDot * directionSign; #Corrects sign on mDot to follow stated convention above
    return mDot
