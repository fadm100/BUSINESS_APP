import xml.etree.ElementTree as ET
import json

tree = ET.parse('H:\My Drive\Artículos tesis\DESARROLLO\Ob2\Simulations\VAN\Pasto_VAN.net.xml')
root = tree.getroot()
root.tag

totalLanes = []
for edge in root.findall('edge'): 
    for lane in edge.findall('lane'):
        totalLanes.append(lane.get('id'))
    
with open('TotalLanes.json', 'w') as outfile:
    json.dump(totalLanes, outfile)