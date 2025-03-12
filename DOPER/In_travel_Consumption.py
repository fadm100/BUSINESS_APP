import pandas as pd

# Cargar los datos desde el archivo CSV
file_path = "H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\29-11-2024\\Battery.out.csv" 
df = pd.read_csv(file_path, sep=';')

# Convertir timestep_time a tipo float
df["timestep_time"] = df["timestep_time"].astype(float)

# Definir el tamaño del intervalo en segundos (5 minutos = 300 segundos)
interval_size = 300

# Crear una nueva columna para agrupar por intervalos de tiempo
df["time_interval"] = (df["timestep_time"] // interval_size) * interval_size

# Sumar vehicle_energyConsumed agrupando por time_interval y vehicle_id
result = df.groupby(["time_interval", "vehicle_id"])["vehicle_energyConsumed"].sum().unstack(fill_value=0).reset_index()

# Guardar el resultado en un nuevo archivo CSV
result.to_csv("H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\29-11-2024\\energia_cada_5min.csv", index=False, sep=";")

# Mostrar los primeros registros del resultado
print(result.head())

# Convertir los datos de la columna 'Delivery_0' en un array
delivery_0_array = result['Delivery_0'].dropna().to_numpy()

# Imprimir el array
print(delivery_0_array)
