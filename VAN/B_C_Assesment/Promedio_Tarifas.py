import numpy as np
import pandas as pd

# Leer el DataFrame desde un archivo CSV
filePath = 'Tarifas_energia.csv'  # Costo de la energía CEDENAR
df = pd.read_csv(filePath, sep=',')

# Calcula la media de cada columna
Promedio_N_T_1 = df['Costo_COP/kWh_Nivel_Tension_1'].mean()
Promedio_N_T_2 = df['Costo_COP/kWh_Nivel_Tension_2'].mean()
Promedio_N_T_3 = df['Costo_COP/kWh_Nivel_Tension_3'].mean()

# Crear una nueva fila con los promedios
nueva_fila = pd.DataFrame([['Promedio', Promedio_N_T_1, Promedio_N_T_2, Promedio_N_T_3]], columns=df.columns)

# Concatenar la nueva fila al DataFrame original
df = pd.concat([df, nueva_fila], ignore_index=True)

print(df['Costo_COP/kWh_Nivel_Tension_1'].iloc[-1])

df.to_csv('Tarifas_energia.csv', index=False)