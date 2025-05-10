import pandas as pd
import matplotlib.pyplot as plt

# Ruta al archivo CSV combinado
csv_path = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\25-04-2025\\Dataframe\\ev_variable_results\\battery_discharge_power_EV.csv'

# Cargar el dataframe
df = pd.read_csv(csv_path, index_col='datetime', parse_dates=True)

# Filtrar por rango de tiempo
start_time = '2019-01-01 16:50:00+00:00'
end_time = '2019-01-01 18:25:00+00:00'
filtered_df = df.loc[start_time:end_time]

# Graficar
plt.figure(figsize=(14, 6))

for column in filtered_df.columns:
    plt.plot(filtered_df.index, filtered_df[column], label=column)

plt.title('Battery Discharge Power (VE) entre 16:50 y 18:25')
plt.xlabel('Tiempo')
plt.ylabel('Potencia de descarga (kW)')
plt.legend(loc='upper right', fontsize='small', ncol=2)
plt.grid(True)
plt.tight_layout()
plt.show()

# Contar cuántos valores distintos de cero hay por fila (por instante de tiempo)
nonzero_counts = (filtered_df != 0).sum(axis=1)

# Graficar como histograma de líneas
plt.figure(figsize=(14, 5))
plt.plot(nonzero_counts.index, nonzero_counts.values, marker='o', linestyle='-')
plt.title('Cantidad de Vehículos Eléctricos descargando (Potencia ≠ 0)')
plt.xlabel('Tiempo')
plt.ylabel('Número de EVs descargando')
plt.grid(True)
plt.tight_layout()
plt.show()