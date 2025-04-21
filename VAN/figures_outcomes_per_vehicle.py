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

# Obtener los vehículos únicos
vehicle_ids = df['vehicle_id'].unique()
n = len(vehicle_ids)

# Crear subplots: uno por vehículo
fig1, axs1 = plt.subplots(n, 1, figsize=(12, 4 * n), sharex=True)

# Si solo hay un vehículo, axs no es una lista. Convertirlo en lista para consistencia
if n == 1:
    axs1 = [axs1]

# Graficar en cada subplot
for i, vehicle_id in enumerate(vehicle_ids):
    subset = df[df['vehicle_id'] == vehicle_id]
    axs1[i].plot(subset['timestep_time'], subset['vehicle_energyConsumed'])
    axs1[i].set_title(f'Vehículo: {vehicle_id}')
    axs1[i].set_ylabel('Energía consumida (W)')
    axs1[i].grid(True)

# Etiqueta común del eje x
plt.xlabel('Tiempo (s)')
plt.tight_layout()
plt.show()

# Crear subplots: uno por vehículo
fig2, axs2 = plt.subplots(n, 1, figsize=(12, 4 * n), sharex=True)

# Si solo hay un vehículo, axs no es una lista. Convertirlo en lista para consistencia
if n == 1:
    axs2 = [axs2]

# Graficar en cada subplot
for i, vehicle_id in enumerate(vehicle_ids):
    subset = df[df['vehicle_id'] == vehicle_id]
    axs2[i].plot(subset['timestep_time'], subset['vehicle_energyCharged'])
    axs2[i].set_title(f'Vehículo: {vehicle_id}')
    axs2[i].set_ylabel('Energía consumida (W)')
    axs2[i].grid(True)

# Etiqueta común del eje x
plt.xlabel('Tiempo (s)')
plt.tight_layout()
plt.show()

# Figura especial para Bus_01
bus01 = df[df['vehicle_id'] == 'Bus_01']

plt.figure(figsize=(12, 6))
plt.plot(bus01['timestep_time'], bus01['vehicle_energyConsumed'], label='Energía consumida')
plt.plot(bus01['timestep_time'], bus01['vehicle_energyCharged'], label='Energía cargada')
plt.title('Energía consumida y cargada - Bus_01')
plt.xlabel('Tiempo (s)')
plt.ylabel('Energía (W)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

################

# Filtrar solo Bus_01
df_bus01 = df[df['vehicle_id'] == 'Bus_06'].copy()

# Convertir tiempo a datetime
start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)  # Fecha base cualquiera
df_bus01['tiempo'] = df_bus01['timestep_time'].astype(float).apply(
    lambda x: start_time + datetime.timedelta(seconds=x)
)

# Columnas a graficar
columnas_a_graficar = [
    'vehicle_energyCharged',
    'vehicle_totalEnergyConsumed',
    'vehicle_actualBatteryCapacity',
    'vehicle_energyConsumed',
    'vehicle_totalEnergyRegenerated'
]

# Crear subplots
filas, columnas = 5, 1
fig, axs = plt.subplots(filas, columnas, figsize=(16, 3 * filas), sharex=True)
axs = axs.flatten()

# Graficar
for i, col in enumerate(columnas_a_graficar):
    axs[i].plot(df_bus01['tiempo'], df_bus01[col])
    axs[i].set_title(col)
    axs[i].set_ylabel(col)
    axs[i].grid(True)

    axs[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

# Rotar etiquetas del eje X
for ax in axs[:len(columnas_a_graficar)]:
    plt.setp(ax.get_xticklabels(), rotation=45)

# Eliminar subplots no usados
for j in range(len(columnas_a_graficar), filas * columnas):
    fig.delaxes(axs[j])

plt.tight_layout()
plt.show()