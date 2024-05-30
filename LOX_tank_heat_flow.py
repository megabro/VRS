from math import pi

# Tank info
tempSurrounding = 303  # temperature of air surrounding the fuel/oxidizer
                       # tank/insulation (K)
tempTank = 90  # temperature of the oxidizer tank (K)
tempBoilOffLOX = 90  # temperature of evaporation for LOX (K)
diameterTank = 0.1  # diameter of the tank (m)
lengthTank = 0.45  # length of cylindrical tank sidewall (m)
roundEndCaps = 'no'  # 'yes' or 'no' for round tank end caps
thicknessTank = 0.003  # thickness of tank walls (m)

# MLI info
numLayers = 35  # number of MLI layers
layerDensity = 14  # number of MLI layers per cm
emissivity = 0.01  # effective emittance between 0.05 & 0.007

# Surface area calculation
if roundEndCaps == 'no':
    # Surface area calculation for cylindrical tank with flat end caps
    cylinder = (2 * pi * (diameterTank / 2) * lengthTank +
                2 * pi * (diameterTank / 2) ** 2)
else:
    # Surface area calculation for cylindrical tank with rounded
    # hemispherical end caps
    cylinder = (2 * pi * (diameterTank / 2) * lengthTank +
                4 * pi * (diameterTank / 2) ** 2)

surfaceArea = cylinder  # surface area of the fuel/oxidizer tank/insulation (m^2)

# Volume calculation
if roundEndCaps == 'no':
    # Volume calculation for cylindrical tank with flat end caps
    cylinderVol = pi * (diameterTank / 2) ** 2 * lengthTank
else:
    # Volume calculation for cylindrical tank with rounded
    # hemispherical end caps
    cylinderVol = (pi * (diameterTank / 2) ** 2 * lengthTank +
                   (4 / 3) * pi * (diameterTank / 2) ** 3)

surfaceArea = cylinder  # surface area of the fuel/oxidizer tank/insulation (m^2)
volume = cylinderVol  # volume of the fuel/oxidizer tank/insulation (m^3)

def lockheedMliHeatTransfer(area, emissivity, tempLow, tempHigh, numLayers, 
                            layerDensity):
    """
    Calculate the total heat flux through multi-layer insulation (MLI)
    using the Lockheed MLI equation including both radiative and
    conductive components.

    Parameters:
    - area (float): surface area of the MLI insulation (m^2)
    - emissivity (float): The MLI shield emissivity of.
    - tempLow (float): Temperature of one surface (K).
    - tempHigh (float): Temperature of the other surface (K).
    - numLayers (int): Number of MLI layers.
    - layerDensity (float): MLI layer density (layers/cm).

    Returns:
    - totalHeatTransfer (float): Total heat transfer rate (W).
    """

    tempMean = (tempHigh + tempLow) / 2

    # Radiation constant
    radiationConstant = 5.39e-7

    # Conduction constant
    conductionConstant = 8.95e-5

    # Radiative heat flux (mW/m^2)
    radiativeHeatFlux = (emissivity * radiationConstant * 
                         (tempHigh ** 4.67 - tempLow ** 4.67)) / numLayers

    # Conductive heat flux (mW/m^2)
    conductiveHeatFlux = (conductionConstant * tempMean * 
                          layerDensity ** 2.56 * (tempHigh - tempLow)) / numLayers

    # Total heat flux (mW/m^2)
    totalHeatFlux = radiativeHeatFlux + conductiveHeatFlux

    # Total heat transfer (W)
    totalHeatTransfer = totalHeatFlux * area * 1000

    return totalHeatTransfer

heatTransfer = lockheedMliHeatTransfer(surfaceArea, emissivity, tempTank, 
                                       tempSurrounding, numLayers, layerDensity)
print(f'The total heat transfer through the MLI is: {heatTransfer:.0f} W')

# The temperature difference across the steel LOX tank is assumed to be 0K
# (this predicts a pessimistic heat transfer).

# Specific heat capacities and density (depend on temperatures!!!)
specificHeatCapacityLOX = 918  # (J/kg K)
specificHeatCapacitySteel = 420  # (J/kg K)
latentHeatCapacityLOX = 214e3  # (J/kg)
densityLOX = 1141  # (kg/m^3)
densitySteel = 8000  # (kg/m^3)

# Time since fueling (s)
time = 10

# Latent and specific heat transfer (J)
energyTempIncrease = (tempBoilOffLOX - tempTank) * (
    volume * specificHeatCapacityLOX * densityLOX + 
    surfaceArea * thicknessTank * specificHeatCapacitySteel * densitySteel)
heatTransferLatent = heatTransfer * time - energyTempIncrease

# Mass of boiled off LOX
massBoilOff = heatTransferLatent / latentHeatCapacityLOX

# Results
if (tempBoilOffLOX - tempTank) > 0:
    tempIncrease = tempBoilOffLOX - tempTank
    print(f'In the {time} seconds between filling the LOX and takeoff, the '
          f'LOX temperature rises by {tempIncrease:.1f} K which puts the final '
          f'temperature at {tempIncrease + tempTank} K')
else:
    print(f'The LOX remains constant for the {time} seconds after fueling '
          f'however {massBoilOff:.3f} kg of LOX boil off.')
