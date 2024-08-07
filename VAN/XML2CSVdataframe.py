import xml.etree.ElementTree as ET
import pandas as pd

xml_file = 'Battery5Days.out.xml'

tree = ET.parse(xml_file)
root = tree.getroot()

data = []

for timestep in root.findall('timestep'):
    time = timestep.get('time')
    for vehicle in timestep.findall('vehicle'):
        vehicle_data = vehicle.attrib
        vehicle_data['time'] = time  # Agregar el tiempo al diccionario de datos del vehículo
        data.append(vehicle_data)

df = pd.DataFrame(data)

print(df.head)

df.to_csv('Battery5DaysDataframe.csv', index=False)