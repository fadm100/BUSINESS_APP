import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy_financial as npf
import seaborn as sns

# Leer el DataFrame desde un archivo CSV
filePath = 'Total_costs_CS.csv'  # Reemplaza 'ruta/al/archivo.csv' con la ruta real de tu archivo
df_costs = pd.read_csv(filePath, sep=';')

df_diferent_costs = df_costs.loc[~df_costs['Charger'].duplicated(keep = 'first')]
df_diferent_costs = df_diferent_costs[df_diferent_costs['Charger'].notnull()]

# Parámetros iniciales
inversion_inicial_rango = df_diferent_costs['Charger'].to_numpy()  # USD
tarifa_carga = 5  # USD por carga
cargas_diarias_promedio = 10

# Rango de variaciones para el análisis de sensibilidad
tasa_descuento_rango = np.arange(0.05, 0.2, 0.05)  # del 5% al 20% --> 9% Colombia 2022 --> https://2022.dnp.gov.co/DNP-Redes/Revista-Juridica/Paginas/Adopci%C3%B3n-de-la-Tasa-Social-de-Descuento-para-la-evaluaci%C3%B3n-de-proyectos-de-inversi%C3%B3n.aspx
costos_operativos_rango = [2000, 10000, 50000, 100000]  # Un solo valor para simplificar
crecimiento_demanda_rango = [0.01, 0.05, 0.1, 0.15]  # Un solo valor para simplificar
vida_util_rango = np.arange(1, 11, 1)  # Vida útil de 1 a 10 años

# Función para calcular el NPV a lo largo de la vida útil
def calcular_NPV_por_año(tasa_descuento, costos_operativos, crecimiento_demanda, inversion_inicial, vida_util):
    npv_por_año = []
    for año in range(vida_util):
        flujos_caja = [-inversion_inicial]
        for t in range(año + 1):
            ingresos_anuales = tarifa_carga * cargas_diarias_promedio * 365
            ingresos_anuales *= (1 + crecimiento_demanda) ** t
            flujo_caja = ingresos_anuales - costos_operativos
            flujos_caja.append(flujo_caja)
        
        IRR = npf.irr(flujos_caja)
        NPV = npf.npv(tasa_descuento, flujos_caja)
        npv_por_año.append(NPV)
    return npv_por_año, flujos_caja

# Crear un DataFrame para almacenar los resultados
resultados = []

for tasa_descuento in tasa_descuento_rango:
    for costos_operativos in costos_operativos_rango:
        for crecimiento_demanda in crecimiento_demanda_rango:
            for inversion_inicial in inversion_inicial_rango:
                NPV_por_año, flujos_caja = calcular_NPV_por_año(tasa_descuento, costos_operativos, crecimiento_demanda, inversion_inicial, vida_util_rango[-1])
                resultados.append({
                    'tasa_descuento': tasa_descuento,
                    'costos_operativos': costos_operativos,
                    'crecimiento_demanda': crecimiento_demanda,
                    'inversion_inicial': inversion_inicial,
                    'vida_util': vida_util_rango,
                    'flujos_caja': flujos_caja,
                    'NPV': NPV_por_año,
                    'NPV_final': NPV_por_año[-1]
                })

df_resultados = pd.DataFrame(resultados)
# Exportar el DataFrame a CSV
df_resultados.to_csv('Economic_results.csv', index=False)

# Listado de columnas a graficar
columnas = ['NPV_final']
# Crear histogramas para cada columna
df_resultados[columnas].hist(bins=15, figsize=(15, 10), layout=(1, 1), edgecolor='black')
plt.suptitle('Histogramas de Variables')
plt.show()

# Crear gráfico de dispersión 3D con cambio de colores tasa_descuento, costos_operativos y NPV
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
npv_min = df_resultados['NPV_final'].min()
npv_max = df_resultados['NPV_final'].max()
scatter = ax.scatter(df_resultados['tasa_descuento'], df_resultados['costos_operativos'], df_resultados['NPV_final'],
                     c=df_resultados['NPV_final'], marker='o', cmap='viridis', vmin=npv_min, vmax=npv_max)

ax.set_xlabel('Tasa de Descuento')
ax.set_ylabel('Costos Operativos')
ax.set_zlabel('NPV Final')
ax.set_title('Gráfica de Dispersión 3D: Tasa de Descuento, Costos Operativos y NPV Final')
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('NPV Final')
plt.show()

# Crear gráfico de dispersión 3D con cambio de colores tasa_descuento, inversion_inicial y NPV
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
npv_min = df_resultados['NPV_final'].min()
npv_max = df_resultados['NPV_final'].max()
scatter = ax.scatter(df_resultados['tasa_descuento'], df_resultados['inversion_inicial'], df_resultados['NPV_final'],
                     c=df_resultados['NPV_final'], marker='o', cmap='viridis', vmin=npv_min, vmax=npv_max)

ax.set_xlabel('Tasa de Descuento')
ax.set_ylabel('Inversión Inicial')
ax.set_zlabel('NPV Final')
ax.set_title('Gráfica de Dispersión 3D: Tasa de Descuento, Inversión Inicial y NPV Final')
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('NPV Final')
plt.show()

# Crear gráfico de dispersión 3D con cambio de colores tasa_descuento, crecimiento_demanda y NPV
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
npv_min = df_resultados['NPV_final'].min()
npv_max = df_resultados['NPV_final'].max()
scatter = ax.scatter(df_resultados['tasa_descuento'], df_resultados['crecimiento_demanda'], df_resultados['NPV_final'],
                     c=df_resultados['NPV_final'], marker='o', cmap='viridis', vmin=npv_min, vmax=npv_max)

ax.set_xlabel('Tasa de Descuento')
ax.set_ylabel('Crecimiento Demanda')
ax.set_zlabel('NPV Final')
ax.set_title('Gráfica de Dispersión 3D: Tasa de Descuento, Crecimiento Demanda y NPV Final')
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('NPV Final')
plt.show()

# # Gráfico de dispersión entre tasa_descuento y NPV_final
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='tasa_descuento', y='NPV_final', data=df_resultados)
# plt.title('Relación entre Tasa de Descuento y NPV Final')
# plt.show()

# # Gráfico de dispersión entre inversion_inicial y NPV_final
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='inversion_inicial', y='NPV_final', data=df_resultados)
# plt.title('Relación entre Inversión Inicial y NPV Final')
# plt.show()

# # Gráfico de barras para NPV_final en diferentes escenarios de tasa_descuento
# plt.figure(figsize=(10, 6))
# sns.barplot(x='tasa_descuento', y='NPV_final', data=df_resultados)
# plt.title('NPV Final por Tasa de Descuento')
# plt.show()

# # Gráfico de barras para NPV_final en diferentes escenarios de crecimiento_demanda
# plt.figure(figsize=(10, 6))
# sns.barplot(x='crecimiento_demanda', y='NPV_final', data=df_resultados)
# plt.title('NPV Final por Crecimiento de Demanda')
# plt.show()

# # Listado de columnas a graficar
# columnas = ['tasa_descuento', 'costos_operativos', 'crecimiento_demanda', 'inversion_inicial', 'NPV_final']
# # Matriz de correlación
# plt.figure(figsize=(10, 8))
# sns.heatmap(df_resultados[columnas].corr(), annot=True, cmap='coolwarm', fmt='.2f')
# plt.title('Matriz de Correlación entre Variables')
# plt.show()

# # Gráfico de línea para ver cómo varía NPV_final con el cambio de tasa_descuento
# plt.figure(figsize=(10, 6))
# sns.lineplot(x='tasa_descuento', y='NPV_final', data=df_resultados)
# plt.title('NPV Final vs Tasa de Descuento')
# plt.show()

# # Gráfico de línea para ver cómo varía NPV_final con el cambio de crecimiento_demanda
# plt.figure(figsize=(10, 6))
# sns.lineplot(x='crecimiento_demanda', y='NPV_final', data=df_resultados)
# plt.title('NPV Final vs Crecimiento de Demanda')
# plt.show()


# Análisis de sensibilidad - Graficar NPV por vida útil
# fig, ax = plt.subplots(figsize=(10, 6))

# for index, row in df_resultados.iterrows():
#     # ax.plot(row['vida_util'], row['NPV'], label=f"Tasa Desc. {row['tasa_descuento']:.0%}, Costos Oper. {row['costos_operativos']} USD, Crec. Demanda {row['crecimiento_demanda']:.0%}, Inv. Inicial {row['inversion_inicial']} USD")
#     ax.plot(row['vida_util'], row['NPV'], label=f"Inv. Inicial {row['inversion_inicial']} USD, Tasa Desc. {row['tasa_descuento']:.0%}")

# ax.set_xlabel('Vida Útil (años)')
# ax.set_ylabel('Valor Presente Neto (NPV) (USD)')
# ax.set_title('Análisis de Sensibilidad - NPV vs Vida Útil')
# ax.legend()
# ax.grid()
# plt.savefig("VPN_10_Years.png")
# plt.show()

# # Análisis de sensibilidad - Graficar flujos de caja anuales
# fig, axs = plt.subplots(len(tasa_descuento_rango), 1, figsize=(10, 15), sharex=True)
# time = np.arange(0, 11, 1)

# for index, (tasa_descuento, ax) in enumerate(zip(tasa_descuento_rango, axs)):
#     for idx, row in df_resultados[df_resultados['tasa_descuento'] == tasa_descuento].iterrows():
#         bars = ax.bar(time, row['flujos_caja'], label=f"Costos Oper. {row['costos_operativos']} USD, Crec. Demanda {row['crecimiento_demanda']:.0%}")
#         ax.axhline(0, color='black', linewidth=0.8)
#         ax.set_ylabel('Flujo de Caja (USD)')
#         ax.set_title(f'Flujos de Caja Anuales - Tasa Desc. {tasa_descuento:.0%}')
#         ax.legend()
#         if index == len(tasa_descuento_rango) - 1:
#             ax.set_xlabel('Años')
        
#         # Agregar etiquetas de texto encima de cada barra
#         for bar in bars:
#             height = bar.get_height()
#             ax.annotate(f'{height:.2f}',
#                         xy=(bar.get_x() + bar.get_width() / 2, height),
#                         xytext=(0, 3),  # 3 points vertical offset
#                         textcoords="offset points",
#                         ha='center', va='bottom')

# plt.tight_layout()
# # Guardar la figura en el disco duro en formato PNG
# plt.savefig('CashFlow_10_Years.png')
# plt.show()
