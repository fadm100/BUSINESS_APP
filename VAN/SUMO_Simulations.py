from operator import le
import os, sys
from random import random
import random
import json
import matplotlib.pyplot as plt 
import numpy as np
import RouteGenerator as RG
import os.path as path
from random import sample

from turtle import clear
if 'SUMO_HOME' in os.environ:
   tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
   sys.path.append(tools)
else:
   sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

sumoCmd = ["sumo", "-c", "TestVan.sumocfg"]
# sumoCmd = ["sumo-gui", "-c", "TestVan.sumocfg"]

morningRoutesJSON = ['MorningRoutesJSON/DE_520001_Route.json', 'MorningRoutesJSON/DE_520002_Route.json', 'MorningRoutesJSON/DE_520003_Route.json',
                     'MorningRoutesJSON/DE_520004_Route.json', 'MorningRoutesJSON/DE_520006_Route.json', 'MorningRoutesJSON/DE_520010_Route.json']
afternoonRoutesJSON = ['AfternoonRoutesJSON/DE_520001_Route.json', 'AfternoonRoutesJSON/DE_520002_Route.json', 'AfternoonRoutesJSON/DE_520003_Route.json',
                     'AfternoonRoutesJSON/DE_520004_Route.json', 'AfternoonRoutesJSON/DE_520006_Route.json', 'AfternoonRoutesJSON/DE_520010_Route.json']

def fleetRetrieval(session):
   if session == 'AM':
      fleetRoutes = RG.DeliveryRoutes(morningRoutesJSON, session)
   elif session == 'PM':
      fleetRoutes = RG.DeliveryRoutes(afternoonRoutesJSON, session)
   return fleetRoutes

norm = "MMPEVEM" # --> https://sumo.dlr.de/docs/Models/MMPEVEM.html

eightAM = 28800
midday = 43200
twoPM = 50400
sixPM = 64800
midnight = 86400
simulationDays = 5

# keep battery level between 20% and 80% --> https://v2charge.com/es/carga-completa-coche-electrico/
maximumCharge = 0.8 
maximumDoD = 0.8
initialMass = 4989.5161

def VehiclesManagement(step, chargeFlag, fleetRoutes, maximumDoD, deliverySuccess, deliveryStops):

   vehicleNames = list(fleetRoutes.keys())
   for i in range(len(vehicleNames)):
      actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
      maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
      chargeStop = True if actualBatteryCapacity < maximumBatteryCapacity * (1-maximumDoD) else False 
      batteryFull = True if actualBatteryCapacity > maximumBatteryCapacity * maximumCharge else False
      if step == eightAM or step == twoPM: 
         # traci.vehicle.setParameter(vehicleNames[i], "device.battery.vehicleMass", initialMass)
         deliverySuccess[i] = 1
         deliveryStops[i] = 0
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=0)
         traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][deliverySuccess[i]])
         deliveryStops[i] = len(fleetRoutes[vehicleNames[i]])-1
         stopTime = random.randint(60, 600)
         traci.vehicle.setStop(vehicleNames[i], fleetRoutes[vehicleNames[i]][deliverySuccess[i]], 0.1, 0, stopTime, 0, 0.0, 2.0)
      elif traci.vehicle.getRoadID(vehicleNames[i]) == fleetRoutes[vehicleNames[i]][deliverySuccess[i]]: 
         if deliverySuccess[i] < deliveryStops[i]:
            deliverySuccess[i]+=1
            traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][deliverySuccess[i]])
            if fleetRoutes[vehicleNames[i]][deliverySuccess[i]] != "-E0":
               stopTime = random.randint(60, 600)
               traci.vehicle.setStop(vehicleNames[i], fleetRoutes[vehicleNames[i]][deliverySuccess[i]], 0.1, 0, stopTime, 0, 0.0, 2.0)
               # vehMass = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.vehicleMass"))
               # traci.vehicle.setParameter(vehicleNames[i], "device.battery.vehicleMass", vehMass - 50.0)
         if traci.vehicle.getRoadID(vehicleNames[i]) == "-E0" and chargeStop == False:
            traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)
      if chargeStop and traci.vehicle.getRoadID(vehicleNames[i]) == "-E0" and chargeFlag[i] == 0: 
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=0)
         chargeFlag[i] = 1
         traci.vehicle.changeTarget(vehicleNames[i], "E0")
         traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=midnight, until=midnight, flags=chargeFlag[i])
      elif batteryFull and chargeFlag[i] == 1:
         chargeFlag[i] = 0
         traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=chargeFlag[i])
         traci.vehicle.changeTarget(vehicleNames[i], "-E0")
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)

def DataCalculate(route, norm_in):
   '''rateOfStops --> this is a number between 0 and 1. 
   This parameter defines how many stops will be set.
   with a high number, the number of stops will be major'''
   
   chargeFlag = [0] * len(morningRoutesJSON)
   fleetRoutesAM = fleetRetrieval('AM')
   fleetRoutesPM = fleetRetrieval('PM')
   vehicleNames = list(fleetRoutesAM.keys())
   deliverySuccess = [1] * len(vehicleNames)
   deliveryStops = [0] * len(vehicleNames)
   step = 0
   Day = 1

   traci.start(route)
   traci.simulationStep()
   for i in range(len(vehicleNames)):
      traci.vehicle.add(vehicleNames[i], "ParkingReturn", "VAN", "now")
      traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)
      traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=1)
   
   while step < midnight and Day <= simulationDays:
      traci.simulationStep()
      fleetRoutes = fleetRoutesAM if step < midday else fleetRoutesPM

      VehiclesManagement(step, chargeFlag, fleetRoutes, maximumDoD, deliverySuccess, deliveryStops)
      
      step += 1
      if step >= midnight-1:
         if Day < simulationDays:
            step = 0
            Day = Day + 1        

   traci.close()
   print("Step = ", step, "; Day = ", Day)

DataCalculate(sumoCmd, norm)

file = 'MorningRoutesJSON/TotalRoutes.json'
os.remove(file)
file = 'AfternoonRoutesJSON/TotalRoutes.json'
os.remove(file)
