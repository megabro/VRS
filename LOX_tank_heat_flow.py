from math import pi

'''
This code approximates the heatflow through different
mediums surrounding the air in the fuel/oxidizer tank. The
following assumptions have been made:
  -   surface area of the internal/external fuel/oxidizer
      tank/insulation is identical
  -   the heat flow conducts through the tank and insulation
      and convects into air.
  -   tempSurroundings = tempInitial (in the case of initial
      pressurization)
 The temperature boundaries are as follows:
  -   temp1 inside the tank (K)
  -   temp2 between the tank and insulation (K)
  -   temp3 on the external side of the insulation (K)
  -   tempSurrounding is temperature of the surroundings (K)
'''

# Constants
tempSurrounding = 303  # temperature of air surrounding the 
                       # fuel/oxidizer tank/insulation (K)
temp1 = 90  # temperature of the fuel/oxidizer tank (K)
diameterTank = 0.15  # diameter of the tank (m)
lengthTank = 0.4  # length of cylindrical tank sidewall (m)
roundEndCaps = 'no'  # 'yes' or 'no' for round tank end caps

# Surface area calculation
if roundEndCaps == 'no':
    # Surface area calculation for cylindrical tank with flat end caps
    cylinder = (2 * pi * (diameterTank / 2) * lengthTank + 
               2 * pi * (diameterTank / 2)**2)
else:
    # Surface area calculation for cylindrical tank with 
    # rounded hemispherical end caps
    cylinder = (2 * pi * (diameterTank / 2) * lengthTank + 
               4 * pi * (diameterTank / 2)**2)

surfaceArea = cylinder  # surface area of the fuel/oxidizer 
                        # tank/insulation (m^2)

# Coefficients and thicknesses
kTank = 14.4  # fuel/oxidizer tanks conduction coefficient (W/(m*K))
kIns = 0.016  # fuel/oxidizer tank insulations conduction coefficient (W/(m*K))
xTank = 0.003  # fuel/oxidizer tank thickness (m)
xIns = 0.002  # fuel/oxidizer tank insulation thickness (m)
hAir = 20.83  # convection coefficient of air (W/(m^2*K))

# Temperature calculations
temp3 = ((hAir * tempSurrounding + temp1 * (kTank / xTank) * 
          (kTank / xTank - 1)) / 
         (hAir - (kTank * kIns) / (xTank * xIns)))

temp2 = temp3 * (kIns / xIns) + temp1 * (kTank / xTank)

# Heat flow calculation
heatFlow = (kTank * (temp2 - temp1)) / xTank

# Output
print('The heat flow with the chosen insulation is:', round(heatFlow, 0), 'W')
