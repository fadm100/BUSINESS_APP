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

nameJSON = ['C1Route']

norm = ["Energy/unknown"] # Energy/unknown --> https://sumo.dlr.de/docs/Models/Electric.html
norms = ['EV']

acceleration = [2.0, 3.0, 4.0]
stopsRate = [0] # 0.35 is used for peak-off and 0.65 is used for rush hours
stopsRates = ['0.0']

def defineStops(stopsRate, deliveryRoute):
   for j in range(len(deliveryRoute)):
      R = random.random()
      if R < stopsRate:
         stopTime = random.randint(3, 60)
         traci.vehicle.setStop(vehicleNames[0], deliveryRoute[j], 0.1, 0, stopTime, 0, 0.0, 2.0)

def DataCalculate(route, norm_in, accel, rateOfStops):
   print('My Route is: ', route)
   step = 0
   actualBatteryCapacity = 0
   maximumBatteryCapacity = 0
   minimumDoD = 0.5

   traci.start(route)

   vehicleNames = []
   for i in range(len(routesJSON)):
      with open(routesJSON[i]) as json_file:
         deliveryRoute = json.load(json_file)
      routes = RG.DeliveryStops(deliveryRoute, i)
      print('The routes are: ', routes)

      traci.route.add(routes['names'][0], routes['routes'][0]) # This route was made in VAN_Ruta.rou.xml, as well. Whatever option es possible
      vehicleNames.append("Delivery_" + str(i))
      traci.vehicle.add(vehicleNames[i], routes['names'][0],"VAN","now")
      """This vehicle is added here because file.rou.xml don't give the minimum route.
      TraCI SUMO finds the minimum route only if the route has 
      2 edges, depart edge and arrival edge; otherwise, SUMO gives
      a warning and teleports the vehicle"""
      traci.vehicle.setEmissionClass(vehicleNames[i], norm_in)
   traci.vehicle.setAccel(vehicleNames[0], accel)

   # rateOfStops --> this is a number between 0 and 1. 
   # This parameter defines how many stops will be set.
   # with a high number, the number of stops will be major 
   # TraCI retrievals --> https://sumo.dlr.de/docs/TraCI.html
   defineStops(rateOfStops, deliveryRoute)
   # traci.vehicle.setChargingStationStop("0", "cS_2to19_0a", 10, 2.0, 0) # stop 10 seconds but only go on if the time is uper than 2.0 seconds
   # print('The street name is: ', traci.edge.getStreetName(':cluster_979937596_979937615_7'))
   deliveryStops = len(routes['names'])
   deliverySuccess = 1
   while traci.simulation.getMinExpectedNumber() > 0:
      traci.simulation.getMinExpectedNumber()
      traci.simulationStep()
      vehicles = traci.vehicle.getIDList()
      for i in range(len(routesJSON)):
         if len(vehicles) != 0:
            actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
            maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
            stop = EVC.EVCharge(actualBatteryCapacity, minimumBatteryCapacity=maximumBatteryCapacity*minimumDoD)
            # print('The vehicle stop state is', stop)
            step += 1
            if traci.vehicle.getRoadID(vehicleNames[i])==deliveryRoute[deliverySuccess]:
               if deliverySuccess < deliveryStops:
                  traci.vehicle.remove(vehicleNames[i])
                  traci.route.add(routes['names'][deliverySuccess], routes['routes'][deliverySuccess])
                  traci.vehicle.add(vehicleNames[i],routes['names'][deliverySuccess],"VAN","now")
                  deliverySuccess+=1
               elif traci.vehicle.getRoadID(vehicleNames[i])=="-E0":
                  traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=2, flags=1)             
      if traci.simulation.getTime() > 2000:
         traci.vehicle.remove(vehicleNames[i])
   traci.close()
   results = {
      'ActualBatteryCapacity': actualBatteryCapacity/1e3, # in [Kwh]
   }
   return results

root = ET.parse("Battery.out.xml")
root_node = root.getroot()

total = {}


for j in range(len(stopsRate)):
   fuelRoute = []
   Routes = {}
   for i in range(len(sumoCmd)):
      ##### The route to use
      # with open(routesJSON[i]) as json_file:
      #    deliveryRoute = json.load(json_file)
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
