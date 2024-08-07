import xml.etree.ElementTree as ET
from random import sample

totalTrips = ['bus.trips.xml', 'moto.trips.xml', 'taxi.trips.xml', 'vehicle.trips.xml']

depart = [[], [], [], []]

for j in range(4):
    for i in range(5):
        depart1 = sample([x for x in range(25200+86400*i,64800+86400*i)],18000)
        depart[j]+=depart1
    depart[j].sort(reverse=False)

def VehicleDepart(vehicleTrip, j):
    tree = ET.parse(vehicleTrip)
    root = tree.getroot()
    root.tag
    i = 0
    for trip in root.findall('trip'): 
        trip.set('depart', str(depart[j][i]))
        i += 1
    tree.write(vehicleTrip)

i = 0
for vehTrip in totalTrips:
    VehicleDepart(vehTrip, i)
    i += 1