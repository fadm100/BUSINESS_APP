import xml.etree.ElementTree as ET

tree = ET.parse('Pasto_VAN.net.xml')

root = tree.getroot()
root.tag

edges = root.findall('edge')

# for edge in edges: 
#     for lane in edge.findall('lane'):
#         if float(lane.get('speed')) >= 22.22:
#             lane.set('speed', str(22.22))
#         elif float(lane.get('speed')) >= 13.88 and float(lane.get('speed')) < 22.22:
#             lane.set('speed', str(13.88))
#         elif float(lane.get('speed')) < 13.88:
#             lane.set('speed', str(8.33))

for edge in edges: 
    for lane in edge.findall('lane'):
        if float(lane.get('speed')) >= 13.88:
            lane.set('speed', str(13.88))
    
tree.write('Pasto_VAN_Updated.net.xml')