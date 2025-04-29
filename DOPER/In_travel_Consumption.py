import pandas as pd

# Cargar los datos desde el archivo CSV
file_path = "H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\25-04-2025\\Battery.out.csv" 
df = pd.read_csv(file_path, sep=';')

# Convertir timestep_time a tipo float
df["timestep_time"] = df["timestep_time"].astype(float)

# Definir el tamaño del intervalo en segundos (5 minutos = 300 segundos)
interval_size = 300

# Crear una nueva columna para agrupar por intervalos de tiempo
df["time_interval"] = (df["timestep_time"] // interval_size) * interval_size

# Sumar vehicle_energyConsumed agrupando por time_interval y vehicle_id
result = df.groupby(["time_interval", "vehicle_id"])["vehicle_energyConsumed"].sum().unstack(fill_value=0).reset_index()

# Dividir todas las columnas excepto 'time_interval' entre 12
result.loc[:, result.columns != 'time_interval'] = result.loc[:, result.columns != 'time_interval'] / 1000
print('Suma = ', result.loc[:, result.columns != 'time_interval'].sum())
# Redondear a 3 decimales todas las columnas excepto 'time_interval'
result.loc[:, result.columns != 'time_interval'] = result.loc[:, result.columns != 'time_interval'].round(3)

# Nueva lista de nombres de columnas
nuevos_nombres = [
    'time_interval','Bus_0','Bus_1','Bus_2','Bus_3','Bus_4','Bus_5','Bus_6','Bus_7','Bus_8','Bus_9','Bus_10','Bus_11','Bus_12','Bus_13','Bus_14'
]

# Asignar los nuevos nombres
result.columns = nuevos_nombres

# Guardar el resultado en un nuevo archivo CSV
result.to_csv("H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\25-04-2025\\energia_cada_5min.csv", index=False, sep=";")

# Mostrar los primeros registros del resultado
print(result.head())
print('Suma = ', result.loc[:, result.columns != 'time_interval'].sum())
# Convertir los datos de la columna 'Delivery_0' en un array
vehicle = result['Bus_0'].dropna().to_numpy()

# Crear nuevo DataFrame con 1 donde hay 0, y 0 en otro caso (excepto la columna time_interval)
df_binary = result.copy()
df_binary.iloc[:, 1:] = (df_binary.iloc[:, 1:] == 0.0).astype(int)

# Nueva lista de nombres de columnas
nuevos_nombres = [
    'time_interval',
    'battery_EV0_avail', 'battery_EV1_avail', 'battery_EV2_avail', 'battery_EV3_avail',
    'battery_EV4_avail', 'battery_EV5_avail', 'battery_EV6_avail', 'battery_EV7_avail',
    'battery_EV8_avail', 'battery_EV9_avail', 'battery_EV10_avail', 'battery_EV11_avail',
    'battery_EV12_avail', 'battery_EV13_avail', 'battery_EV14_avail'
]

# Asignar los nuevos nombres
df_binary.columns = nuevos_nombres

# Guardar el resultado en un nuevo archivo CSV
df_binary.to_csv("H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\25-04-2025\\disponibilidad_cada_5min.csv", index=False, sep=";")
