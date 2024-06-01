from operator import le
import os, sys
from random import random
import random
import json
import matplotlib.pyplot as plt 
import numpy as np
import EV_Charge as EVC
import RouteGenerator as RG
import xml.etree.ElementTree as ET

from turtle import clear
if 'SUMO_HOME' in os.environ:
   tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
   sys.path.append(tools)
else:
   sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# sumoCmd = [["sumo", "-c", "TestVan.sumocfg"]]
sumoCmd = [["sumo-gui", "-c", "TestVan.sumocfg"]]

routesJSON = ['RoutesJSON/DE_520001_Route.json', 'RoutesJSON/DE_520002_Route.json', 'RoutesJSON/DE_520010_Route.json']
fleetRoutes = RG.DeliveryRoutes(routesJSON)

nameJSON = ['C1Route']

norm = ["Energy/unknown"] # Energy/unknown --> https://sumo.dlr.de/docs/Models/Electric.html
norms = ['EV']

acceleration = [2.0, 3.0, 4.0]
stopsRate = [0] # 0.35 is used for peak-off and 0.65 is used for rush hours
stopsRates = ['0.0']
eightAM = 28800
midday = 43200
twoPM = 50400
sixPM = 64800
midnight = 86400

def defineStops(stopsRate, deliveryRoute):
   for j in range(len(deliveryRoute)):
      R = random.random()
      if R < stopsRate:
         stopTime = random.randint(3, 60)
         traci.vehicle.setStop(vehicleNames[0], deliveryRoute[j], 0.1, 0, stopTime, 0, 0.0, 2.0)

def RoutesManagement(vehicleNames, minimumDoD, deliverySuccess, deliveryStops):
   for i in range(len(vehicleNames)):
            actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
            maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
            stop = EVC.EVCharge(actualBatteryCapacity, minimumBatteryCapacity=maximumBatteryCapacity*minimumDoD)
            currentRoute = fleetRoutes[vehicleNames[i]][deliverySuccess[i]-1][1] # current route to vehicle i defined by tow edges
            if traci.vehicle.getRoadID(vehicleNames[i]) == currentRoute[1]: 
               if deliverySuccess[i] < deliveryStops[i]:
                  traci.vehicle.remove(vehicleNames[i])
                  currentRouteName = fleetRoutes[vehicleNames[i]][deliverySuccess[i]][0] # current route ID to vehicle i
                  currentRoute = fleetRoutes[vehicleNames[i]][deliverySuccess[i]][1] # current route to vehicle i defined by tow edges
                  traci.route.add(currentRouteName, currentRoute) 
                  traci.vehicle.add(vehicleNames[i], currentRouteName,"VAN","now")
                  deliverySuccess[i]+=1
               if traci.vehicle.getRoadID(vehicleNames[i]) == "-E0":
                  traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=2, flags=1)

def DataCalculate(route, norm_in, accel, rateOfStops):
   step = 0
   actualBatteryCapacity = 0
   maximumBatteryCapacity = 0
   vehicleNames = list(fleetRoutes.keys())
   deliverySuccess = [1] * len(vehicleNames)
   deliveryStops = [0] * len(vehicleNames)
   minimumDoD = 0.5

   traci.start(route)

   # for i in range(len(vehicleNames)):
      # initialRouteName = fleetRoutes[vehicleNames[i]][0][0] # first route ID to vehicle i
      # initialRoute = fleetRoutes[vehicleNames[i]][0][1] # first route to vehicle i defined by tow edges
      # traci.route.add(initialRouteName, initialRoute) # This route was made in VAN_Ruta.rou.xml, as well. Whatever option es possible
      # traci.vehicle.add(vehicleNames[i], initialRouteName,"VAN","now")
      # """This vehicle is added here because file.rou.xml don't give the minimum route.
      # TraCI SUMO finds the minimum route only if the route has 
      # 2 edges, depart edge and arrival edge; otherwise, SUMO gives
      # a warning and teleports the vehicle"""
      # deliveryStops[i] = len(fleetRoutes[vehicleNames[i]])
      # traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)

   # rateOfStops --> this is a number between 0 and 1. 
   # This parameter defines how many stops will be set.
   # with a high number, the number of stops will be major 
   # TraCI retrievals --> https://sumo.dlr.de/docs/TraCI.html
   # # # # # # defineStops(rateOfStops, deliveryRoute[vehicleNames[i]])
   
   while step < midnight:
      # traci.simulationStep()
      if step < eightAM:
         traci.simulationStep()
         if step == 0: 
            print('Early morning')
            initialRoute_EarlyMorning_Name = ["initial_V01", "initial_V02", "initial_V03"] # first route to vehicle i defined by tow edges
            returnRoute_EarlyMorning_Name = ["return_V01", "return_V02", "return_V03"] 
            for i in range(len(vehicleNames)):
               traci.route.add(initialRoute_EarlyMorning_Name[i], ["-E0", "E0"])
               traci.vehicle.add(vehicleNames[i], initialRoute_EarlyMorning_Name[i], "VAN", "now")
               traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)
               traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=0)
               actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
               maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
               if actualBatteryCapacity <= maximumBatteryCapacity * 0.9:
                  traci.route.add(returnRoute_EarlyMorning_Name[i], ["E0", "-E0"])
                  traci.vehicle.add(vehicleNames[i], returnRoute_EarlyMorning_Name[i], "VAN", "now")
                  traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=2, flags=1)
      elif step >= eightAM and step < midday: 
         traci.simulationStep()
         if step == eightAM: 
            print('Morning')
            for i in range(len(vehicleNames)):
               traci.vehicle.remove(vehicleNames[i])
               initialRouteName = fleetRoutes[vehicleNames[i]][0][0] # first route ID to vehicle i
               initialRoute = fleetRoutes[vehicleNames[i]][0][1] # first route to vehicle i defined by tow edges
               traci.route.add(initialRouteName, initialRoute) # This route was made in VAN_Ruta.rou.xml, as well. Whatever option es possible
               traci.vehicle.add(vehicleNames[i], initialRouteName,"VAN","now")
               """This vehicle is added here because file.rou.xml don't give the minimum route.
               TraCI SUMO finds the minimum route only if the route has 
               2 edges, depart edge and arrival edge; otherwise, SUMO gives
               a warning and teleports the vehicle"""
               deliveryStops[i] = len(fleetRoutes[vehicleNames[i]])
         RoutesManagement(vehicleNames, minimumDoD, deliverySuccess, deliveryStops)
         # vehicles = traci.vehicle.getIDList()
      elif step >= midday and step < twoPM:
         traci.simulationStep()
         if step == midday: print('Lunch')
      elif step >= twoPM and step < sixPM:
         traci.simulationStep()
         if step == twoPM: print('Afternoon')
      elif step >= sixPM:
         traci.simulationStep()
         if step == sixPM: print('Night')
      step += 1
   traci.close()
   print(step)
   results = {
      'ActualBatteryCapacity': actualBatteryCapacity/1e3, # in [Kwh]
   }
   return results

# root = ET.parse("Battery.out.xml")
# root_node = root.getroot()

total = {}

for j in range(len(stopsRate)):
   fuelRoute = []
   Routes = {}
   for i in range(len(sumoCmd)):
      fuelNorm = []
      Norms = {}
      for k in range(len(norm)):
         outResults = DataCalculate(sumoCmd[i], norm[k], acceleration[1], stopsRate[j])
         Norms[norms[k]] = outResults
      fuelRoute.append(fuelNorm)
      Routes[nameJSON[i]] = Norms
   total[stopsRates[j]] = Routes

   with open('TotalResults.json', 'w') as outfile:
      json.dump(total, outfile)
