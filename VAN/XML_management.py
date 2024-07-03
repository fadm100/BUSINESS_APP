import xml.etree.ElementTree as ET

tree = ET.parse('Battery.out.xml')
root = tree.getroot()
root.tag

i = 0
for child in root: 
    for vehicle in child.findall('vehicle'):
        print(id)
        if id != "Delivery_0" and id != "Delivery_1" and id != "Delivery_2" and id != "Delivery_3" and id != "Delivery_4" and id != "Delivery_5":
            child.remove(vehicle)
    
tree.write('BatteryOut.xml')