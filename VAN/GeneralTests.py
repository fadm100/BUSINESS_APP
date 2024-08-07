import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el DataFrame desde un archivo CSV
file_path = 'Battery.out.csv'  # Reemplaza 'ruta/al/archivo.csv' con la ruta real de tu archivo
df = pd.read_csv(file_path, sep=';')

# Mostrar las primeras 5 filas del DataFrame
print("Primeras 5 filas del DataFrame:")
print(df.head())

# Información del DataFrame
print("\nInformación del DataFrame:")
print(df.info())

# Estadísticas descriptivas
print("\nEstadísticas descriptivas del DataFrame:")
print(df.describe())

# Agrupar por vehicle_id y realizar análisis
grouped = df.groupby('vehicle_id')

# Analizar el consumo de energía total por vehicle_id
total_energy_consumed = grouped['vehicle_totalEnergyConsumed'].last() - grouped['vehicle_totalEnergyRegenerated'].last()
print("\nConsumo total de energía por vehicle_id:")
print(total_energy_consumed)

# Analizar la capacidad de batería actual promedio por vehicle_id
mean_battery_capacity = grouped['vehicle_actualBatteryCapacity'].last()
print("\nCapacidad de batería final por vehicle_id:")
print(mean_battery_capacity)

# Función para añadir anotaciones a las barras
def add_annotations(ax):
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')

# Graficar el consumo total de energía por vehicle_id
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=total_energy_consumed.index, y=total_energy_consumed.values)
add_annotations(ax)
plt.xlabel('Vehicle ID')
plt.ylabel('Consumo Total de Energía')
plt.title('Consumo Total de Energía por Vehicle ID')
plt.xticks(rotation=45)
plt.show()

# Graficar la capacidad de batería actual promedio por vehicle_id
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=mean_battery_capacity.index, y=mean_battery_capacity.values)
add_annotations(ax)
plt.xlabel('Vehicle ID')
plt.ylabel('Capacidad de Batería Promedio')
plt.title('Capacidad de Batería Promedio por Vehicle ID')
plt.xticks(rotation=45)
plt.show()

# Contar cuántas filas en 'vehicle_chargingStationId' son diferentes de NULL, discriminado por 'vehicle_id'
chargingTime = df.groupby('vehicle_id')['vehicle_chargingStationId'].apply(lambda x: x.notnull().sum())

print("Número de filas donde 'vehicle_chargingStationId' es diferente de NULL, discriminado por 'vehicle_id':")
print(chargingTime)

# Graficar el tiempo total de carga por vehicle_id
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=chargingTime.index, y=chargingTime.values)
add_annotations(ax)
plt.xlabel('Vehicle ID')
plt.ylabel('Tiempo Total de Carga')
plt.title('Tiempo Total de Carga por Vehicle ID')
plt.xticks(rotation=45)
plt.show()
