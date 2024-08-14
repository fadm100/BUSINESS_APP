import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el DataFrame desde un archivo CSV
filePath = 'Battery.out.csv'  # Reemplaza 'ruta/al/archivo.csv' con la ruta real de tu archivo
df = pd.read_csv(filePath, sep=';')

print("DataFrame first 5 rows")
print(df.head())

print("\nDataFrame information")
print(df.info())

print("\nDataFrame Descriptive statistics")
print(df.describe())

# Group per vehicle_id and perform analysis
grouped = df.groupby('vehicle_id')

# Analyze total energy consumption per vehicle_id
totalEnergyConsumed = (grouped['vehicle_totalEnergyConsumed'].last() - grouped['vehicle_totalEnergyRegenerated'].last()) / 1000
print("\nTotal energy consumption per vehicle [kWh]")
print(totalEnergyConsumed)

# Analyze total cost of energy consumption per vehicle_id
totalEnergyCost = totalEnergyConsumed * 1099.25 # COP/kWh CEDENAR july 2024
print("\nTotal energy consumption per vehicle [COP]")
print(totalEnergyCost)

# Analyze the final battery state of charge
totalCapacity = 80000
batterySoC = grouped['vehicle_actualBatteryCapacity'].last() / totalCapacity * 100
print("\nFinal SoC per vehicle")
print(batterySoC)

# Function to add annotations to the bars
def AddAnnotations(ax):
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')

# Graph total energy consumption per vehicle_id
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=totalEnergyConsumed.index, y=totalEnergyConsumed.values)
AddAnnotations(ax)
plt.xlabel('ID vehículo')
plt.ylabel('Consumo Total de Energía [kWh]')
plt.title('Consumo Total de Energía por vehículo')
plt.xticks(rotation=45)
plt.show()

# Graph total cost of energy consumption per vehicle_id
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=totalEnergyCost.index, y=totalEnergyCost.values)
AddAnnotations(ax)
plt.xlabel('ID vehículo')
plt.ylabel('Costo Total de Energía [COP]')
plt.title('Costo Total de Energía por vehículo')
plt.xticks(rotation=45)
plt.show()

# Graph battery SoC per vehicle_id
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=batterySoC.index, y=batterySoC.values)
AddAnnotations(ax)
plt.xlabel('ID vehículo')
plt.ylabel('SoC de la Batería [%]')
plt.title('Estado de carga de la Batería por vehículo')
plt.xticks(rotation=45)
plt.show()

# Count how many rows in 'vehicle_chargingStationId' are different from NULL, discriminated per 'vehicle_id'  vehicle_lane
chargingTime = df.groupby('vehicle_id')['vehicle_chargingStationId'].apply(lambda x: x.notnull().sum()) / 60

print("Total charging time per vehicle [min]")
print(chargingTime)

# Grapf total charging time per vehicle
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=chargingTime.index, y=chargingTime.values)
AddAnnotations(ax)
plt.xlabel('ID vehículo')
plt.ylabel('Tiempo Total de Carga [min]')
plt.title('Tiempo Total de Carga por vehículo')
plt.xticks(rotation=45)
plt.show()

# Count how many rows in 'vehicle_lane' are equal to -E0_0, discriminated per 'vehicle_id'  
parkingTime = df[df['vehicle_lane'] == '-E0_0'].groupby('vehicle_id').size() /3600

print("Total parking time per vehicle [h]")
print(parkingTime)

# Grapf total charging time per vehicle
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=parkingTime.index, y=parkingTime.values)
AddAnnotations(ax)
plt.xlabel('ID vehículo')
plt.ylabel('Tiempo Total de parqueo [h]')
plt.title('Tiempo Total de parqueo por vehículo')
plt.xticks(rotation=45)
plt.show()

# Crear el DataFrame combinado (si no lo tienes ya)
combined_data = pd.DataFrame({
    'charging_time': chargingTime / 60,
    'parking_time': parkingTime
})

# Rellenar NaN con 0 para los vehículos sin registros
combined_data = combined_data.fillna(0)

# Añadir vehicle_id como una columna
combined_data['vehicle_id'] = combined_data.index

# Reordenar columnas para el gráfico
combined_data = combined_data[['vehicle_id', 'charging_time', 'parking_time']]

# Supongamos que ya tenemos el DataFrame combined_data
# Calcular la tercera variable
combined_data['time_on_route'] = 24 - (combined_data['charging_time'] + combined_data['parking_time'])

# Asegurarse de que no haya valores negativos
combined_data['time_on_route'] = combined_data['time_on_route'].clip(lower=0)

# Verificar el DataFrame
print('Combined Data')
print(combined_data.head())

# Configurar la figura del gráfico
plt.figure(figsize=(12, 8))

# Crear el gráfico de áreas apiladas
plt.stackplot(combined_data['vehicle_id'], 
              combined_data['charging_time'], 
              combined_data['parking_time'],
              combined_data['time_on_route'],
              labels=['Tiempo de carga', 'Tiempo de parqueo', 'Tiempo en ruta'])

# Configurar las etiquetas y el título
plt.title('Distribución de tiempo en un día por vehículo en horas')
plt.xlabel('ID del Vehículo')
plt.ylabel('Tiempo [h]')
plt.legend(loc='upper left')

# Mostrar el gráfico
plt.show()
