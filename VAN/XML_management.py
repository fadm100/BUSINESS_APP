import xml.etree.ElementTree as ET

tree = ET.parse('Battery.out.xml')
root = tree.getroot()
root.tag
root[0][0]

# for child in root:
#     print(child.tag, child.attrib)
    
# for timestep in root.findall('timestep'):
#     vehicle = timestep.find('vehicle')
#     name = timestep.get('name')
#     print(name, vehicle)