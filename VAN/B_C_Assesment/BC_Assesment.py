import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf

# Función para calcular el NPV a lo largo de la vida útil
def calcular_NPV_por_año(tasa_descuento, costos_mantenimiento, crecimiento_demanda, inversion_inicial, vida_util, tarifa):
    npv_por_año = []
    for año in range(vida_util):
        flujos_caja = [-inversion_inicial]
        for t in range(año + 1):
            ingresos_anuales = tarifa * cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga * 365
            if t> maximo_años_crecimiento_demanda and crecimiento_demanda >= 0.25:
                ingresos_anuales *= (1 + crecimiento_demanda) ** maximo_años_crecimiento_demanda
            else:
                ingresos_anuales *= (1 + crecimiento_demanda) ** t
            ingresos_anuales *= (1 + inflacion) ** t
            gastos = costos_mantenimiento * (1 + inflacion) ** t
            flujo_caja = ingresos_anuales - gastos
            flujos_caja.append(flujo_caja)
        
        IRR = npf.irr(flujos_caja)
        NPV = npf.npv(tasa_descuento, flujos_caja)
        npv_por_año.append(NPV)
    return npv_por_año, flujos_caja

def escenarios_NPV(tasa_descuento_rango, costos_mantenimiento, crecimiento_demanda_rango, inversion_inicial, inversion_name, vida_util_rango, tarifa):
        # Crear un DataFrame para almacenar los resultados
    resultados = []

    for tasa_descuento in tasa_descuento_rango:
        for crecimiento_demanda in crecimiento_demanda_rango:
            NPV_por_año, flujos_caja = calcular_NPV_por_año(tasa_descuento, costos_mantenimiento, crecimiento_demanda, inversion_inicial, vida_util_rango[-1], tarifa)
            resultados.append({
                'tasa_descuento': tasa_descuento,
                'costos_mantenimiento': costos_mantenimiento,
                'crecimiento_demanda': crecimiento_demanda,
                'inversion_inicial': inversion_inicial,
                'tipo_cargador': inversion_name,
                'vida_util': vida_util_rango,
                'flujos_caja': flujos_caja,
                'NPV': NPV_por_año,
                'NPV_final': NPV_por_año[-1]
            })
    return resultados

def graficar(df_resultados):
    # Listado de columnas a graficar
    columnas = ['NPV_final']
    # Crear histogramas para cada columna
    df_resultados[columnas].hist(bins=15, figsize=(15, 10), layout=(1, 1), edgecolor='black')
    plt.suptitle('Histogramas de Variables', fontsize=20, fontweight='bold')
    # Configurar las etiquetas de los ejes en negrita
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.savefig("VPN_Histogram.png")
    plt.show()

    # Crear gráfico de dispersión 3D con colores basado en tasa_descuento, crecimiento_demanda y NPV
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Definir los límites de color
    npv_min = df_resultados['NPV_final'].min()
    npv_max = df_resultados['NPV_final'].max()

    # Crear el gráfico de dispersión con puntos más grandes, transparencia y bordes
    scatter = ax.scatter(df_resultados['tasa_descuento'], df_resultados['crecimiento_demanda'], df_resultados['NPV_final'],
                        c=df_resultados['NPV_final'], marker='o', cmap='viridis', vmin=npv_min, vmax=npv_max,
                        s=80,  # Tamaño de los puntos
                        alpha=0.8,  # Transparencia
                        edgecolors='k')  # Borde negro para cada punto

    # Etiquetas de los ejes con títulos más grandes y en negrita
    ax.set_xlabel('Tasa de Descuento', fontsize=16, fontweight='bold')
    ax.set_ylabel('Crecimiento Demanda', fontsize=16, fontweight='bold')
    ax.set_zlabel('NPV Final', fontsize=16, fontweight='bold')

    # Título del gráfico
    ax.set_title('Relación entre Tasa de Descuento, Crecimiento de Demanda y NPV Final', fontsize=18, fontweight='bold')

    # Configuración de la barra de color
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, aspect=8)  # Ajuste del tamaño de la barra de color
    cbar.set_label('NPV Final', fontsize=14, fontweight='bold')

    # Guardar el gráfico
    plt.savefig("VPN_3D_mejorado_puntos_intensos.png", bbox_inches='tight')

    # Mostrar el gráfico
    plt.show()

    # Análisis de sensibilidad - Graficar NPV por vida útil
    fig, ax = plt.subplots(figsize=(10, 6))

    for index, row in df_resultados.iterrows():
        # ax.plot(row['vida_util'], row['NPV'], label=f"Tasa Desc. {row['tasa_descuento']:.0%}, Costos Oper. {row['costos_operativos']} USD, Crec. Demanda {row['crecimiento_demanda']:.0%}, Inv. Inicial {row['inversion_inicial']} USD")
        ax.plot(row['vida_util'], row['NPV'], label=f"Demand inc. {row['crecimiento_demanda']:.0%}, IRR {row['tasa_descuento']:.0%}")

    ax.set_xlabel('Service life (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Net Present Value (NPV) (USD)', fontsize=14, fontweight='bold')
    ax.set_title('Fast CS Sensitivity Analysis - NPV vs. service Life', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid()
    plt.savefig("VPN_All_Cases_10_Years.png")
    plt.show()

    # Encontrar el mejor y peor NPV_final
    mejor_idx = df_resultados['NPV_final'].idxmax()
    peor_idx = df_resultados['NPV_final'].idxmin()
    
    # Graficar comparación de flujos de caja - Mejor y Peor NPV_final
    plt.figure(figsize=(12, 6))

    # Gráfico de barras para el mejor NPV_final
    plt.bar(range(len(df_resultados['flujos_caja'].iloc[mejor_idx])), 
            df_resultados['flujos_caja'].iloc[mejor_idx], 
            label=f'Best NPV_final: {df_resultados["NPV_final"].iloc[mejor_idx]:.2f}', 
            alpha=0.7, width=0.4, align='center', color='green')

    # Gráfico de barras para el peor NPV_final
    plt.bar(range(len(df_resultados['flujos_caja'].iloc[peor_idx])), 
            df_resultados['flujos_caja'].iloc[peor_idx], 
            label=f'Worst NPV_final: {df_resultados["NPV_final"].iloc[peor_idx]:.2f}', 
            alpha=0.7, width=0.4, align='edge', color='red')

    # Título y etiquetas de los ejes
    plt.title('Fast CS Cash Flow - Best and Worst NPV_final', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Cash Flow', fontsize=14, fontweight='bold')

    # Leyenda
    plt.legend(fontsize=12, title_fontsize='13', title='Legend', loc='best', frameon=True)

    # Configurar las etiquetas de los ejes en negrita
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')

    # Mostrar cuadrícula
    plt.grid(True)

    # Guardar gráfico
    plt.savefig("Cash_Flow_Best_Worst.png", bbox_inches='tight')

    # Mostrar gráfico
    plt.show()



if __name__ == '__main__':

    # Leer el DataFrame de costos de cargadores
    filePath = 'H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Total_costs_CS.csv'  # Costos de un solo cargador, la tabla contiene varios tipos de cargadores divididos entre lentos, semirápidos y rapídos
    # filePath = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Total_costs_CS.csv'  # Costos de un solo cargador, la tabla contiene varios tipos de cargadores divididos entre lentos, semirápidos y rapídos
    df_costs = pd.read_csv(filePath, sep=';')
    
    # Define una tasa de cambio
    T_C = 3951.65 # promedio dolar durante 2024 --> https://www.dolar-colombia.com/ano/2024 --> consultado el 28/08/2024
    
    # Adición de costos del sistema PV de 2.7kW; 3.5HPS; 9.45kWh/día
    # PV_costs = 3060000 / T_C # --> https://articulo.mercadolibre.com.co/MCO-1474396115-panel-solar-300w-6000lm-ecosun-_JM#polycard_client=search-nordic&position=25&search_layout=grid&type=item&tracking_id=2cc4c4ba-44f7-4324-93b7-6aecd2a125ae
    PV_costs = 0
    # PV_install_Cost = 13500000 / T_C # --> https://autosolar.co/paneles-solares/paneles-solares-colombia ; https://greentech.net.co/costo-de-instalacion-de-paneles-solares/
    PV_install_Cost = 0

    # Se filtran los costos de las estaciones lentas porque no son útiles para estaciones de carga públicas o electrolineras
    df_costs = df_costs[df_costs['Charge_type'] != 'Slow']

    # Se toman los valores no repetidos porque los duplicados corresponden al mismo tipo de cargador en un contexto diferente (público, privado, etc.)
    df_diferent_costs = df_costs.loc[~df_costs['Charger'].duplicated(keep = 'first')]
    df_diferent_costs = df_diferent_costs[df_diferent_costs['Charger'].notnull()]

    # Toma los diferentes costos de cargadores semirápidos y rápidos, los dos primeros datos son semirápidos. Con esto se generan casos de inversión inicial. Se suma con el costo de instalación de ese cargador específico (no inlcuye obra civil)
    # inversion_inicial_rango = df_diferent_costs['Charger'].to_numpy() + df_diferent_costs['Installation'].to_numpy() # USD Sin paneles PV
    inversion_inicial_rango = df_diferent_costs['Charger'].to_numpy() + df_diferent_costs['Installation'].to_numpy() + PV_costs + PV_install_Cost # USD con paneles PV
    print(df_diferent_costs['Charger'].to_numpy(), '+', df_diferent_costs['Installation'].to_numpy())
    # Se da el nombre Semifast_Basic al primer dato de inversión inicial, Semifast_Complex al segundo dato y Fast al tercer dato
    inversion_inicial_name = ['Semifast_Basic', 'Semifast_Complex', 'Fast']

    # Leer el DataFrame de tarifas de energía de CEDENAR
    filePath = 'H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Tarifas_energia.csv' 
    # filePath = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Tarifas_energia.csv' 
    df_tarifas = pd.read_csv(filePath, sep=',')

    # tarifa_energia = df_tarifas['Costo_COP/kWh_Nivel_Tension_1'].iloc[-1] / T_C # Costo promedio año 2024 kWh nivel de tensión 1
    tarifa_energia = 500 / T_C # Costo promedio año 2024 kWh nivel de tensión 1
    # porcentaje_ganancia = 3
    '''Esta variable se puede modificar, se tiene control sobre ella (analisis de sensibilidad o mejor optimización)
    Se asume un porcentaje de ganancia del 50% para estaciones semirápidas y de 300% para estaciones DC rápidas'''
    # tarifa_carga = tarifa_energia * (1 + porcentaje_ganancia)
    tarifa_carga = 1250 / T_C # Para carga semirápida Enel X (https://www.elespectador.com/autos/cuanto-cuesta-cargar-un-carro-electrico-en-colombia/)
    # tarifa_carga = 1450 / T_C # Para carga rápida Enel X (https://www.elespectador.com/autos/cuanto-cuesta-cargar-un-carro-electrico-en-colombia/)
    ganancia_tarifa = tarifa_carga - tarifa_energia
    print('Tarifa de energía = ', tarifa_energia * T_C, '; Tarifa de venta', tarifa_carga * T_C, '; Ganancia venta', ganancia_tarifa * T_C)
    
    # Define el porcentaje de inflación promedio anual en Colombia --> https://datosmacro.expansion.com/ipc-paises/colombia --> 4.1%
    inflacion = 0 # En algunos casos la inflación esta implicita en la tasa de retorno, pero no siempre 

    # Un VE puede cargarse durante 2.5 y 5 horas en una estación semirápida según "Prediction of electric vehicle charging duration time using ensemble machine learning algorithm and Shapley additive explanations"
    cargas_diarias_promedio = 0.28
    '''Se asume una promedio de 2 cargas por semana el primer año para estaciones semirápidas y 1 carga por semana para estaciones DC rápidas'''
    tiempo_carga_promedio = 2
    '''promedio Short Duration connection, tabla 2 doc --> "A data driven typology of electric vehicle user types and charging sessions" para estaciones tipo 2 se asume 2 horas
    para estaciones rápidas se asume 30 min de tiempo de carga'''
    numero_cargas_maximas_dia = 24 / tiempo_carga_promedio # El número de cargas máximas que se puede hacer en un día. Ej. Con 2 horas por carga un cargador puede usarse para 12 cargas máximo en un día
    potencia_promedio_carga = 5
    '''Una estación tipo 2 de una fase puede entregar hasta 7.4kW --> Mennekes - IEC 62196. 5kWh promedio de Density transaction volume [kWh] para Short Duration, figure E23 doc --> "A data driven typology of electric vehicle user types and charging sessions"
    10kWh Tesla S --> Business Case for EV Charging on the Motorway Network in Denmark.
    una estación de carga CCS combo 2 puede entregar 50kW o 150kW para este caso se considera un VE Renault Megane E-Tech EV40 130hp que 
     carga con 42kW en promedio con una estación de 50kW.'''

    # Rango de variaciones para el análisis de sensibilidad
    tasa_descuento_rango = np.arange(0.05, 0.16, 0.05)  # del 5% al 20% --> 9% Colombia 2022 --> https://2022.dnp.gov.co/DNP-Redes/Revista-Juridica/Paginas/Adopci%C3%B3n-de-la-Tasa-Social-de-Descuento-para-la-evaluaci%C3%B3n-de-proyectos-de-inversi%C3%B3n.aspx

    costos_mantenimiento_rango = [400, 800]  # Sin PV
    # costos_mantenimiento_rango = [560, 960]  # Con PV
    ''' costos anuales de 400 USD para lenta y semirápida. 800 USD para DC rápidas --> https://afdc.energy.gov/fuels/electricity-infrastructure-maintenance-and-operation
    este costo no incluye costos operacionales por uso o alquiler de software de gestión --> https://driivz.com/blog/operation-maintenance-ev-charging-infrastructure/#:~:text=Charging%20station%20operators%20should%20anticipate,chargers%20costing%20double%20that%20amount.&text=EV%20charging%20stations%20are%20not%20just%20glorified%20electrical%20sockets.'''

    # Tomado del trabajo de Nohora. Valores para incremento de taxis VE los porcentajes de incremento son muy variables
    crecimiento_demanda_rango = [0.05, 0.15, 0.25] 

    maximo_años_crecimiento_demanda = np.round(np.log10(24/(cargas_diarias_promedio*tiempo_carga_promedio))/np.log10(1+crecimiento_demanda_rango[2]))
    print(maximo_años_crecimiento_demanda)

    vida_util_rango = np.arange(1, 21, 1)  # Vida útil de 1 a 10 años

    # Calcula NPV para cada tasa de descuento y cada crecimiento de demanda para costo de mantenimiento semirápido e inversión inicial semirápido communication Basic
    resultados = escenarios_NPV(tasa_descuento_rango, costos_mantenimiento_rango[0], crecimiento_demanda_rango, inversion_inicial_rango[0], inversion_inicial_name[0], vida_util_rango, ganancia_tarifa)
    df_semifast_Basic = pd.DataFrame(resultados)
    # graficar(df_semifast_Basic)

    # Calcula NPV para cada tasa de descuento y cada crecimiento de demanda para costo de mantenimiento semirápido e inversión inicial semirápido communication Complex
    resultados = escenarios_NPV(tasa_descuento_rango, costos_mantenimiento_rango[0], crecimiento_demanda_rango, inversion_inicial_rango[1], inversion_inicial_name[1], vida_util_rango, ganancia_tarifa)
    df_semifast_Complex = pd.DataFrame(resultados)
    graficar(df_semifast_Complex)

    # Calcula NPV para cada tasa de descuento y cada crecimiento de demanda para costo de mantenimiento e inversión inicial estación rápida
    resultados = escenarios_NPV(tasa_descuento_rango, costos_mantenimiento_rango[1], crecimiento_demanda_rango, inversion_inicial_rango[2], inversion_inicial_name[2], vida_util_rango, ganancia_tarifa)
    df_fast = pd.DataFrame(resultados)
    # graficar(df_fast)

    # Concatena los 3 dataframes ingresados [df_semifast_Basic, df_semifast_Complex, df_fast]
    df_resultados = pd.concat([df_semifast_Basic, df_semifast_Complex, df_fast], ignore_index=True)
    # Exportar el DataFrame a CSV
    df_resultados.to_csv('H:\\Mi unidad\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\Economic_results.csv', index=False)
    # df_resultados.to_csv('H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\Economic_results.csv', index=False)

