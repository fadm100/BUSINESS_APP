import pandas as pd
import glob

# Ruta de los archivos CSV (ajusta según la ubicación de los archivos)
ruta_archivos = 'D:\\UNIVALLE\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\ev_variable_results/*.csv'

# Leer todos los archivos CSV en la ruta
archivos_csv = glob.glob(ruta_archivos)

# Inicializar el DataFrame final como None
df_final = None

# Iterar sobre cada archivo CSV
for archivo in archivos_csv:
    # Leer cada archivo CSV
    df = pd.read_csv(archivo)
    
    # Asegurarse de que la columna 'datetime' sea tratada correctamente
    if 'datetime' not in df.columns:
        raise ValueError(f"El archivo {archivo} no contiene la columna 'datetime'")
    
    # Combinar los DataFrames alineando por 'datetime'
    if df_final is None:
        df_final = df  # Primer archivo se usa como base
    else:
        df_final = pd.merge(df_final, df, on='datetime', how='outer')  # Unión por 'datetime'

# Ordenar el DataFrame final por la columna 'datetime'
df_final = df_final.sort_values(by='datetime')

# # Convertir la columna a formato de fecha y hora en UTC
# df_final['datetime'] = pd.to_datetime(df_final['Timestamp'], unit='s', utc=True)

# # Convertir a la zona horaria deseada (ejemplo: Bogotá)
# df_final['datetime'] = df_final['datetime'].dt.tz_convert('America/Bogota')

# Guardar el DataFrame combinado en un nuevo archivo CSV
df_final.to_csv('D:\\UNIVALLE\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\dataframe_combinado.csv', index=False)

print("DataFrame combinado guardado como 'dataframe_combinado.csv'")
