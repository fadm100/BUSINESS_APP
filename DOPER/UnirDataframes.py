import pandas as pd
import os

# Ruta base donde están los CSV
base_path = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\24-04-2025\\Dataframe\\ev_variable_results'

# Rango de archivos que quieres unir (EV0 a EV14)
file_indices = range(15)

# Lista para almacenar los dataframes
dataframes = []

for i in file_indices:
    file_name = f'battery_discharge_power_EV_EV{i}.csv'
    full_path = os.path.join(base_path, file_name)

    # Leer CSV completo, pero nos quedamos solo con datetime y la segunda columna
    df = pd.read_csv(full_path)

    # Identificar la segunda columna (índice 1)
    second_col = df.columns[1]
    
    # Renombrar la segunda columna con nombre del archivo sin extensión
    col_name = os.path.splitext(file_name)[0]
    df = df[['datetime', second_col]].rename(columns={second_col: col_name})
    
    # Convertir datetime y poner como índice
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    dataframes.append(df)

# Combinar todos los dataframes por datetime
merged_df = pd.concat(dataframes, axis=1)

# Guardar resultado
output_file = os.path.join(base_path, 'battery_discharge_power_EV.csv')
merged_df.to_csv(output_file)
