import xml.etree.ElementTree as ET
from random import random
import random

totalTrips = ['bus.trips.xml', 'moto.trips.xml', 'taxi.trips.xml', 'vehicle.trips.xml']

deletePrBus = 0.5
deletePrMoto = 0.5
deletePrTaxi = 0.5
deletePrVehicle = 0.5

probabilities = [deletePrBus, deletePrMoto, deletePrTaxi, deletePrVehicle]

def VehicleFilter(vehicleTrip, deleteProbability):
    tree = ET.parse(vehicleTrip)
    root = tree.getroot()
    root.tag
    i = 25200
    for trip in root.findall('trip'): 
        R = random.random()
        if R < deleteProbability:
            root.remove(trip) 
        else:
            # trip.set('depart', str(i))
            i+=1
    tree.write(vehicleTrip)

i = 0
for vehTrip in totalTrips:
    VehicleFilter(vehTrip, probabilities[i])
    i += 1