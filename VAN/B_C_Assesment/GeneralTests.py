# import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# import matplotlib.gridspec as gridspec

# # Cargar datos
# filePath = 'G:\\My Drive\\Artículos tesis\\DESARROLLO\\Informe 2024-2\\Parque_automotor_EV.csv'
# df_growth = pd.read_csv(filePath, sep=';')

# # Calcular el incremento porcentual
# df_growth['Incremento (%)'] = df_growth['Cantidad'].pct_change() * 100

# # Crear una figura más compacta y especificar la estructura del grid
# fig = plt.figure(figsize=(12, 8))  # Tamaño reducido de la figura
# gs = gridspec.GridSpec(2, 2, width_ratios=[2, 3])  # Dos filas y dos columnas, con el mapa más ancho

# # Primer subplot: gráfico de barras y líneas
# ax1 = fig.add_subplot(gs[0, 0])  # Primer gráfico en la fila superior izquierda
# color = '#296073'
# bars = ax1.bar(df_growth['Año'], df_growth['Cantidad'], color=color, label='Cantidad')
# ax1.set_xlabel('Year\na)')
# ax1.set_ylabel('Registered EVs', color=color)
# ax1.tick_params(axis='y', labelcolor=color)
# # ax1.set_title('Increase of EVs in Colombia', fontsize=12)

# # Añadir etiquetas sobre las barras
# for bar in bars:
#     yval = bar.get_height()
#     ax1.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=8)

# # Línea del incremento
# ax2 = ax1.twinx()
# color = 'black'
# ax2.plot(df_growth['Año'], df_growth['Incremento (%)'], color=color, marker='o', label='Incremento (%)')
# ax2.set_ylabel('Annual increase (%)', color=color)
# ax2.tick_params(axis='y', labelcolor=color)

# # Segundo subplot: gráfico circular
# labels = ['ICE', 'Hybrid', 'EV']
# sizes = [98.75, 1.05, 0.2]
# colors = ['#e9e9df', '#00a8de', '#05e72c']
# explode = (0, 0.05, 0.2)
# ax3 = fig.add_subplot(gs[1, 0])  # Segundo gráfico en la fila inferior izquierda
# ax3.pie(
#     sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True
# )
# ax3.set_xlabel('b)')
# # ax3.set_title('Distribution of Vehicle Types in Colombia (2024)', fontsize=12)

# # Tercer subplot: mapa de Colombia
# ax4 = fig.add_subplot(gs[:, 1])  # El mapa ocupa ambas filas a la derecha
# m = Basemap(projection='merc', llcrnrlat=-4, urcrnrlat=14, llcrnrlon=-82, urcrnrlon=-66, resolution='i', ax=ax4)
# m.drawmapboundary(fill_color='#92d6ec')
# m.fillcontinents(color='#f2fcef', lake_color='#41493f')
# m.drawcoastlines()
# m.drawcountries(linewidth=2, color='black')
# m.drawstates(linewidth=1, linestyle='dotted', color='grey')

# ciudades = {
#     'Bogotá - 49%': (-74.0721, 4.7110, 49),
#     'Medellín - 27%': (-75.5636, 6.2518, 27),
#     'Cali - 5.7%': (-76.5225, 3.4516, 6),
#     'Pasto - 0.1%': (-77.2811, 1.21361, 0.1)
# }

# for ciudad, (lon, lat, size) in ciudades.items():
#     x, y = m(lon, lat)
#     ax4.plot(x, y, 'ro', markersize=size)
#     ax4.text(x, y, ciudad, fontsize=8, ha='left')

# ax4.set_xlabel('c)')
# # ax4.set_title('Colombian Map with Vehicle Proportions', fontsize=12)

# # Ajustar el layout general
# fig.tight_layout(pad=2.0)  # Más espacio entre los subplots

# # Guardar la figura
# plt.savefig("VE_Colombian_layout_compact.png", bbox_inches='tight')

# # Mostrar la figura
# plt.show()

############# figuras con areas sombreadas

import numpy as np
import matplotlib.pyplot as plt

# Datos simulados (ajústalos según sea necesario)
horas = np.arange(0, 24, 1)  # Horas del día (intervalos de una hora)

# Número de vehículos activos por hora
vehiculos_pasajeros = np.maximum(0, np.sin((horas - 12) / 8 * np.pi) * 6)
vehiculos_reparto = np.maximum(0, np.sin((horas - 8) / 8 * np.pi) * 10)

# Crear la figura
plt.figure(figsize=(10, 6))

# Gráfico de barras apiladas
plt.bar(
    horas, vehiculos_reparto, label="Vehículos de Reparto", color="lightblue", width=1, edgecolor="none"
)
plt.bar(
    horas, vehiculos_pasajeros, label="Vehículos de Transporte de Pasajeros", color="blue", width=1, edgecolor="none"
)

# Configurar etiquetas y estilo
plt.title("Patrones de conducción por tipo de vehículo", fontsize=14)
plt.xlabel("Hora del día", fontsize=12)
plt.ylabel("Número de vehículos activos", fontsize=12)
plt.xticks(range(0, 25, 2))  # Mostrar marcas cada 2 horas
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Mostrar el gráfico
plt.tight_layout()
plt.show()
