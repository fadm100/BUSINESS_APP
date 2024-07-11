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

from turtle import clear
if 'SUMO_HOME' in os.environ:
   tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
   sys.path.append(tools)
else:
   sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# sumoCmd = [["sumo", "-c", "TestVan.sumocfg"]]
sumoCmd = [["sumo-gui", "-c", "TestVan.sumocfg"]]

morningRoutesJSON = ['MorningRoutesJSON/DE_520001_Route.json', 'MorningRoutesJSON/DE_520002_Route.json', 'MorningRoutesJSON/DE_520003_Route.json',
                     'MorningRoutesJSON/DE_520004_Route.json', 'MorningRoutesJSON/DE_520006_Route.json', 'MorningRoutesJSON/DE_520010_Route.json']
afternoonRoutesJSON = ['AfternoonRoutesJSON/DE_520001_Route.json', 'AfternoonRoutesJSON/DE_520002_Route.json', 'MorningRoutesJSON/DE_520003_Route.json',
                     'MorningRoutesJSON/DE_520004_Route.json', 'MorningRoutesJSON/DE_520006_Route.json', 'MorningRoutesJSON/DE_520010_Route.json']

def fleetRetrieval(session):
   fleetRoutes = RG.DeliveryRoutes(morningRoutesJSON, session)
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


actualBatteryCapacity = 0
maximumBatteryCapacity = 0
maximumCharge = 0.9
maximumDoD = 0.5

def defineStops(stopsRate, deliveryRoute):
   for j in range(len(deliveryRoute)):
      R = random.random()
      if R < stopsRate:
         stopTime = random.randint(3, 60)
         traci.vehicle.setStop(vehicleNames[0], deliveryRoute[j], 0.1, 0, stopTime, 0, 0.0, 2.0)

def RoutesManagement(step, norm_in, batteryFull, fleetRoutes, maximumDoD, deliverySuccess, deliveryStops, hour):

   vehicleNames = list(fleetRoutes.keys())
   for i in range(len(vehicleNames)):
      if step == 0: 
         # batteryFull.append(False)
         traci.vehicle.add(vehicleNames[i], "ToCharging", "VAN", "now")
         traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)
         traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=1)
      elif step == hour: 
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
      stop = EVC.EVCharge(actualBatteryCapacity, minimumBatteryCapacity=maximumBatteryCapacity*maximumDoD)
      if not batteryFull[i] and actualBatteryCapacity >= maximumBatteryCapacity * maximumCharge:
         batteryFull[i] = True
         traci.vehicle.setChargingStationStop(vehicleNames[i], "cS_2to19_0a", duration=10.0, until=eightAM, flags=0)
         traci.vehicle.changeTarget(vehicleNames[i], "-E0")
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=1)

def Traffic(hour):
   print('# vhe = ', traci.vehicle.getIDCount())
   if hour <= 18000:
      if traci.vehicle.getIDCount() < 5000: # Add 5000 vehicles to the simulation before 5am
         print('5am-' + str(hour) + 'veh')
         traci.vehicle.add('5am-' + str(hour) + 'veh', "", "P_passenger", depart='now')
   elif hour > 18000 and hour < eightAM:
      for i in range(4): # Add 4 vehicles each second until 8am to achieve around 35000 vehicles
         traci.vehicle.add('5am+' + str(hour) + 'veh' + str(i), "", "P_passenger", depart='now')
   elif hour >= eightAM and hour < (eightAM + 7200):
      if traci.vehicle.getIDCount() < 24000: # between 8am and 10am vehicles must be more than 24000
         traci.vehicle.add('8am+' + str(hour) + 'veh', "", "P_passenger", depart='now')
   elif hour >= (eightAM + 7200) and hour < (eightAM + 10800):
      if traci.vehicle.getIDCount() < 25000:
         for i in range(2): # Add 2 vehicles each second until 11am to achieve around 25000 vehicles
            traci.vehicle.add('10am+' + str(hour) + 'veh' + str(i), "", "P_passenger", depart='now')
   elif hour >= (eightAM + 10800) and hour < (eightAM + 12600):
      if traci.vehicle.getIDCount() < 30000:
         for i in range(2): # Add 2 vehicles each second until 11:30am to achieve around 30000 vehicles
            traci.vehicle.add('11am+' + str(hour) + 'veh' + str(i), "", "P_passenger", depart='now')
   elif hour >= (eightAM + 12600) and hour < midday:
      if traci.vehicle.getIDCount() < 35000:
         for i in range(2): # Add 2 vehicles each second until 12m to achieve around 35000 vehicles
            traci.vehicle.add('11am+' + str(hour) + 'veh' + str(i), "", "P_passenger", depart='now')
   elif hour >= midday and hour < (midday + 3600):
      if traci.vehicle.getIDCount() < 28000: # between 12m and 1pm vehicles must be more than 28000
         traci.vehicle.add('12m+' + str(hour) + 'veh', "", "P_passenger", depart='now')
   elif hour >= (midday + 3600) and hour < twoPM:
      if traci.vehicle.getIDCount() < 30000:
         for i in range(2): # Add 2 vehicles each second until 2pm to achieve around 30000 vehicles
            traci.vehicle.add('1pm+' + str(hour) + 'veh' + str(i), "", "P_passenger", depart='now')
   elif hour >= twoPM and hour < sixPM:
      if traci.vehicle.getIDCount() < 24000: # between 2pm and 6pm vehicles must be more than 24000
         traci.vehicle.add('2pm+' + str(hour) + 'veh', "", "P_passenger", depart='now')

def DataCalculate(route, norm_in, accel, rateOfStops):
   '''rateOfStops --> this is a number between 0 and 1. 
   This parameter defines how many stops will be set.
   with a high number, the number of stops will be major'''
   
   batteryFull = [False] * len(morningRoutesJSON)
   fleetRoutesAM = fleetRetrieval('AM')
   fleetRoutesPM = fleetRetrieval('PM')
   vehicleNames = list(fleetRoutesAM.keys())
   step = 0
   
   #test
   totalVeh = []
   distance = 0
   deliverySuccessTot = []
   deliverySuccess = []
   deliveryStops = []
   #test

   traci.start(route)
   # defineStops(rateOfStops, deliveryRoute[vehicleNames[i]])
   
   while step < midnight:
      if step < eightAM:
         traci.simulationStep()
         if step == 0: 
            print('Early morning')
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, norm_in, batteryFull, fleetRoutesAM, maximumDoD, deliverySuccess, deliveryStops, 0)
         Traffic(step)
      elif step >= eightAM and step < midday: 
         traci.simulationStep()
         if step == eightAM: 
            print('Morning')
            deliverySuccess = []
            deliveryStops = []
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, norm_in, batteryFull, fleetRoutesAM, maximumDoD, deliverySuccess, deliveryStops, eightAM)
         Traffic(step)
      elif step >= midday and step < twoPM:
         traci.simulationStep()
         if step == midday: 
            print('Lunch')
            for i in range(len(vehicleNames)):
               if traci.vehicle.isStoppedParking(vehicleNames[i]) == True:
                  traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=twoPM-midday, until=sixPM, flags=1)
               elif traci.vehicle.getRoadID(vehicleNames[i]) == "-E0":
                  traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)
               else:
                  traci.vehicle.changeTarget(vehicleNames[i], "-E0")
                  traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)
         Traffic(step)
      elif step >= twoPM and step < sixPM:
         traci.simulationStep()
         if step == twoPM: 
            print('Afternoon')
            deliverySuccess = []
            deliveryStops = []
            deliverySuccess = [1] * len(vehicleNames)
            deliveryStops = [0] * len(vehicleNames)
         RoutesManagement(step, norm_in, batteryFull, fleetRoutesPM, maximumDoD, deliverySuccess, deliveryStops, twoPM)
         Traffic(step)
      elif step >= sixPM:
         traci.simulationStep()
         if step == sixPM: print('Night')
      step += 1
      #test
      # print("vehicles", traci.vehicle.getIDCount())
      totalVeh.append(traci.vehicle.getIDCount())
      distance = distance + traci.vehicle.getDistance(vehicleNames[0])
      deliverySuccessTot.append(deliverySuccess)
      #test
   traci.close()
   print(step)
   results = {
      #test
      'total of vehicles in scenario': totalVeh, # int
      'total distance route delivery_0': distance, # in [m]
      'delivery success': deliverySuccessTot
      #test
   }
   return results

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

file = 'MorningRoutesJSON/TotalRoutes.json'
os.remove(file)
file = 'AfternoonRoutesJSON/TotalRoutes.json'
os.remove(file)
