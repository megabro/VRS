# Formula to Calculate the Optimal Pipe Diameter for the Fuel Lines

from math import pi
# Flow rate of fluid (m^3 / s)
FlowRateLOX = 0.6/1000
FlowRateEthanol = 0.4/1000

# Dynamic Viscocity of fluid (Pa s) at respective flow temperature
DynamicViscosityLOX = 
DynamicViscosityEthanol =

# Specify the acceptable Pressure Drop (Pa)
PressureDropLOX = 
PressureDropEthanol = 

# Specify the length of the Pipe (m)
PipeLengthLOX = 
PipeLengthEthanol = 

def PipeDiameter(Length, PressureDrop, Viscosity, Flowrate):
    '''
    Uses the a rearranged Darcy-Weisbach equation to solve the pipediameter for a laminar flow of given diameters. The Darcy friction fraction has already been substituted for a circular pipe diameter.
    
    Parameters
    ----------
        Length          :   Length of the straight circular pipe across which the pressure drop occurs (in meters).
        Pressure Drop   :   The change in pressure that occurs between the two ends of the straight circular pipe (in pascals).
        Viscocity       :   The dynamics viscocity of the fluid flowing through the pipe (in pascal seconds). Keep in mind the viscoity changes with temperature.
        Flowrate        :   The volumetric flowrate of the fluid through the pipe (in meters cubed per second).
    
    Return
    ------
        Diameter        :   The diameter for the pipe that allows a fluid to flow through it in a way that matches the specified parameters (in meters).
    '''
    Diameter = (128 * Length * Viscosity * Flowrate / (pi * PressureDrop)) ** 0.25
    return Diameter 

DiameterLOX = PipeDiameter(PipeLengthLOX, PressureDropLOX, DynamicViscosityLOX, FlowRateLOX)
DiameterEthanol = PipeDiameter(PipeLengthEthanol, PressureDropEthanol, DynamicViscosityEthanol, FlowRateEthanol)

print("The optimal diameter for the LOX piping is ", DiameterLOX, " meters.")
print("The optimal diameter for the ethanol piping is ", DiameterEthanol, " meters.")