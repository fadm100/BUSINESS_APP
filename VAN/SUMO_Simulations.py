from operator import le
import os, sys
from random import random
import random
import json
import matplotlib.pyplot as plt 
import numpy as np
import EV_Charge as EVC
import RouteGenerator as RG

from turtle import clear
if 'SUMO_HOME' in os.environ:
   tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
   sys.path.append(tools)
else:
   sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

sumoCmd = [["sumo", "-c", "TestVan.sumocfg"]]
# sumoCmd = [["sumo-gui", "-c", "TestVan.sumocfg"]]

routesJSON = ['RoutesJSON/DE01_Route.json']

nameJSON = ['C1Route']

norm = ["Energy/unknown"] # Energy/unknown --> https://sumo.dlr.de/docs/Models/Electric.html
norms = ['EV']

acceleration = [2.0, 3.0, 4.0]
stopsRate = [0] # 0.35 is used for peak-off and 0.65 is used for rush hours
stopsRates = ['0.35']

def defineStops(stopsRate):
   for j in range(len(deliveryRoute)):
      R = random.random()
      if R < stopsRate:
         stopTime = random.randint(3, 60)
         traci.vehicle.setStop("Delivery_01", deliveryRoute[j], 0.1, 0, stopTime, 0, 0.0, 2.0)

def DataCalculate(route, norm_in, accel, rateOfStops):
   print('My Route is: ', route)
   step = 0
   speed = 0
   distance = 0
   acceleration = 0
   totalEnergyBatConsumption = 0
   totalEnergyConsumption = 0
   totalEnergyRegenerated = 0
   actualBatteryCapacity = 0
   maximumBatteryCapacity = 0
   deepOfDischarge = 0.5
   noise = 0
   effort = 0
   traci.start(route)

   routes = RG.DeliveryStops(deliveryRoute)
    
   traci.route.add(routes['names'][0], routes['routes'][0]) # This route was made in VAN_Ruta.rou.xml, as well. Whatever option es possible
   traci.vehicle.add("Delivery_01",routes['names'][0],"VAN","now")
   """This vehicle is added here because file.rou.xml don't give the minimum route.
      TraCI SUMO finds the minimum route only if the route has 
      2 edges, depart edge and arrival edge; otherwise, SUMO gives
      a warning and teleports the vehicle"""

   traci.vehicle.setEmissionClass("Delivery_01", norm_in)
   traci.vehicle.setAccel("Delivery_01", accel)

   # rateOfStops --> this is a number between 0 and 1. 
   # This parameter defines how many stops will be set.
   # with a high number, the number of stops will be major 
   # TraCI retrievals --> https://sumo.dlr.de/docs/TraCI.html
   defineStops(rateOfStops)
   # traci.vehicle.setChargingStationStop("0", "cS_2to19_0a", 10, 2.0, 0) # stop 10 seconds but only go on if the time is uper than 2.0 seconds
   # print('The street name is: ', traci.edge.getStreetName(':cluster_979937596_979937615_7'))
   simulationRun = True
   while traci.simulation.getMinExpectedNumber() > 0:
   # while simulationRun:
      traci.simulation.getMinExpectedNumber()
      traci.simulationStep()
      vehicles = traci.vehicle.getIDList()
      if len(vehicles) != 0:
         """ # This is made to calculate the the speed without considering the detention of the vehicle
         if traci.vehicle.getSpeed("0") != 0:
            speed2 = speed2 + traci.vehicle.getSpeed("0")
            count += 1
         """
         speed = speed + traci.vehicle.getSpeed("Delivery_01")
         distance = traci.vehicle.getDistance("Delivery_01")
         acceleration = acceleration + traci.vehicle.getAcceleration("Delivery_01")
         totalEnergyBatConsumption = totalEnergyBatConsumption + float(traci.vehicle.getParameter("Delivery_01", "device.battery.energyConsumed"))
         # totalEnergyConsumption = totalEnergyConsumption + traci.vehicle.getElectricityConsumption("0")
         totalEnergyConsumption = float(traci.vehicle.getParameter("Delivery_01", "device.battery.totalEnergyConsumed"))
         totalEnergyRegenerated = float(traci.vehicle.getParameter("Delivery_01", "device.battery.totalEnergyRegenerated"))
         actualBatteryCapacity = float(traci.vehicle.getParameter("Delivery_01", "device.battery.actualBatteryCapacity"))
         maximumBatteryCapacity = float(traci.vehicle.getParameter("Delivery_01", "device.battery.maximumBatteryCapacity"))
         stop = EVC.EVCharge(actualBatteryCapacity, minimumBatteryCapacity=maximumBatteryCapacity*deepOfDischarge)
         # print('The vehicle stop state is', stop)
         noise = noise + traci.vehicle.getNoiseEmission("Delivery_01")
         effort = effort + traci.vehicle.getEffort("Delivery_01", 1.0, ':cluster_979937596_979937615_7')
         step += 1
         if traci.vehicle.getRoadID("Delivery_01")==deliveryRoute[1] and simulationRun:
            print('Delivery_01 current edge: ', traci.vehicle.getRoadID("Delivery_01"))
            traci.vehicle.remove("Delivery_01")
            traci.route.add(routes['names'][1], routes['routes'][1]) # This route was made in VAN_Ruta.rou.xml, as well. Whatever option es possible
            traci.vehicle.add("Delivery_01",routes['names'][1],"VAN","now")
            simulationRun = False
   traci.close()
   print('Actual battery capacity is:', actualBatteryCapacity)
   meanSpeed = speed*3600/(step*1000)
   meanNoise = noise/step
   results = {
      'BatteryEnergy': totalEnergyBatConsumption/1e3, # in [kwh] 
      'TotalEnergyConsumed': totalEnergyConsumption/1e3, # in [Kwh] 
      'TotalEnergyRegenerated': totalEnergyRegenerated/1e3, # in [Kwh]
      'ActualBatteryCapacity': actualBatteryCapacity/1e3, # in [Kwh]
      'Speed': meanSpeed, # in [m/s]
      'Acceleration': acceleration,
      'Distance': distance/1e3, # in [km]
      'Noise': meanNoise, # in [dB]
      'Effort': effort # unidades???
   }
   return results

total = {}


for j in range(len(stopsRate)):
   fuelRoute = []
   Routes = {}
   for i in range(len(sumoCmd)):
      ##### The route to use
      with open(routesJSON[i]) as json_file:
         deliveryRoute = json.load(json_file)
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
