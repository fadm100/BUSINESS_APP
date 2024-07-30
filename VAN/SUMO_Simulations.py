from operator import le
import os, sys
from random import random
import random
import json
import matplotlib.pyplot as plt 
import numpy as np
import EV_Charge as EVC
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

nameJSON = ['C1Route']

norm = "MMPEVEM" # --> https://sumo.dlr.de/docs/Models/MMPEVEM.html
norms = ['EV']

acceleration = [2.0, 3.0, 4.0]
stopsRate = 0 # 0.35 is used for peak-off and 0.65 is used for rush hours
stopsRates = ['0.0']

eightAM = 28800
midday = 43200
twoPM = 50400
sixPM = 64800
midnight = 86400
simulationDays = 5

actualBatteryCapacity = 0
maximumBatteryCapacity = 0
# keep battery level between 20% and 80% --> https://v2charge.com/es/carga-completa-coche-electrico/
maximumCharge = 0.8 
maximumDoD = 0.8

def defineStops(stopsRate, deliveryRoute):
   for j in range(len(deliveryRoute)):
      R = random.random()
      if R < stopsRate:
         stopTime = random.randint(3, 60)
         traci.vehicle.setStop(vehicleNames[0], deliveryRoute[j], 0.1, 0, stopTime, 0, 0.0, 2.0)

def RoutesManagement(step, Day, norm_in, chargeFlag, fleetRoutes, maximumDoD, deliverySuccess, deliveryStops, hour):

   vehicleNames = list(fleetRoutes.keys())
   for i in range(len(vehicleNames)):
      if step == 0 and Day < 2: 
         # batteryFull.append(False)
         traci.vehicle.add(vehicleNames[i], "ParkingReturn", "VAN", "now")
         traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)
         # traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=1)
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=1)
      elif step == hour and step != 0 and step != midday: 
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=0)
         traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][deliverySuccess[i]])
         deliveryStops[i] = len(fleetRoutes[vehicleNames[i]])-1
      elif traci.vehicle.getRoadID(vehicleNames[i]) == fleetRoutes[vehicleNames[i]][deliverySuccess[i]]: 
         if deliverySuccess[i] < deliveryStops[i]:
            deliverySuccess[i]+=1
            traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][deliverySuccess[i]])
         if traci.vehicle.getRoadID(vehicleNames[i]) == "-E0":
            traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)
      actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
      maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
      chargeStop = True if actualBatteryCapacity < maximumBatteryCapacity * (1-maximumDoD) else False #EVC.EVCharge(actualBatteryCapacity, minimumBatteryCapacity=maximumBatteryCapacity*(1-maximumDoD))
      batteryFull = True if actualBatteryCapacity > maximumBatteryCapacity * maximumCharge else False
      if chargeStop and (traci.vehicle.getRoadID(vehicleNames[i]) == "-E0" or traci.vehicle.isStoppedParking(vehicleNames[i]) == True) and chargeFlag[i] == 0: #and actualBatteryCapacity >= maximumBatteryCapacity * maximumCharge:
         chargeFlag[i] = 1
         traci.vehicle.changeTarget(vehicleNames[i], "E0")
         traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=midnight, until=midnight, flags=chargeFlag[i])
         # batteryFull[i] = True
      elif batteryFull and chargeFlag[i] == 1:
         chargeFlag[i] = 0
         traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=chargeFlag[i])
         traci.vehicle.changeTarget(vehicleNames[i], "-E0")
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)

def DataCalculate(route, norm_in, rateOfStops):
   '''rateOfStops --> this is a number between 0 and 1. 
   This parameter defines how many stops will be set.
   with a high number, the number of stops will be major'''
   
   # batteryFull = [False] * len(morningRoutesJSON)
   chargeFlag = [0] * len(morningRoutesJSON)
   fleetRoutesAM = fleetRetrieval('AM')
   fleetRoutesPM = fleetRetrieval('PM')
   vehicleNames = list(fleetRoutesAM.keys())
   step = 0
   Day = 1
   
   deliverySuccess = []
   deliveryStops = []

   traci.start(route)
   # defineStops(rateOfStops, deliveryRoute[vehicleNames[i]])
   
   while step < midnight and Day <= simulationDays:
      if step < eightAM:
         traci.simulationStep()
         if step == 0: 
            print('Day = ', Day)
            print('Early morning')
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, Day, norm_in, chargeFlag, fleetRoutesAM, maximumDoD, deliverySuccess, deliveryStops, 0)
      elif step >= eightAM and step < midday: 
         traci.simulationStep()
         if step == eightAM: 
            print('Morning')
            deliverySuccess = []
            deliveryStops = []
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, Day, norm_in, chargeFlag, fleetRoutesAM, maximumDoD, deliverySuccess, deliveryStops, eightAM)
      elif step >= midday and step < twoPM:
         traci.simulationStep()
         if step == midday: 
            print('Lunch')

      elif step >= twoPM and step < sixPM:
         traci.simulationStep()
         if step == twoPM: 
            print('Afternoon')
            deliverySuccess = []
            deliveryStops = []
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, Day, norm_in, chargeFlag, fleetRoutesPM, maximumDoD, deliverySuccess, deliveryStops, twoPM)
      elif step >= sixPM:
         traci.simulationStep()
         if step == sixPM: print('Night')
      
      step += 1
      if step >= midnight-1:
         if Day < simulationDays:
            step = 0
            Day = Day + 1        

   traci.close()
   print("Step = ", step, "; Day = ", Day)

DataCalculate(sumoCmd, norm, stopsRate)

file = 'MorningRoutesJSON/TotalRoutes.json'
os.remove(file)
file = 'AfternoonRoutesJSON/TotalRoutes.json'
os.remove(file)
