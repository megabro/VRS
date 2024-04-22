# VOID Rocket Simulations

## Scripts
- CGCalc.ipynb - Calculate shifting of CG within tanks due to depletion.
- Pipe Diameter.py - Pipe diameter calculations.
- project25enginecalc.ipynb - Calculations regarding the engine.

## RocketPy
- Easier to automate and combine with the rest of our scripts.

## OpenRocket
- Interface with OpenRocket to change CG and mass during simulation.
  - Changing CG using the RockSim file-format: http://wiki.openrocket.info/RSE_File (Should really test if this even affects the simulation)
  - Simulation listeners or `orhelper`

- Engine altitude compensation
  - This could done by iteratively simulating the flight, then updating the thrust curve to match altitude data from sim. Do this a couple times for the altitude plot to converge. `See ORLEG.`
  - Is this needed for 3km?

- Other OpenRocket projects:
  - Multi-level wind simulation (maybe it's in OpenRocket stock now?):
    - https://github.com/rocketsam2016/MultiLevelWind
  - https://notebook.community/psas/liquid-engine-analysis/Simulation_and_Optimization/openrocket_interface
  - https://github.com/bkuker/dispersion/tree/master/src