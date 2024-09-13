def VehiclesManagement(step, i, chargeFlag, vehicleNames, fleetRoutes, maximumDoD, deliverySuccess, deliveryStops):
   actualBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.actualBatteryCapacity"))
   maximumBatteryCapacity = float(traci.vehicle.getParameter(vehicleNames[i], "device.battery.maximumBatteryCapacity"))
   chargeStop = True if actualBatteryCapacity < maximumBatteryCapacity * (1 - maximumDoD) else False 
   batteryFull = True if actualBatteryCapacity > maximumBatteryCapacity * maximumCharge else False

   # Verificar si el vehículo está en un estacionamiento a las horas indicadas
   if traci.vehicle.isStoppedParking(vehicleNames[i]) and (step == eightAM or step == twoPM): 
      traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=10, until=eightAM, flags=0)
      traci.vehicle.changeTarget(vehicleNames[i], fleetRoutes[vehicleNames[i]][1])

      # Validar si el punto de parada está en la ruta
      current_route = traci.vehicle.getRoute(vehicleNames[i])  # Obtener la ruta actual
      next_stop = fleetRoutes[vehicleNames[i]][1]  # Próxima parada
      if next_stop in current_route:  # Si la próxima parada está en la ruta
         stopTime = random.randint(60, 600)
         traci.vehicle.setStop(vehicleNames[i], next_stop, 0.1, 0, stopTime, 0, 0.0, 2.0)
      else:
         print(f"Error: La próxima parada {next_stop} no está en la ruta del vehículo {vehicleNames[i]}")

   # Verificar si el vehículo ya llegó a su parada
   elif traci.vehicle.getRoadID(vehicleNames[i]) == fleetRoutes[vehicleNames[i]][1] and len(fleetRoutes[vehicleNames[i]]) > 1:
      currentEdge = traci.vehicle.getRoadID(vehicleNames[i])
      if currentEdge != "-E0": 
         del fleetRoutes[vehicleNames[i]][1]
         newTarget = fleetRoutes[vehicleNames[i]][1]
         traci.vehicle.changeTarget(vehicleNames[i], newTarget)
         current_route = traci.vehicle.getRoute(vehicleNames[i])
         if newTarget in current_route:
            stopTime = random.randint(60, 600)
            traci.vehicle.setStop(vehicleNames[i], newTarget, 0.1, 0, stopTime, 0, 0.0, 2.0)
         else:
            print(f"Error: El nuevo destino {newTarget} no está en la ruta del vehículo {vehicleNames[i]}")
      elif currentEdge == "-E0" and not chargeStop:
         traci.vehicle.setParkingAreaStop(vehicleNames[i], "ParkAreaA", duration=midnight, until=midnight, flags=1)
   
   # Verificar si es necesario hacer una parada de carga
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

