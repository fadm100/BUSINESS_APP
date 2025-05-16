import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

# Cargar el DataFrame desde un archivo CSV usando el separador correcto (;)
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\21-04-2025\\Battery.out.csv'
df = pd.read_csv(filePath, sep=';')

# Asegurarse de que los valores son numéricos
df['timestep_time'] = pd.to_numeric(df['timestep_time'], errors='coerce')
df['vehicle_energyConsumed'] = pd.to_numeric(df['vehicle_energyConsumed'], errors='coerce')
df['vehicle_energyCharged'] = pd.to_numeric(df['vehicle_energyCharged'], errors='coerce')
df['vehicle_actualBatteryCapacity'] = pd.to_numeric(df['vehicle_actualBatteryCapacity'], errors='coerce')
df['vehicle_totalEnergyConsumed'] = pd.to_numeric(df['vehicle_totalEnergyConsumed'], errors='coerce')
df['vehicle_totalEnergyRegenerated'] = pd.to_numeric(df['vehicle_totalEnergyRegenerated'], errors='coerce')

# Convertir tiempo a datetime
df['datetime'] = df['timestep_time'].astype(float).apply(lambda x: datetime.datetime(2023, 1, 1) + datetime.timedelta(seconds=x))

# Definir el rango de tiempo entre 05:00 y 22:00 del mismo día
start_time = datetime.datetime(2023, 1, 1, 4, 0, 0)
end_time = datetime.datetime(2023, 1, 1, 22, 0, 0)

# Obtener los vehículos únicos
vehicle_ids = df['vehicle_id'].unique()
n = len(vehicle_ids)

# Figura 1: Energía consumida por vehículo
fig1, axs1 = plt.subplots(n, 1, figsize=(12, 1.5 * n), sharex=True, sharey=True)
if n == 1:
    axs1 = [axs1]

for i, vehicle_id in enumerate(vehicle_ids):
    subset = df[df['vehicle_id'] == vehicle_id]
    axs1[i].plot(subset['datetime'], subset['vehicle_energyConsumed'])
    axs1[i].set_title(f'Vehículo: {vehicle_id}')
    axs1[i].grid(True)
    axs1[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axs1[i].set_xlim(start_time, end_time)
    axs1[i].set_ylabel('Energía (W)')

plt.xlabel('Hora')
plt.tight_layout()
plt.show()

# Figura 2: Energía cargada por vehículo
fig2, axs2 = plt.subplots(n, 1, figsize=(12, 1.5 * n), sharex=True, sharey=True)
if n == 1:
    axs2 = [axs2]

for i, vehicle_id in enumerate(vehicle_ids):
    subset = df[df['vehicle_id'] == vehicle_id]
    axs2[i].plot(subset['datetime'], subset['vehicle_energyCharged'])
    axs2[i].set_title(f'Vehículo: {vehicle_id}')
    axs2[i].grid(True)
    axs2[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axs2[i].set_xlim(start_time, end_time)
    axs2[i].set_ylabel('Energía (W)')

plt.xlabel('Hora')
plt.tight_layout()
plt.show()

# Figura especial para Bus_08
bus08 = df[df['vehicle_id'] == 'Bus_08']
plt.figure(figsize=(12, 6))
plt.plot(bus08['datetime'], bus08['vehicle_energyConsumed'], label='Energía consumida')
plt.plot(bus08['datetime'], bus08['vehicle_energyCharged'], label='Energía cargada')
plt.title('Energía consumida y cargada - Bus_08')
# plt.xlabel('Hora')
plt.ylabel('Energía (W)')
plt.legend()
plt.grid(True)
plt.xlim(start_time, end_time)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()
plt.show()

# Subplots de múltiples variables para Bus_08
df_bus08 = bus08.copy()
columnas = [
    'vehicle_energyCharged',
    'vehicle_totalEnergyConsumed',
    'vehicle_actualBatteryCapacity',
    'vehicle_energyConsumed',
    'vehicle_totalEnergyRegenerated'
]
titles = [
    'Energía cargada',
    'Energía total consumida',
    'Capacidad actual de la batería',
    'Energía consumida',
    'Energía total regenerada'
]
ylabels = [
    'Potencia de carga [W]',
    'Energía [Wh]',
    'Energía [Wh]',
    'Potencia consumo [W]',
    'Energía [Wh]'
]

fig, axs = plt.subplots(len(columnas), 1, figsize=(12, 8), sharex=True, sharey=False)

for i, col in enumerate(columnas):
    axs[i].plot(df_bus08['datetime'], df_bus08[col])
    axs[i].set_title(titles[i])
    axs[i].grid(True)
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axs[i].set_xlim(start_time, end_time)
    axs[i].set_ylabel(ylabels[i])

# plt.xlabel('Hora')
plt.tight_layout()
plt.show()

# Gráfico de estado agregado de carga de la flota
grouped_battery = df.groupby('timestep_time')['vehicle_actualBatteryCapacity'].sum()
normalized_battery = grouped_battery / 4860000

plt.figure(figsize=(10, 5))
plt.plot(
    df['datetime'].drop_duplicates().sort_values(),
    normalized_battery.values,
    label='Capacidad relativa de batería'
)
plt.xlabel('Hora')
plt.ylabel('Fracción de batería total')
plt.title('Estado agregado de carga de la flota en el tiempo')
plt.grid(True)
plt.legend()
plt.xlim(start_time, end_time)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()
plt.show()

print('La demanda total es = ', df_bus08['vehicle_energyConsumed'].sum(), ' Wh')
