import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf

# Función para calcular el NPV a lo largo de la vida útil
def calcular_NPV_por_año(tasa_descuento, crecimiento_demanda, vida_util, station_info):
    npv_por_año = []
    
    # Calcular máximo años de crecimiento de la demanda
    maximo_años_crecimiento_demanda = np.round(
        np.log10(24 / (station_info[4] * station_info[5])) / 
        np.log10(1 + crecimiento_demanda)
    )
    
    for año in range(vida_util):
        flujos_caja = [-station_info[1]]
        
        for t in range(año + 1):
            # Calcular ingresos anuales
            ingresos_anuales = (station_info[3] * station_info[4] * 
                                station_info[5] * station_info[6] * 365)

            # Ajustar ingresos según el crecimiento de la demanda
            if t > maximo_años_crecimiento_demanda and crecimiento_demanda >= 0.25:
                ingresos_anuales *= (1 + crecimiento_demanda) ** maximo_años_crecimiento_demanda
            else:
                ingresos_anuales *= (1 + crecimiento_demanda) ** t

            # Calcular flujo de caja
            flujo_caja = ingresos_anuales - station_info[0]
            if t == 9:
                flujo_caja -= station_info[1] * station_info[7]  # Upgrade percentage
            
            flujos_caja.append(flujo_caja)
        
        # Calcular NPV e IRR
        NPV = npf.npv(tasa_descuento, flujos_caja)
        npv_por_año.append(NPV)
    
    return npv_por_año, flujos_caja

def escenarios_NPV(tasa_descuento_rango, crecimiento_demanda_rango, 
                   vida_util_rango, station_info):
    # Crear una lista para almacenar los resultados
    resultados = []

    # Iterar sobre tasas de descuento y crecimiento de demanda
    for tasa_descuento in tasa_descuento_rango:
        for crecimiento_demanda in crecimiento_demanda_rango:
            # Calcular NPV por año y flujos de caja
            NPV_por_año, flujos_caja = calcular_NPV_por_año(
                tasa_descuento,
                crecimiento_demanda,
                vida_util_rango[-1], 
                station_info
            )
            # Almacenar los resultados en un diccionario
            resultados.append({
                'tasa_descuento': tasa_descuento,
                'costos_mantenimiento': station_info[0],
                'crecimiento_demanda': crecimiento_demanda,
                'inversion_inicial': station_info[1],
                'tipo_cargador': station_info[2],
                'vida_util': vida_util_rango,
                'flujos_caja': flujos_caja,
                'NPV': NPV_por_año,
                'NPV_final': NPV_por_año[-1]
            })

    return resultados


def graficar(df_resultados):
    # Análisis de sensibilidad - Graficar NPV por vida útil
    plt.figure(figsize=(10, 6))

    # Graficar NPV para cada resultado
    for _, row in df_resultados.iterrows():
        plt.plot(row['vida_util'], row['NPV'], label=f"Demand inc. {row['crecimiento_demanda']:.0%}, IRR {row['tasa_descuento']:.0%}")

    # Configurar etiquetas y título
    plt.xlabel('Service life (years)', fontsize=14, fontweight='bold')
    plt.ylabel('Net Present Value (NPV) (USD)', fontsize=14, fontweight='bold')
    plt.title(df_resultados['tipo_cargador'][0] + ' CS Sensitivity Analysis - NPV vs. Service Life', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid()
    plt.savefig(df_resultados['tipo_cargador'][0] + " VPN_All_Cases_10_Years.png")
    plt.show()

    # Encontrar índices de mejor y peor NPV_final
    mejor_idx = df_resultados['NPV_final'].idxmax()
    peor_idx = df_resultados['NPV_final'].idxmin()

    # Graficar comparación de flujos de caja - Mejor y Peor NPV_final
    plt.figure(figsize=(12, 6))

    # Graficar flujos de caja para el mejor y peor NPV_final
    for idx, color, label in zip([mejor_idx, peor_idx], ['green', 'red'], ['Best NPV_final', 'Worst NPV_final']):
        plt.bar(range(len(df_resultados['flujos_caja'].iloc[idx])),
                df_resultados['flujos_caja'].iloc[idx],
                label=f'{label}: {df_resultados["NPV_final"].iloc[idx]:.2f}',
                alpha=0.7, width=0.4, align='center' if idx == mejor_idx else 'edge', color=color)

    # Configurar título y etiquetas
    plt.title(df_resultados['tipo_cargador'][0] + ' CS Cash Flow - Best and Worst NPV_final', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Cash Flow', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12, title_fontsize='13', title='Legend', loc='best', frameon=True)

    # Configurar etiquetas de los ejes
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')

    plt.grid(True)
    plt.savefig(df_resultados['tipo_cargador'][0] + " Cash_Flow_Best_Worst.png", bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    # Leer el DataFrame de costos de cargadores
    filePath = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Total_costs_CS.csv'
    df_costs = pd.read_csv(filePath, sep=';')
    
    # Define una tasa de cambio
    T_C = 3951.65  # Promedio dólar durante 2024

    # Costos de sistemas PV (paneles solares)
    PV_costs = 0
    PV_install_Cost = 0

    # Filtrar costos de estaciones lentas
    df_costs = df_costs[df_costs['Charge_type'] != 'Slow']
    df_diferent_costs = df_costs.loc[~df_costs['Charger'].duplicated(keep='first')]
    df_diferent_costs = df_diferent_costs[df_diferent_costs['Charger'].notnull()]

    # Calcular inversión inicial con costos de instalación y paneles PV
    inversion_inicial_rango = (df_diferent_costs['Charger'].to_numpy() + 
                                df_diferent_costs['Installation'].to_numpy() + 
                                PV_costs + PV_install_Cost)

    # Asignar nombres a las inversiones iniciales
    inversion_inicial_name = ['Semifast_Basic', 'Semifast', 'Fast']

    # Leer el DataFrame de tarifas de energía de CEDENAR
    filePath = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Tarifas_energia.csv'
    df_tarifas = pd.read_csv(filePath, sep=',')
    
    # Tarifas de energía y carga
    tarifa_energia = 500 / T_C  # Costo promedio año 2024 kWh nivel de tensión 1
    tarifa_carga_semi = 1250 / T_C    # Para carga semirápida Enel X
    tarifa_carga_fast = 1450 / T_C    # Para carga semirápida Enel X
    ganancia_tarifa = [tarifa_carga_semi - tarifa_energia, tarifa_carga_fast - tarifa_energia]

    # Rango de variaciones para el análisis de sensibilidad
    tasa_descuento_rango = np.arange(0.05, 0.16, 0.05)  # del 5% al 20%
    costos_mantenimiento_rango = [400, 800]  # Sin PV
    crecimiento_demanda_rango = [0.05, 0.15, 0.25] 
    vida_util_rango = np.arange(1, 36, 1)  # Vida útil de 1 a 20 años
    
    # Información sobre cargas
    cargas_diarias_promedio_semi = 0.28 # dos cargas a la semana
    cargas_diarias_promedio_fast = 0.14 # una carga a la semana
    tiempo_carga_promedio_semi = 2 # dos horas
    tiempo_carga_promedio_fast = 0.5 # 30 min
    potencia_promedio_carga_semi = 5
    potencia_promedio_carga_fast = 42
    
    # Upgrade percentage
    
    upgrade_semi = 0.5
    upgrade_fast = 0.2

    # Groups input information by station type
    semi_fast_basic = [costos_mantenimiento_rango[0], 
                         inversion_inicial_rango[0], 
                         inversion_inicial_name[0], 
                         ganancia_tarifa[0], 
                         cargas_diarias_promedio_semi, 
                         tiempo_carga_promedio_semi, 
                         potencia_promedio_carga_semi, 
                         upgrade_semi] 
    semi_fast_complex = [costos_mantenimiento_rango[0], 
                         inversion_inicial_rango[1], 
                         inversion_inicial_name[1], 
                         ganancia_tarifa[0], 
                         cargas_diarias_promedio_semi, 
                         tiempo_carga_promedio_semi, 
                         potencia_promedio_carga_semi, 
                         upgrade_semi]
    fast = [costos_mantenimiento_rango[1], 
                         inversion_inicial_rango[2], 
                         inversion_inicial_name[2], 
                         ganancia_tarifa[1], 
                         cargas_diarias_promedio_fast, 
                         tiempo_carga_promedio_fast, 
                         potencia_promedio_carga_fast, 
                         upgrade_fast]

    # Calcular NPV para cada configuración
    df_semifast_Basic = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
                                                      crecimiento_demanda_rango, 
                                                      vida_util_rango,
                                                      semi_fast_basic))
    
    # Calcular NPV para cada configuración
    df_semifast_Complex = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
                                                      crecimiento_demanda_rango, 
                                                      vida_util_rango,
                                                      semi_fast_complex))
    
    # Calcular NPV para cada configuración
    df_fast = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
                                                      crecimiento_demanda_rango, 
                                                      vida_util_rango,
                                                      fast))
    graficar(df_semifast_Complex)
    graficar(df_fast)

    # Concatenar los dataframes y exportar resultados
    df_resultados = pd.concat([df_semifast_Basic, df_semifast_Complex, df_fast], ignore_index=True)
    df_resultados.to_csv('H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\Economic_results.csv', index=False)
