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
import os.path as path

from turtle import clear
if 'SUMO_HOME' in os.environ:
   tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
   sys.path.append(tools)
else:
   sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# sumoCmd = [["sumo", "-c", "TestVan.sumocfg"]]
sumoCmd = [["sumo-gui", "-c", "TestVan.sumocfg"]]

morningRoutesJSON = ['MorningRoutesJSON/DE_520001_Route.json', 'MorningRoutesJSON/DE_520002_Route.json', 'MorningRoutesJSON/DE_520010_Route.json']
afternoonRoutesJSON = ['AfternoonRoutesJSON/DE_520001_Route.json', 'AfternoonRoutesJSON/DE_520002_Route.json', 'AfternoonRoutesJSON/DE_520010_Route.json']

def fleetRetrieval(session):
   if session == 'AM':
      directory = 'MorningRoutesJSON/TotalRoutes.json'
   else:
      directory = 'AfternoonRoutesJSON/TotalRoutes.json'
   if not path.exists(directory):
      fleetRoutes = RG.DeliveryRoutes(morningRoutesJSON, session)
   else:
      with open(directory) as json_file:
         fleetRoutes = json.load(json_file)
   '''fleetRoutes was created or loaded'''
   return fleetRoutes




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

def RoutesManagement(step, vehicleNames, maximumDoD, deliverySuccess, deliveryStops, hour):
   if hour < midday:
      fleetRoutes = fleetRetrieval('AM')
   else:
      fleetRoutes = fleetRetrieval('PM')
   if step == hour: 
      for i in range(len(vehicleNames)):
         # traci.vehicle.remove(vehicleNames[i])
         initialRouteName = fleetRoutes[vehicleNames[i]][0][0] # first route ID to vehicle i
         initialRoute = fleetRoutes[vehicleNames[i]][0][1] # first route to vehicle i defined by tow edges
         # traci.route.add(initialRouteName, initialRoute) # This route was made in VAN_Ruta.rou.xml, as well. Whatever option es possible
         # traci.vehicle.add(vehicleNames[i], initialRouteName,"VAN","now")
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=0)
         traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][1])
         """This vehicle is added here because file.rou.xml don't give the minimum route.
               TraCI SUMO finds the minimum route only if the route has 
               2 edges, depart edge and arrival edge; otherwise, SUMO gives
               a warning and teleports the vehicle"""
         deliveryStops[i] = len(fleetRoutes[vehicleNames[i]])
   else:
      for i in range(len(vehicleNames)):
         actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
         maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
         stop = EVC.EVCharge(actualBatteryCapacity, minimumBatteryCapacity=maximumBatteryCapacity*maximumDoD)
         currentRoute = fleetRoutes[vehicleNames[i]][deliverySuccess[i]-1][1] # current destination of the vehicle i 
         if traci.vehicle.getRoadID(vehicleNames[i]) == fleetRoutes[vehicleNames[i]][deliverySuccess[i]]: 
            if deliverySuccess[i] < deliveryStops[i]:
               # traci.vehicle.remove(vehicleNames[i])
               currentRouteName = fleetRoutes[vehicleNames[i]][deliverySuccess[i]][0] # current route ID to vehicle i
               currentRoute = fleetRoutes[vehicleNames[i]][deliverySuccess[i]][1] # current route to vehicle i defined by tow edges
               # traci.route.add(currentRouteName, currentRoute) 
               # traci.vehicle.add(vehicleNames[i], currentRouteName,"VAN","now")
               traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][0])
               deliverySuccess[i]+=1
            if traci.vehicle.getRoadID(vehicleNames[i]) == "-E0":
               traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=2, flags=1)

def DataCalculate(route, norm_in, accel, rateOfStops):
   '''rateOfStops --> this is a number between 0 and 1. 
   This parameter defines how many stops will be set.
   with a high number, the number of stops will be major'''
   step = 0
   actualBatteryCapacity = 0
   maximumBatteryCapacity = 0
   fleetRoutes = fleetRetrieval('AM')
   vehicleNames = list(fleetRoutes.keys())
   deliverySuccess = [1] * len(vehicleNames)
   deliveryStops = [0] * len(vehicleNames)
   maximumCharge = 0.9
   maximumDoD = 0.5
   batteryFull = []

   traci.start(route)
   # defineStops(rateOfStops, deliveryRoute[vehicleNames[i]])
   
   while step < midnight:
      if step < eightAM:
         traci.simulationStep()
         for i in range(len(vehicleNames)):
            if step == 0: 
               print('Early morning')
               batteryFull.append(False)
               traci.vehicle.add(vehicleNames[i], "ToCharging", "VAN", "now")
               traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)
               traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=1)
            actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
            maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
            if not batteryFull[i] and actualBatteryCapacity >= maximumBatteryCapacity * maximumCharge:
               batteryFull[i] = True
               traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=0)
               traci.vehicle.changeTarget(vehicleNames[i], "-E0")
               traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=1)
      elif step >= eightAM and step < midday: 
         traci.simulationStep()
         if step == eightAM: print('Morning')
         RoutesManagement(step, vehicleNames, maximumDoD, deliverySuccess, deliveryStops, eightAM)
      elif step >= midday and step < twoPM:
         traci.simulationStep()
         if step == midday: print('Lunch')
         for i in range(len(vehicleNames)):
            if traci.vehicle.isStoppedParking(vehicleNames[i]) == True:
               traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=twoPM-midday, until=sixPM, flags=1)
      elif step >= twoPM and step < sixPM:
         traci.simulationStep()
         if step == twoPM: 
            print('Afternoon')
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, vehicleNames, maximumDoD, deliverySuccess, deliveryStops, twoPM)
      elif step >= sixPM:
         traci.simulationStep()
         if step == sixPM: print('Night')
      step += 1
      # print(step)
      # print(traci.simulation.getTime())
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
