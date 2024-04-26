# Formula to Calculate the Optimal Pipe Diameter for the Fuel Lines

from math import pi
import numpy as np
from numpy import log10, sqrt
from scipy.optimize import brentq

# Flow rate of fluid (m^3 / s)
FlowRateLOX = 0.6/1000
FlowRateEthanol = 0.4/1000

# Dynamic viscocity of fluid (Pa s) at respective flow temperature
DynamicViscosityLOX = 
DynamicViscosityEthanol = 

# Specify the acceptable pressure drop (Pa)
PressureDropLOX = 5 * 10 ** 5
PressureDropEthanol = 5 * 10 ** 5

# Specify the length of the pipe (m)
PipeLengthLOX = 1
PipeLengthEthanol = 1

# Specify the density of the fluids (kg/m^3)
DensityLOX = 1141
DensityEthanol = 784
'''
Please double check ethanol density as I don't now the operating temperature
'''

# Specify the pipe roughness coefficient (m)
Roughness = 0.0642 * 10 ** (-6)

# Specify an initial guess for the internal pipe diameter (m)
DiameterGuess = 0.005

def Velocity(FlowRate, Diameter):
    '''
    Determines the mean velocity of a fluid in a pipe depending on it's diameter and flowrate

    Parameters
    ----------
        Flowrate    :   The volumetric flowrate of the fluid through the pipe (in meters cubed per second).
        Diameter    :   The internal pipe diameter for which the fluid flows through (in meters).

    Return
    ------
        Velocity    :   The mean velocity of the fluid flowing through the pipe (in meters per second).
    '''
    Velocity = 4 * FlowRate / (pi * (Diameter ** 2))
    return Velocity

def ReynoldsNumber(Density, Length, Viscosity, Flowrate, Diameter):
    '''
    Determines the reynolds number for a flow of specified parameters.

    Parameters
    ----------
        Density         :   The density of the fluid flowing through the pipe (in kilograms per cubic meters).
        Length          :   Length of the straight circular pipe across which the pressure drop occurs (in meters).
        Viscocity       :   The dynamics viscocity of the fluid flowing through the pipe (in pascal seconds). Keep in mind the viscoity changes with temperature.
        Flowrate        :   The volumetric flowrate of the fluid through the pipe (in meters cubed per second).
        Diameter        :   The internal pipe diameter for which the fluid flows through (in meters).

    
    Return
    ------
        Reynolds Number :   The reynolds number for the specified flow (dimensionless).
    '''
    velocity = Velocity(Flowrate, Diameter)
    ReynoldsNumber = Density * Length  * velocity / Viscosity
    return ReynoldsNumber

@np.vectorize
def SolveColebrook(Roughness, Diameter, Density, Length, Viscosity, Flowrate):
    """
    Solves the Colebrook equation for the friction factor.

    Parameters
    ----------
        Roughness       :   The pipe roughness (in meters).
        Diameter        :   The internal pipe diameter for which the fluid flows through (in meters).
        Density         :   The density of the fluid flowing through the pipe (in kilograms per cubic meters).
        Length          :   Length of the straight circular pipe across which the pressure drop occurs (in meters).
        Viscocity       :   The dynamics viscocity of the fluid flowing through the pipe (in pascal seconds). Keep in mind the viscoity changes with temperature.
        Flowrate        :   The volumetric flowrate of the fluid through the pipe (in meters cubed per second).

    Return
    ------
        Darcy Friction Factor   :   The Darcy friction factor for the specified pipe (dimensionless)

    """
    def Colebrook(f):
        return 1/sqrt(f) + 2*log10((Roughness / Diameter)/3.7 + 2.51/(ReynoldsNumber(Density, Length, Viscosity, Flowrate, Diameter)*sqrt(f)))
    return brentq(Colebrook, 0.005, 0.1)

def PipeDiameter(Length, PressureDrop, Viscosity, Flowrate, Density, Roughness, DiameterG):
    '''
    Uses the a rearranged Darcy-Weisbach equation to solve the pipediameter for a laminar flow of given diameters. The Darcy friction fraction has already been substituted for a circular pipe diameter.
    
    Parameters
    ----------
        Length          :   Length of the straight circular pipe across which the pressure drop occurs (in meters).
        PressureDrop    :   The change in pressure that occurs between the two ends of the straight circular pipe (in pascals).
        Viscocity       :   The dynamics viscocity of the fluid flowing through the pipe (in pascal seconds). Keep in mind the viscoity changes with temperature.
        Flowrate        :   The volumetric flowrate of the fluid through the pipe (in meters cubed per second).
        Density         :   The density of the fluid flowing through the pipe (in kilograms per cubic meters).
        Roughness       :   The pipe roughness (in meters).
        DiameterG       :   A guess for the internal pipe diameter for which the fluid flows through (in meters).
    
    Return
    ------
        PipeDiameter        :   The diameter for the pipe that allows a fluid to flow through it in a way that matches the specified parameters (in meters).
    '''
    Diameter = ((SolveColebrook(Roughness, DiameterG, Density, Length, Viscosity, Flowrate)) * 8 * Density * Length * Flowrate ** 2 / (pi ** 2 * PressureDrop)) ** 0.2
    return Diameter 

DiameterLOX = PipeDiameter(PipeLengthLOX, PressureDropLOX, DynamicViscosityLOX, FlowRateLOX, DensityLOX, Roughness, DiameterGuess)
DiameterEthanol = PipeDiameter(PipeLengthEthanol, PressureDropEthanol, DynamicViscosityEthanol, FlowRateEthanol, DensityEthanol, Roughness, DiameterGuess)

while abs(DiameterLOX - DiameterGuess) > 0.0001:
    DiffLOX1 = abs(DiameterLOX - DiameterGuess)
    DiameterGuess += 0.00005
    DiffLOX2 = abs(DiameterLOX - DiameterGuess)
    if DiffLOX2 < DiffLOX1:
        continue
    else:
        DiameterGuess -= 0.0001
else: 
    print('To avoid bottlenecks the LOX pipe diameter must be greater than ', round((DiameterLOX * 1000), 2), 'mm.')

while abs(DiameterEthanol - DiameterGuess) > 0.0001:
    DiffEthanol1 = abs(DiameterEthanol - DiameterGuess)
    DiameterGuess += 0.00005
    DiffEthanol2 = abs(DiameterEthanol - DiameterGuess)
    if DiffEthanol2 < DiffEthanol1:
        continue
    else:
        DiameterGuess -= 0.0001
else: 
    print('To avoid bottlenecks the Ethanol pipe diameter must be greater than ', round((DiameterEthanol * 1000), 2), 'mm.')
