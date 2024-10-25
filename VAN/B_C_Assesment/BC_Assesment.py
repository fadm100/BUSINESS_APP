import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf
import json

# Función para calcular el NPV a lo largo de la vida útil
def calcular_NPV_por_año(tasa_descuento, crecimiento_demanda, vida_util, station_info, PV_data, fast_info):
    npv_por_año = []
    
    # Calcular máximo años de crecimiento de la demanda
    maximo_años_crecimiento_demanda = np.round(
        np.log10(24 / (station_info[5] * station_info[6])) / 
        np.log10(1 + crecimiento_demanda)
    )
    
    for año in range(vida_util):
        flujos_caja = [-station_info[1] - PV_data['Costo compra'] / T_C - PV_data['Costo instalación'] / T_C]
        
        for t in range(año + 1):
            if t < 40:
                # cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga
                consumo = station_info[5] * station_info[6] * station_info[7]

                # Ajustar ingresos según el crecimiento de la demanda
                if t > maximo_años_crecimiento_demanda and crecimiento_demanda >= 0.25:
                    consumo *= (1 + crecimiento_demanda) ** maximo_años_crecimiento_demanda
                else:
                    consumo *= (1 + crecimiento_demanda) ** t

                generacion_consumo = PV_data['Promedio kWh/dia'] - consumo

                if generacion_consumo > 0:
                    # Ingreso = consumo * tarifa de venta COP/kWh  --> 1250 COP  y 1450 COP enel x
                    ingresos_diarios = consumo * station_info[3] + generacion_consumo * station_info[9]
                else:
                    # Ingreso = sonsumo * tarifa de venta COP/kWh estación semirápida --> 1250COP enel x
                    ingresos_diarios = (-1) * generacion_consumo * station_info[4] + PV_data['Promedio kWh/dia'] * station_info[3]

                # Calcular ingresos anuales --> ganancia_tarifa * cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga * 365
                ingresos_anuales = ingresos_diarios * 365

                # Calcular flujo de caja
                flujo_caja = ingresos_anuales - station_info[0] - PV_data['Costo mantenimiento'] / T_C
                if t == 9: flujo_caja -= (station_info[1] * station_info[8] + PV_data['Costo compra'] / T_C * 0.2)  # Upgrade percentage, 20% por actualizacion del inversor solar
            else:
                # Calcular máximo años de crecimiento de la demanda
                maximo_años_crecimiento_demanda = np.round(
                    np.log10(24 / (fast_info[5] * fast_info[6])) / 
                    np.log10(1 + crecimiento_demanda)
                )
                # cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga
                consumo = fast_info[5] * fast_info[6] * fast_info[7]

                # Ajustar ingresos según el crecimiento de la demanda
                if t > maximo_años_crecimiento_demanda and crecimiento_demanda >= 0.25:
                    consumo *= (1 + crecimiento_demanda) ** maximo_años_crecimiento_demanda
                else:
                    consumo *= (1 + crecimiento_demanda) ** t

                generacion_consumo = PV_data['Promedio kWh/dia'] - consumo

                if generacion_consumo > 0:
                    # Ingreso = consumo * tarifa de venta COP/kWh  --> 1250 COP  y 1450 COP enel x
                    ingresos_diarios = consumo * fast_info[3] + generacion_consumo * fast_info[9]
                else:
                    # Ingreso = sonsumo * tarifa de venta COP/kWh estación semirápida --> 1250COP enel x
                    ingresos_diarios = (-1) * generacion_consumo * fast_info[4] + PV_data['Promedio kWh/dia'] * fast_info[3]

                # Calcular ingresos anuales --> ganancia_tarifa * cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga * 365
                ingresos_anuales = ingresos_diarios * 365

                # Calcular flujo de caja
                flujo_caja = ingresos_anuales - fast_info[0] - PV_data['Costo mantenimiento'] / T_C
                if t == 19: flujo_caja -= (fast_info[1] * fast_info[8] + PV_data['Costo compra'] / T_C * 0.2)  # Upgrade percentage, 20% por actualizacion del inversor solar
            
            flujos_caja.append(flujo_caja)
        
        # Calcular NPV e IRR
        NPV = npf.npv(tasa_descuento, flujos_caja)
        npv_por_año.append(NPV)
    
    return npv_por_año, flujos_caja

def escenarios_NPV(tasa_descuento_rango, crecimiento_demanda_rango, 
                   vida_util_rango, station_info, PV_data, fast_info):
    # Crear una lista para almacenar los resultados
    resultados = []

    # Iterar sobre tasas de descuento y crecimiento de demanda
    for tasa_descuento in tasa_descuento_rango:
        for crecimiento_demanda in crecimiento_demanda_rango:
            # Calcular NPV por año y flujos de caja
            NPV_por_año, flujos_caja = calcular_NPV_por_año(
                tasa_descuento,
                crecimiento_demanda,
                tasa_descuento,
                crecimiento_demanda,
                vida_util_rango[-1], 
                station_info, 
                PV_data,
                fast_info
            )
            # Almacenar los resultados en un diccionario
            resultados.append({
                'tasa_descuento': tasa_descuento,
                'costos_mantenimiento': station_info[0],
                'costos_mantenimiento': station_info[0],
                'crecimiento_demanda': crecimiento_demanda,
                'inversion_inicial': station_info[1],
                'tipo_cargador': station_info[2],
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
    plt.title(df_resultados['tipo_cargador'][0] + ' to Fast CS Sensitivity Analysis - NPV vs. Service Life', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid()
    plt.savefig(df_resultados['tipo_cargador'][0] + " to Fast VPN_All_Cases_10_Years.png")
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
    plt.title(df_resultados['tipo_cargador'][0] + ' to Fast CS Cash Flow - Best and Worst NPV_final', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Cash Flow', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12, title_fontsize='13', title='Legend', loc='best', frameon=True)

    # Configurar etiquetas de los ejes
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')

    plt.grid(True)
    plt.savefig(df_resultados['tipo_cargador'][0] + " to Fast Cash_Flow_Best_Worst.png", bbox_inches='tight')
    plt.show()

def PV_inclusion(condicion, PV_data):

    if not condicion:
        # Escalar por el que quieres multiplicar
        escalar = 0  # ejemplo: multiplicar por 1.2

        # Multiplicar cada valor numérico por el escalar
        for key, value in PV_data.items():
            if isinstance(value, (int, float)):  # Verifica si es un número
                PV_data[key] = value * escalar
    
    return PV_data

def rebates_taxCredit(condicion ,inversion_data):
    if condicion:
        # Escalar por el que quieres multiplicar
        level2 = 6500 # The California Electric Vehicle Infrastructure Project (CALeVIP)
        DC_fast = 80000 # The California Electric Vehicle Infrastructure Project (CALeVIP)

        # Multiplicar cada valor numérico por el escalar
        inversion_data -= [level2, level2, DC_fast]

        # reducción del 30% como apoyo federal tax
        inversion_data *= [0.7, 0.7, 1]
    
    return inversion_data

if __name__ == '__main__':
    # Leer el DataFrame de costos de cargadores
    filePath = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Total_costs_CS.csv'
    df_costs = pd.read_csv(filePath, sep=';')
    
    # Leer arcuivo Json con información de generacion solar y costos
    with open("H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\promedios.json") as archivo:
        # Cargar su contenido y crear un diccionario con 'Promedio kWh/dia' y 'Promedio kWh/mes'
        info_PV_gen = json.load(archivo)

    # Incluir o excluir PV system, True para incluir, False para excluir
    info_PV_gen = PV_inclusion(True, info_PV_gen)

    # Define una tasa de cambio
    T_C = 3951.65  # Promedio dólar durante 2024

    # Filtrar costos de estaciones lentas
    df_costs = df_costs[df_costs['Charge_type'] != 'Slow']
    df_diferent_costs = df_costs.loc[~df_costs['Charger'].duplicated(keep='first')]
    df_diferent_costs = df_diferent_costs[df_diferent_costs['Charger'].notnull()]

    # Calcular inversión inicial con costos de instalación y paneles PV
    inversion_inicial_rango = (df_diferent_costs['Charger'].to_numpy() + 
                               df_diferent_costs['Installation'].to_numpy())

    # Incluir o excluir rebates and federal tax credit, True para incluir, False para excluir
    inversion_inicial_rango = rebates_taxCredit(True, inversion_inicial_rango)

    # Asignar nombres a las inversiones iniciales
    inversion_inicial_name = ['Semifast_Basic', 'Semifast', 'Fast']
    inversion_inicial_name = ['Semifast_Basic', 'Semifast', 'Fast']

    # Leer el DataFrame de tarifas de energía de CEDENAR
    filePath = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Tarifas_energia.csv'
    df_tarifas = pd.read_csv(filePath, sep=',')
    
    # Tarifas de energía y carga
    tarifa_energia = 500 / T_C  # Costo promedio año 2024 kWh nivel de tensión 1
    tarifa_carga_semi = 1250 / T_C    # Para carga semirápida Enel X
    tarifa_carga_fast = 1450 / T_C    # Para carga semirápida Enel X
    ganancia_semi = tarifa_carga_semi - tarifa_energia
    ganancia_fast = tarifa_carga_fast - tarifa_energia

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
    
    upgrade_semi = 0.9
    upgrade_fast = 0.2

    # Groups input information by station type
    semi_fast_basic = [costos_mantenimiento_rango[0], 
                         inversion_inicial_rango[0], 
                         inversion_inicial_name[0], 
                         tarifa_carga_semi,
                         ganancia_semi, 
                         cargas_diarias_promedio_semi, 
                         tiempo_carga_promedio_semi, 
                         potencia_promedio_carga_semi, 
                         upgrade_semi,
                         tarifa_energia] 
    semi_fast_complex = [costos_mantenimiento_rango[0], 
                         inversion_inicial_rango[1], 
                         inversion_inicial_name[1], 
                         tarifa_carga_semi,
                         ganancia_semi,  
                         cargas_diarias_promedio_semi, 
                         tiempo_carga_promedio_semi, 
                         potencia_promedio_carga_semi, 
                         upgrade_semi,
                         tarifa_energia]
    fast = [costos_mantenimiento_rango[1], 
                         inversion_inicial_rango[2], 
                         inversion_inicial_name[2], 
                         tarifa_carga_fast,
                         ganancia_fast, 
                         cargas_diarias_promedio_fast, 
                         tiempo_carga_promedio_fast, 
                         potencia_promedio_carga_fast, 
                         upgrade_fast,
                         tarifa_energia]

    # # Calcular NPV para cada configuración
    # df_semifast_Basic = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
    #                                                   crecimiento_demanda_rango, 
    #                                                   vida_util_rango,
    #                                                   semi_fast_basic,
    #                                                   info_PV_gen))
    
    # Calcular NPV para cada configuración
    df_semifast_Complex = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
                                                      crecimiento_demanda_rango, 
                                                      vida_util_rango,
                                                      semi_fast_complex,
                                                      info_PV_gen,
                                                      fast))
    
    # Calcular NPV para cada configuración
    df_fast = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
                                                      crecimiento_demanda_rango, 
                                                      vida_util_rango,
                                                      fast,
                                                      info_PV_gen,
                                                      fast))
    graficar(df_semifast_Complex)
    graficar(df_fast)

    # # Concatenar los dataframes y exportar resultados
    # df_resultados = pd.concat([df_semifast_Basic, df_semifast_Complex, df_fast], ignore_index=True)
    # df_resultados.to_csv('H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\Economic_results.csv', index=False)
