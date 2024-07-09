import xml.etree.ElementTree as ET

tree = ET.parse('Battery.out.xml')
root = tree.getroot()
root.tag

for timeStep in root: 
    for vehicle in timeStep.findall('vehicle'):
        if id != "Delivery_0" and id != "Delivery_1" and id != "Delivery_2" and id != "Delivery_3" and id != "Delivery_4" and id != "Delivery_5":
            timeStep.remove(vehicle)
    
tree.write('BatteryOut.xml')