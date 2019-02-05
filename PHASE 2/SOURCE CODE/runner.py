
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci
# the port used for communicating with your sumo instance
PORT = 8876


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1. / 30
    pEW = 1. / 31
    pNS = 1. / 30
    
    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" vClass="emergency" guiShape="emergency"/>
        <vType id="typeNS1" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" />
        <route id="right" edges="51o 1i 2o 52i" />
        <route id="right1" edges="54o 4i 3o 53i" />

        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />""", file=routes)
        lastVeh = 0
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,1,1" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="down_%i" type="typeNS1" route="right1" depart="%i"  />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i

        print("</routes>", file=routes)



def run():
    i=0
    """execute the TraCI control loop"""
    traci.init(PORT)
    step = 0
    edge_id=traci.inductionloop.getIDList();
    # we start with phase 2 where EW has green
    traci.trafficlights.setPhase("0", 2)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.trafficlights.getPhase("0") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("0") > 0:#gets number of vehicles in the loop
		#print(traci.inductionloop.getLastStepVehicleNumber("0"))
             if traci.inductionloop.getLastStepOccupancy("0") == 100.0:#if no of vehicles exceed the detector area then give green signal for NS
  		           traci.trafficlights.setPhase("0", 3) #set green signal for the NS path
			   print(traci.inductionloop.getLastStepOccupancy("0"))  
	     else:             
		for i in xrange(1):
	         	vehicle_Ids=traci.inductionloop.getLastStepVehicleIDs(edge_id[i])
		        for vehicle in vehicle_Ids:
                           typeID=traci.vehicle.getTypeID(vehicle)
                           print (typeID)
	        if typeID=="typeNS":	#checks the type of the vehicle        
	           # there is a emergency vehicle from the north, switch 
                   traci.trafficlights.setPhase("0", 3)#set green signal for the NS path
		
                else:
                   # otherwise try to keep green for EW
                   traci.trafficlights.setPhase("0", 2)#green 0 for EW 
 
            else:
                # otherwise try to keep green for EW
                traci.trafficlights.setPhase("0", 2)#green 0 for EW 
        step += 1
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "data/cross.sumocfg", "--tripinfo-output",
                                    "tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)
    run()
    sumoProcess.wait()
