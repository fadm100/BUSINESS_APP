import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros iniciales
inversion_inicial = 100000  # USD
tarifa_carga = 5  # USD por carga
cargas_diarias_promedio = 10
vida_util = 10  # Vida útil de 10 años

# Rango de variaciones para el análisis de sensibilidad
tasa_descuento_rango = np.arange(0.05, 0.2, 0.05)  # del 5% al 20%
costos_operativos_rango = [10000]  # Un solo valor para simplificar
crecimiento_demanda_rango = [0.15]  # Un solo valor para simplificar

# Función para calcular los flujos de caja por año
def calcular_flujos_caja_anuales(tasa_descuento, costos_operativos, crecimiento_demanda, vida_util):
    flujos_caja_anuales = []
    van_por_año = []
    ingresos_acumulados = -inversion_inicial  # Ingresos iniciales negativos debido a la inversión

    for año in range(vida_util):
        ingresos_anuales = tarifa_carga * cargas_diarias_promedio * 365
        ingresos_anuales *= (1 + crecimiento_demanda) ** año
        flujo_caja = ingresos_anuales - costos_operativos
        ingresos_acumulados += flujo_caja
        flujos_caja_descuentados = flujo_caja / (1 + tasa_descuento) ** (año + 1)
        
        if ingresos_acumulados > 0 and not any(van_por_año):  # Encuentra el primer año en que el ingreso acumulado es positivo
            punto_equilibrio = año + 1
        else:
            punto_equilibrio = vida_util  # Si nunca es positivo dentro de la vida útil, se fija en el último año
            
        flujos_caja_anuales.append(flujo_caja)
        van_por_año.append((sum(van_por_año) if año else 0) + flujos_caja_descuentados)
        
    return flujos_caja_anuales, van_por_año, punto_equilibrio

# Crear un DataFrame para almacenar los resultados
resultados = []

for tasa_descuento in tasa_descuento_rango:
    for costos_operativos in costos_operativos_rango:
        for crecimiento_demanda in crecimiento_demanda_rango:
            flujos_caja_anuales, van_por_año, punto_equilibrio = calcular_flujos_caja_anuales(
                tasa_descuento, costos_operativos, crecimiento_demanda, vida_util
            )
            resultados.append({
                'tasa_descuento': tasa_descuento,
                'costos_operativos': costos_operativos,
                'crecimiento_demanda': crecimiento_demanda,
                'vida_util': np.arange(1, vida_util + 1),
                'flujos_caja': flujos_caja_anuales,
                'VAN': van_por_año,
                'punto_equilibrio': punto_equilibrio
            })

df_resultados = pd.DataFrame(resultados)

# Análisis de sensibilidad - Graficar flujos de caja anuales en una sola figura
fig, ax = plt.subplots(figsize=(12, 8))

colors = plt.cm.viridis(np.linspace(0, 1, len(tasa_descuento_rango)))

for index, tasa_descuento in enumerate(tasa_descuento_rango):
    for idx, row in df_resultados[df_resultados['tasa_descuento'] == tasa_descuento].iterrows():
        bars = ax.bar(row['vida_util'] + index * 0.1, row['flujos_caja'], width=0.1, color=colors[index],
                      label=f"Tasa Desc. {row['tasa_descuento']:.0%}")
        # for bar in bars:
        #     height = bar.get_height()
        #     ax.annotate(f'{height:.2f}',
        #                 xy=(bar.get_x() + bar.get_width() / 2, height),
        #                 xytext=(0, 3),  # 3 points vertical offset
        #                 textcoords="offset points",
        #                 ha='center', va='bottom')

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xlabel('Años')
ax.set_ylabel('Flujo de Caja (USD)')
ax.set_title('Flujos de Caja Anuales - Análisis de Sensibilidad por Tasa de Descuento')
ax.legend()
plt.tight_layout()
plt.show()
