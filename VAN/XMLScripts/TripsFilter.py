import xml.etree.ElementTree as ET
from random import random
import random

totalTrips = ['bus.trip.xml', 'moto.trip.xml', 'taxi.trip.xml', 'vehicle.trip.xml']

deletePrBus = 0.8
deletePrMoto = 0.4
deletePrTaxi = 0.5
deletePrVehicle = 0.1

probabilities = [deletePrBus, deletePrMoto, deletePrTaxi, deletePrVehicle]

def VehicleFilter(vehicleTrip, deleteProbability):
    tree = ET.parse(vehicleTrip)
    root = tree.getroot()
    root.tag
    for trip in root.findall('trip'): 
        R = random.random()
        if R < deleteProbability:
            root.remove(trip) 
    tree.write(vehicleTrip)
    
for i in range(totalTrips):
    VehicleFilter(totalTrips[i], probabilities[i])