# import tabula
import pandas as pd
import math
import matplotlib.pyplot as plt

# # # ############## Calcula el porcentaje de incremento de vehículos ################
# # # # Leer el DataFrame de costos de cargadores
# # # filePath = 'H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\evProjections.csv'  # Costos de un solo cargador, la tabla contiene varios tipos de cargadores divididos entre lentos, semirápidos y rapídos
# # # df = pd.read_csv(filePath, sep=',')

# # # # Calcular el porcentaje de incremento para cada columna
# # # df['Taxis projection % Incremento'] = df['Taxis projection'].pct_change() * 100
# # # df['Annual EV % Incremento'] = df['Annual EV'].pct_change() * 100

# # # # porcentaje de incremento de demanda estaciones de carga
# # # crecimiento_demanda_rango = [0.05, 0.15, 0.25]

# # # # Uso de estaciones de carga año 0
# # # cargas_semana_type2 = 7 # 2 cargas a la semana
# # # cargas_diarias_type2 = cargas_semana_type2 / 7
# # # cargas_semana_CCS = 2 # una carga a la semana
# # # cargas_diarias_CCS = cargas_semana_CCS / 7

# # # # Máximo número de cargas diarias
# # # tiempo_carga_type2 = 2 # horas
# # # max_cargas_type2 = 24 / tiempo_carga_type2
# # # tiempo_carga_CCS = 0.5 # horas
# # # max_cargas_CCS = 24 / tiempo_carga_CCS

# # # # Años de análisis
# # # años_type2 = 20
# # # años_CCS = 25

# # # # Proyeccioes de uso de estaciones de carga
# # # proyeccion_type2 = []
# # # proyeccion_type2_semana = []
# # # utilization_rate_type2 = []
# # # for t in range(años_type2 + 1):
# # #     proyeccion = cargas_diarias_type2 * (1 + crecimiento_demanda_rango[2]) ** t
# # #     if proyeccion <= max_cargas_type2:
# # #         proyeccion_type2.append(proyeccion)
# # #         proyeccion_type2_semana.append(proyeccion * 7)
# # #         utilization_rate_type2.append(proyeccion * tiempo_carga_type2 / 24)
# # #     else:
# # #         proyeccion_type2.append(max_cargas_type2)
# # #         proyeccion_type2_semana.append(max_cargas_type2 * 7)
# # #         utilization_rate_type2.append(max_cargas_type2 * tiempo_carga_type2 / 24)

# # # proyeccion_CCS = []
# # # proyeccion_CCS_semana = []
# # # utilization_rate_CCS = []
# # # for t in range(años_CCS + 1):
# # #     proyeccion = cargas_diarias_CCS * (1 + crecimiento_demanda_rango[2]) ** t
# # #     if proyeccion <= max_cargas_CCS:
# # #         proyeccion_CCS.append(proyeccion)
# # #         proyeccion_CCS_semana.append(proyeccion * 7)
# # #         utilization_rate_CCS.append(proyeccion * tiempo_carga_CCS / 24)
# # #     else:
# # #         proyeccion_CCS.append(max_cargas_CCS)
# # #         proyeccion_CCS_semana.append(max_cargas_CCS * 7)
# # #         utilization_rate_CCS.append(max_cargas_CCS * tiempo_carga_CCS / 24)

# # # # guardar en el dataframe CS es Charging Station
# # # df['type 2 projection from CS'] = pd.DataFrame(proyeccion_type2)
# # # df['CCS projection from CS'] = pd.DataFrame(proyeccion_CCS)
# # # df['type 2 projection from CS week'] = pd.DataFrame(proyeccion_type2_semana)
# # # df['CCS projection from CS week'] = pd.DataFrame(proyeccion_CCS_semana)
# # # df['type 2 utilization rate'] = pd.DataFrame(utilization_rate_type2)
# # # df['CCS utilization rate'] = pd.DataFrame(utilization_rate_CCS)

# # # # porcentaje diario de taxis que usaría las estaciones
# # # df['% taxis usando type 2'] = df['type 2 projection from CS'] / df['Annual EV'] * 100
# # # df['% taxis usando CCS'] = df['CCS projection from CS'] / df['Annual EV'] * 100

# # # # calculo 1% de taxis EV cada año
# # # df['taxis EV 1%'] = df['Annual EV'] * 0.01

# # # # Mostrar el resultado
# # # print(df[['Year', 'Annual EV', 'taxis EV 1%', '# CS L2-M2&3', 'type 2 projection from CS', 'type 2 utilization rate', '% taxis usando type 2', '# CS L3', 'CCS projection from CS', 'CCS utilization rate', '% taxis usando CCS']].round(2))

###########################################################

# # filePath = 'H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Informe 2024-2\\Datos_A_data_driven_typology.csv'
# # # filePath = 'H:\\My Drive\Artículos tesis\\DESARROLLO\\Informe 2024-2\\Datos_A_data_driven_typology.csv'
# # df_datos = pd.read_csv(filePath, sep=';')

# # # Crear gráfico de barras
# # plt.figure(figsize=(8,6))
# # plt.bar(df_datos['User_behavior_type'], df_datos['Charging_time'], color='darkseagreen')

# # # Etiquetas del gráfico
# # plt.xlabel('User Behavior Type')
# # plt.ylabel('Charging Time (hours)')
# # plt.title('Charging Time vs User Behavior Type')

# # plt.savefig("Charging_time.png", bbox_inches='tight')

# # # Mostrar gráfico
# # plt.show()

##########################################################
filePath = 'H:\\Mi unidad\Artículos tesis\\DESARROLLO\\Informe 2024-2\\Parque_automotor_EV.csv'
df_growth = pd.read_csv(filePath, sep=';')

# Calcular el incremento porcentual
df_growth['Incremento (%)'] = df_growth['Cantidad'].pct_change() * 100

print(df_growth)

# Crear una nueva figura y eje
fig, ax1 = plt.subplots(figsize=(10, 6))

# Gráfico de barras para la cantidad por año en el primer eje y
color = '#296073'
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Registered EVs', color=color, fontsize=14)
bars = ax1.bar(df_growth['Año'], df_growth['Cantidad'], color=color, label='Cantidad')
ax1.tick_params(axis='y', labelcolor=color)

# Añadir etiquetas de cantidad sobre cada barra con mayor tamaño de fuente
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=12)

# Crear un segundo eje y, compartiendo el mismo eje x
ax2 = ax1.twinx()
color = 'black'
ax2.set_ylabel('Annual increase (%)', color=color, fontsize=14)
line, = ax2.plot(df_growth['Año'], df_growth['Incremento (%)'], color=color, marker='o', label='Incremento (%)')
ax2.tick_params(axis='y', labelcolor=color)

# Añadir etiquetas de porcentaje de incremento sobre cada punto con mayor tamaño de fuente
for i, txt in enumerate(df_growth['Incremento (%)'].round(2)):
    if pd.notna(txt):  # Solo mostrar si no es NaN (primer valor es NaN)
        ax2.text(df_growth['Año'][i], df_growth['Incremento (%)'][i], f'{txt:.2f}%', 
                 ha='center', va='bottom', color=color, fontsize=12)

# Configurar los límites del eje de incremento porcentual entre 0 y 100%
ax2.set_ylim(0, 100)

# Título del gráfico con mayor tamaño de fuente
plt.title('Increase of EVs in Colombia', fontsize=16)

# Agregar cuadrícula al gráfico para mejor visibilidad
ax1.grid(True, linestyle='--', alpha=0.6)

# Ajustar el layout
fig.tight_layout()

plt.savefig("VE_Colombian_increase.png", bbox_inches='tight')

# Mostrar gráfico
plt.show()

#####################################################################################

# Datos
labels = ['Conventional fuel vehicles', 'Hybrid Vehicles', 'Electric Vehicles']
sizes = [98.75, 1.05, 0.2]  # Porcentajes
colors = ['#e9e9df', '#00a8de', '#05e72c']  # Colores para cada sección
explode = (0, 0.05, 0.2)  # Destacar la sección de los vehículos eléctricos

# Crear la gráfica de torta
plt.figure(figsize=(7, 7))  # Tamaño de la figura
plt.pie(
    sizes, 
    explode=explode, 
    labels=labels, 
    colors=colors, 
    autopct='%1.1f%%', 
    startangle=90, 
    shadow=True, 
    textprops={'fontsize': 16}  # Tamaño de los textos
)

# # Añadir título con un tamaño de fuente más grande
# plt.title('Distribución del Parque Automotor en Colombia (2024)', fontsize=18)

plt.savefig("VE_Colombian_proportion.png", bbox_inches='tight')

# Mostrar la gráfica
plt.show()
