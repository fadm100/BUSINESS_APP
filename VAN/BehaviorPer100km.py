import xml.etree.ElementTree as ET

tree = ET.parse('Battery.out.xml')
# tree = ET.parse('EnergyUnknownBattery.out.xml')
root = tree.getroot()
root.tag

data = root.findall('timestep')
vehData = data[-1].findall('vehicle')

energyConsumed = []
energyRegenerated = []

for vehicle in vehData:
    energyConsumed.append(float(vehicle.get('totalEnergyConsumed')))
    energyRegenerated.append(float(vehicle.get('totalEnergyRegenerated')))

speedVh = [0, 0, 0, 0, 0, 0]
for timeStep in root: 
    for vehicle in timeStep.findall('vehicle'):
        if vehicle.get('id') == 'Delivery_0':
            speedVh[0] = speedVh[0] + float(vehicle.get('speed'))
        elif vehicle.get('id') == 'Delivery_1':
            speedVh[1] = speedVh[1] + float(vehicle.get('speed'))
        elif vehicle.get('id') == 'Delivery_2':
            speedVh[2] = speedVh[2] + float(vehicle.get('speed'))
        elif vehicle.get('id') == 'Delivery_3':
            speedVh[3] = speedVh[3] + float(vehicle.get('speed'))
        elif vehicle.get('id') == 'Delivery_4':
            speedVh[4] = speedVh[4] + float(vehicle.get('speed'))
        elif vehicle.get('id') == 'Delivery_5':
            speedVh[5] = speedVh[5] + float(vehicle.get('speed'))
            
rendimiento = []
realConsumption = []
speed100km = []
shouldBe = []
for i in range(len(speedVh)):
    realConsumption.append((energyConsumed[i] - energyRegenerated[i])/1000)
    speed100km.append(speedVh[i]/1000/100)
    rendimiento.append(realConsumption[i] / speed100km[i])
    shouldBe.append(35 * speed100km[i])

print('distance in 100km = ', speed100km)
print('real consumption = ', realConsumption)
print('consumption that should be = ', shouldBe)
print('performance = ', rendimiento)
print('performance average = ', sum(rendimiento) / len(rendimiento))
