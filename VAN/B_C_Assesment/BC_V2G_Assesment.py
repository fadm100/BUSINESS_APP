import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf
import json

def Flujos_Descontados(arr, inicial):
    diferencias = [arr[i] - arr[i - 1] for i in range(1, len(arr))]
    return [-inicial] + diferencias  

# Función para calcular el NPV a lo largo de la vida útil
def calcular_NPV_por_año(tasa_descuento, crecimiento_demanda, vida_util, station_info, PV_data, income):
    npv_por_año = []
    
    for año in range(vida_util):
        flujos_caja = [-station_info[1] - PV_data['Costo compra'] / T_C - PV_data['Costo instalación'] / T_C]
        
        for t in range(año + 1):
            # USD_kW = 3
            ingresos_diarios = income / 30 #680.74 * USD_kW / 30 # se toma de DOPER ejemplo: 1000 USD --> por venta de energía
            gastos_diarios = 0.0 # se toma de DOPER ejemplo:2000 USD --> por compra de energía
            if t >= 10: 
                gastos_diarios *= (1 + crecimiento_demanda) # se incrementan los gastos por la entrada de buses nuevos a la flota
                ingresos_diarios *= (1 + crecimiento_demanda) # se incrementan los ingresos por la entrada de buses nuevos a la flota
            
            # Calcular ingresos anuales --> ganancia_tarifa * cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga * 365
            ingresos_anuales = (ingresos_diarios - gastos_diarios) * 365

            # Calcular flujo de caja
            flujo_caja = ingresos_anuales - station_info[0] - PV_data['Costo mantenimiento'] / T_C
            if t == 9: flujo_caja -= (station_info[1] * station_info[3] + PV_data['Costo compra'] / T_C * 0.2)  # Upgrade percentage, 20% por actualizacion del inversor solar
            
            flujos_caja.append(flujo_caja)
        
        # Calcular NPV e IRR
        NPV = npf.npv(tasa_descuento, flujos_caja)
        npv_por_año.append(NPV)
    flujos_descon = Flujos_Descontados(npv_por_año, station_info[1])    
    return npv_por_año, flujos_descon

def escenarios_NPV(tasa_descuento_rango, crecimiento_demanda, 
                   vida_util_rango, station_info, PV_data, incomes, income_name):
    # Crear una lista para almacenar los resultados
    resultados = []
    
    # Iterar sobre tasas de descuento y crecimiento de demanda
    for tasa_descuento in tasa_descuento_rango:
        i = 0
        for income in incomes:
            # Calcular NPV por año y flujos de caja
            NPV_por_año, flujos_caja = calcular_NPV_por_año(
                tasa_descuento,
                crecimiento_demanda,
                vida_util_rango[-1], 
                station_info, 
                PV_data,
                income
            )
            # Almacenar los resultados en un diccionario
            resultados.append({
                'tasa_descuento': tasa_descuento,
                'income': income_name[i],
                'inversion_inicial': station_info[1],
                'vida_util': vida_util_rango,
                'flujos_caja': flujos_caja,
                'NPV': NPV_por_año,
                'NPV_final': NPV_por_año[-1]
            })
            i += 1

    return resultados


def graficar1(df_resultados):
    # Análisis de sensibilidad - Graficar NPV por vida útil
    plt.figure(figsize=(8, 4.2))

    row = df_resultados.iloc[0]
    plt.plot(row['vida_util'], row['NPV'], label='NPV')

    # Configurar etiquetas y título
    # plt.xlabel('Service life (years)', fontsize=14, fontweight='bold')
    # plt.ylabel('Net Present Value (NPV) (USD)', fontsize=14, fontweight='bold')
    # plt.title(' CS sensitivity analysis - NPV vs. service life', fontsize=16, fontweight='bold')
    plt.title('NPV en función de la vida útil', fontsize=16, fontweight='bold')
    plt.xlabel('Vida útil (años)', fontsize=14, fontweight='bold')
    plt.ylabel('NPV', fontsize=14, fontweight='bold')
    plt.grid()
    # plt.savefig(" VPN_All_Cases_10_Years.png")
    plt.show()

    # Graficar comparación de flujos de caja - Mejor y Peor NPV_final
    plt.figure(figsize=(10, 4.5))
    idx = 0
    plt.bar(range(len(df_resultados['flujos_caja'].iloc[idx])),
            df_resultados['flujos_caja'].iloc[idx],
            label=f'NPV: {df_resultados["NPV_final"].iloc[idx]:.2f}',
            color='blue', alpha=0.7)

    # Configurar título y etiquetas
    # plt.title(' CS cash flow - Best and worst NPV', fontsize=16, fontweight='bold')
    # plt.xlabel('Year', fontsize=14, fontweight='bold')
    # plt.ylabel('Cash Flow', fontsize=14, fontweight='bold')
    plt.title('Flujo de Caja', fontsize=16, fontweight='bold')
    plt.xlabel('Año', fontsize=14, fontweight='bold')
    plt.ylabel('Valor del flujo', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12, title_fontsize='13', loc='best', frameon=True)

    # Configurar etiquetas de los ejes
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')

    plt.grid(True)
    # plt.savefig(" Cash_Flow_Best_Worst.png", bbox_inches='tight')
    plt.show()

def graficar(df_resultados):

    # Análisis de sensibilidad - Graficar NPV por vida útil
    plt.figure(figsize=(12, 7))

    for _, row in df_resultados.iterrows():
        x = row['vida_util']
        y = row['NPV']
        label = f"Inc: {row['income']}, r: {row['tasa_descuento']:.0%}"
        plt.plot(x, y, label=label)
        
        # Agregar texto al final de cada línea
        plt.text(x[-1] + 0.3, y[-1], label, fontsize=9, verticalalignment='center')

    # Etiquetas y estilo
    plt.xlabel('Service life (years)', fontsize=14, fontweight='bold')
    plt.ylabel('Net Present Value (NPV) (USD)', fontsize=14, fontweight='bold')
    plt.title('CS sensitivity analysis - NPV vs. service life', fontsize=16, fontweight='bold')
    plt.grid()
    plt.tight_layout()
    plt.savefig("VPN_All_Cases_10_Years_Annotated.png")
    plt.show()

    # --- Segunda gráfica: flujos de caja ---
    mejor_idx = df_resultados['NPV_final'].idxmax()
    peor_idx = df_resultados['NPV_final'].idxmin()

    plt.figure(figsize=(12, 6))

    for idx, color, label in zip([mejor_idx, peor_idx], ['green', 'red'], ['Best NPV', 'Worst NPV']):
        plt.bar(range(len(df_resultados['flujos_caja'].iloc[idx])),
                df_resultados['flujos_caja'].iloc[idx],
                label=f'{label}: {df_resultados["NPV_final"].iloc[idx]:.2f}',
                alpha=0.7, width=0.4, align='center' if idx == mejor_idx else 'edge', color=color)

    plt.title('CS cash flow - Best and worst NPV', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Cash Flow', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12, title_fontsize='13', loc='best', frameon=True)
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.grid(True)
    plt.savefig("Cash_Flow_Best_Worst.png", bbox_inches='tight')
    plt.show()


def PV_inclusion(condicion, PV_data):

    escalar = 10 # ejemplo: multiplicar por 2
    if not condicion:
        # Escalar por el que quieres multiplicar
        escalar = 0  # elimina PV system

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
        inversion_data *= [0.2, 0.2, 0.2] # España subsidia hasta el 80% de los costos iniciales https://www.idae.es/ayudas-y-financiacion/para-movilidad-y-vehiculos/programa-moves-iii
    
    return inversion_data

if __name__ == '__main__':
    # Leer el DataFrame de costos de cargadores
    filePath = 'H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Total_costs_CS.csv' # Modificar los costos de las estaciones Fast
    df_costs = pd.read_csv(filePath, sep=';')
    
    # Leer arcuivo Json con información de generacion solar y costos
    with open("H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\promedios.json") as archivo:
        # Cargar su contenido y crear un diccionario con 'Promedio kWh/dia' y 'Promedio kWh/mes'
        info_PV_gen = json.load(archivo)

    # Incluir o excluir PV system, True para incluir, False para excluir
    info_PV_gen = PV_inclusion(False, info_PV_gen)

    # Define una tasa de cambio
    T_C = 3951.65  # Promedio dólar durante 2024
    # T_C = 5000  # tasa de cambio para ser congruente con el trabajo de Nohora

    incomes = [680.74 * 3, 680.74 * 4, 680.74 * 5, 810.0 * 3, 810.0 * 4, 810.0 * 5]

    # Filtrar costos de estaciones lentas
    df_costs = df_costs[df_costs['Charge_type'] != 'Slow']
    df_diferent_costs = df_costs.loc[~df_costs['Charger'].duplicated(keep='first')]
    df_diferent_costs = df_diferent_costs[df_diferent_costs['Charger'].notnull()]

    # Calcular inversión inicial con costos de instalación y paneles PV
    inversion_inicial_rango = (df_diferent_costs['Charger'].to_numpy() + 
                               df_diferent_costs['Installation'].to_numpy())

    # Incluir o excluir rebates and federal tax credit, True para incluir, False para excluir
    inversion_inicial_rango = rebates_taxCredit(False, inversion_inicial_rango)

    # Asignar nombres a las inversiones iniciales
    income_name = ['680kW_3USD/kW', '680kW_4USD/kW', '680kW_5USD/kW', '810kW_3USD/kW', '810kW_4USD/kW', '810kW_5USD/kW']

    # Rango de variaciones para el análisis de sensibilidad
    tasa_descuento_rango = [0.05, 0.1, 0.15]  # del 5% al 20% # alrededor del 10% para Colombia
    costos_mantenimiento_rango = [400, 800]  # Sin PV
    crecimiento_demanda = 0.00 # Asumimos una flota ya establecida con un numero fijo de buses o un bajo incremento cada varios años
    vida_util_short = np.arange(1, 16, 1)  # Vida útil de 1 a 20 años
    vida_util_large = np.arange(1, 21, 1)  # Vida útil de 1 a 20 años
    
    # Upgrade percentage
    
    upgrade_semi = 0.5
    upgrade_fast = 0.8

    # Groups input information by station type
    semi_fast_basic = [costos_mantenimiento_rango[0], 
                         inversion_inicial_rango[0], 
                         income_name[0], 
                         upgrade_semi] 
    semi_fast_complex = [costos_mantenimiento_rango[0], 
                         inversion_inicial_rango[1], 
                         income_name[1], 
                         upgrade_semi]
    fast = [costos_mantenimiento_rango[1], 
                         20000 * 7, #inversion_inicial_rango[2]/15*7, 
                         income_name[1],
                         upgrade_fast]
    
    # Calcular NPV para cada configuración
    # df_semifast_Complex = pd.DataFrame(escenarios_NPV(tasa_descuento, 
    #                                                   crecimiento_demanda, 
    #                                                   vida_util_short,
    #                                                   semi_fast_complex,
    #                                                   info_PV_gen))
    # print(df_semifast_Complex['NPV_final'].to_string(index=False))
    # Calcular NPV para cada configuración
    df_fast = pd.DataFrame(escenarios_NPV(tasa_descuento_rango, 
                                                      crecimiento_demanda, 
                                                      vida_util_large,
                                                      fast,
                                                      info_PV_gen,
                                                      incomes,
                                                      income_name))
    print(df_fast['NPV_final'].to_string(index=False))
    # graficar(df_semifast_Complex)
    graficar(df_fast)

    # # Concatenar los dataframes y exportar resultados
    # df_resultados = pd.concat([df_semifast_Basic, df_semifast_Complex, df_fast], ignore_index=True)
    # df_semifast_Complex.to_csv('H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\L2_L3_PV40k_TF_SB.csv', index=False)
    df_fast.to_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\25-04-2025\\All.csv', index=False)
    