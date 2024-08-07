import xml.etree.ElementTree as ET
import json

tree = ET.parse('H:\My Drive\Artículos tesis\DESARROLLO\Ob2\Simulations\VAN\Pasto_VAN.net.xml')
root = tree.getroot()
root.tag

totalEdges = []
for edge in root.findall('edge'): 
    totalEdges.append(edge.get('id'))
    
with open('TotalEdges.json', 'w') as outfile:
    json.dump(totalEdges, outfile)