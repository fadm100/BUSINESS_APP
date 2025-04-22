# import pandas as pd

# # Cargar el archivo
# df = pd.read_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\21-04-2025\\buses_availability_5min.csv', sep=";", encoding='utf-8')
# print('Encabezados', df.columns.tolist())

# # Creamos un nuevo DataFrame, copiando el original
# df_invertido = df.copy()

# # Invertimos solo las columnas que contienen datos binarios (sin incluir 'time_interval')
# columnas_binarias = df.columns.drop('time_interval')
# df_invertido[columnas_binarias] = 1 - df_invertido[columnas_binarias]

# # Guardar el resultado
# df_invertido.to_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\21-04-2025\\buses_availability_5min_inverted.csv', sep=";", index=False)


################################

import pandas as pd

# Cargar los datos
df1 = pd.read_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\21-04-2025\\buses_availability_5min_inverted.csv', sep=";", encoding='utf-8')  # dataframe con battery_EV
df2 = pd.read_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\21-04-2025\\energy_steps5min.csv', sep=";", encoding='utf-8')  # dataframe con Bus

# Asegurar que la columna de tiempo esté alineada
df2["time_interval"] = df2["time_interval"].astype(int)
df = pd.merge(df1, df2, on="time_interval")

# Tomar sólo las columnas correspondientes a buses y baterías
battery_columns = [col for col in df.columns if "battery" in col]
bus_columns = [col for col in df.columns if "Bus" in col]

# Multiplicar elemento a elemento
df_result = df.copy()
for i in range(15):
    battery_col = f"battery_EV{i}_avail"
    bus_col = f"Bus_{i}"
    result_col = f"Result_EV{i}"
    df_result[result_col] = df[battery_col] * df[bus_col]

# Incluir solo columna de tiempo y resultados
final_df = df_result[["time_interval"] + [f"Result_EV{i}" for i in range(15)]]

final_df.to_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\21-04-2025\\energy_steps5min_new.csv', sep=";", index=False)

