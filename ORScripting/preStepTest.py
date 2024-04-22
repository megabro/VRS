import os

import numpy as np
from matplotlib import pyplot as plt

import orhelper
import jpype
from orhelper import FlightDataType, FlightEvent

class MyPreStep(orhelper.AbstractSimulationListener):
    def startSimulation(self, status) -> None:
        print("startSim")
#        coord = jpype.JPackage("net").sf.openrocket.util.Coordinate(0.0, 0.0, 100.0)
#        status.setRocketPosition(coord)
        pass
    
    def endSimulation(self, status, simulation_exception) -> None:
        print("endSim")
        pass

    def preStep(self, status) -> bool:
        coord = jpype.JPackage("net").sf.openrocket.util.Coordinate(0.0, 0.0, 0.0)
        status.setRocketVelocity(coord)
        status.setRocketAcceleration(coord)
        
        print(status.getRocketPosition())
        return True

with orhelper.OpenRocketInstance() as instance:
    orh = orhelper.Helper(instance)

    # Load document, run simulation and get data and events

    testing = [MyPreStep()]
    doc = orh.load_doc(os.path.join('examples', 'simple.ork'))
    sim = doc.getSimulation(0)
    orh.run_simulation(sim, testing)
    data = orh.get_timeseries(sim, [FlightDataType.TYPE_TIME, FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_VELOCITY_Z])
    events = orh.get_events(sim)

    # Make a custom plot of the simulation

    events_to_annotate = {
        FlightEvent.BURNOUT: 'Motor burnout',
        FlightEvent.APOGEE: 'Apogee',
        FlightEvent.LAUNCHROD: 'Launch rod clearance'
    }

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    ax1.plot(data[FlightDataType.TYPE_TIME], data[FlightDataType.TYPE_ALTITUDE], 'b-')
    ax2.plot(data[FlightDataType.TYPE_TIME], data[FlightDataType.TYPE_VELOCITY_Z], 'r-')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Altitude (m)', color='b')
    ax2.set_ylabel('Vertical Velocity (m/s)', color='r')
    change_color = lambda ax, col: [x.set_color(col) for x in ax.get_yticklabels()]
    change_color(ax1, 'b')
    change_color(ax2, 'r')

    index_at = lambda t: (np.abs(data[FlightDataType.TYPE_TIME] - t)).argmin()
    for event, times in events.items():
        if event not in events_to_annotate:
            continue
        for time in times:
            ax1.annotate(events_to_annotate[event], xy=(time, data[FlightDataType.TYPE_ALTITUDE][index_at(time)]),
                         xycoords='data', xytext=(20, 0), textcoords='offset points',
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    ax1.grid(True)

# Leave OpenRocketInstance context before showing plot in order to shutdown JVM first
plt.show()
