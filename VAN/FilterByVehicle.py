import xml.etree.ElementTree as ET

tree = ET.parse('Battery5Days.out.xml')

root = tree.getroot()
root.tag

for timeStep in root: 
    for vehicle in timeStep.findall('vehicle'):
        if vehicle.get('id') != 'Delivery_0':
            timeStep.remove(vehicle)
    
tree.write('Battery.out.xml')