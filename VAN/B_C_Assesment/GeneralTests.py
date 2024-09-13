import tabula
import pandas as pd
import math

############## Calcula el porcentaje de incremento de vehículos ################
# Leer el DataFrame de costos de cargadores
filePath = 'evProjections.csv'  # Costos de un solo cargador, la tabla contiene varios tipos de cargadores divididos entre lentos, semirápidos y rapídos
df = pd.read_csv(filePath, sep=',')

# Calcular el porcentaje de incremento para cada columna
df['Taxis projection % Incremento'] = df['Taxis projection'].pct_change() * 100
df['Annual EV % Incremento'] = df['Annual EV'].pct_change() * 100

# porcentaje de incremento de demanda estaciones de carga
crecimiento_demanda_rango = [0.05, 0.15, 0.25]

# Uso de estaciones de carga año 0
cargas_semana_type2 = 7 # 2 cargas a la semana
cargas_diarias_type2 = cargas_semana_type2 / 7
cargas_semana_CCS = 2 # una carga a la semana
cargas_diarias_CCS = cargas_semana_CCS / 7

# Máximo número de cargas diarias
tiempo_carga_type2 = 2 # horas
max_cargas_type2 = 24 / tiempo_carga_type2
tiempo_carga_CCS = 0.5 # horas
max_cargas_CCS = 24 / tiempo_carga_CCS

# Años de análisis
años_type2 = 20
años_CCS = 25

# Proyeccioes de uso de estaciones de carga
proyeccion_type2 = []
proyeccion_type2_semana = []
utilization_rate_type2 = []
for t in range(años_type2 + 1):
    proyeccion = cargas_diarias_type2 * (1 + crecimiento_demanda_rango[2]) ** t
    if proyeccion <= max_cargas_type2:
        proyeccion_type2.append(proyeccion)
        proyeccion_type2_semana.append(proyeccion * 7)
        utilization_rate_type2.append(proyeccion * tiempo_carga_type2 / 24)
    else:
        proyeccion_type2.append(max_cargas_type2)
        proyeccion_type2_semana.append(max_cargas_type2 * 7)
        utilization_rate_type2.append(max_cargas_type2 * tiempo_carga_type2 / 24)

proyeccion_CCS = []
proyeccion_CCS_semana = []
utilization_rate_CCS = []
for t in range(años_CCS + 1):
    proyeccion = cargas_diarias_CCS * (1 + crecimiento_demanda_rango[2]) ** t
    if proyeccion <= max_cargas_CCS:
        proyeccion_CCS.append(proyeccion)
        proyeccion_CCS_semana.append(proyeccion * 7)
        utilization_rate_CCS.append(proyeccion * tiempo_carga_CCS / 24)
    else:
        proyeccion_CCS.append(max_cargas_CCS)
        proyeccion_CCS_semana.append(max_cargas_CCS * 7)
        utilization_rate_CCS.append(max_cargas_CCS * tiempo_carga_CCS / 24)

# guardar en el dataframe CS es Charging Station
df['type 2 projection from CS'] = pd.DataFrame(proyeccion_type2)
df['CCS projection from CS'] = pd.DataFrame(proyeccion_CCS)
df['type 2 projection from CS week'] = pd.DataFrame(proyeccion_type2_semana)
df['CCS projection from CS week'] = pd.DataFrame(proyeccion_CCS_semana)
df['type 2 utilization rate'] = pd.DataFrame(utilization_rate_type2)
df['CCS utilization rate'] = pd.DataFrame(utilization_rate_CCS)

# porcentaje diario de taxis que usaría las estaciones
df['% taxis usando type 2'] = df['type 2 projection from CS'] / df['Annual EV'] * 100
df['% taxis usando CCS'] = df['CCS projection from CS'] / df['Annual EV'] * 100

# calculo 1% de taxis EV cada año
df['taxis EV 1%'] = df['Annual EV'] * 0.01

# Mostrar el resultado
print(df[['Year', 'Annual EV', 'taxis EV 1%', '# CS L2-M2&3', 'type 2 projection from CS', 'type 2 utilization rate', '% taxis usando type 2', '# CS L3', 'CCS projection from CS', 'CCS utilization rate', '% taxis usando CCS']].round(2))
