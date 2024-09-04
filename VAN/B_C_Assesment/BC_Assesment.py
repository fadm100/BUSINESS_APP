import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy_financial as npf
import seaborn as sns

# Función para calcular el NPV a lo largo de la vida útil
def calcular_NPV_por_año(tasa_descuento, costos_mantenimiento, crecimiento_demanda, inversion_inicial, vida_util, tarifa):
    npv_por_año = []
    for año in range(vida_util):
        flujos_caja = [-inversion_inicial]
        for t in range(año + 1):
            ingresos_anuales = tarifa * cargas_diarias_promedio * tiempo_carga_promedio * potencia_promedio_carga * 365
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
    plt.suptitle('Histogramas de Variables')
    plt.savefig("VPN_Histogram.png")
    plt.show()

    # # Crear gráfico de dispersión 3D con cambio de colores tasa_descuento, costos_operativos y NPV
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111, projection='3d')
    # npv_min = df_resultados['NPV_final'].min()
    # npv_max = df_resultados['NPV_final'].max()
    # scatter = ax.scatter(df_resultados['tasa_descuento'], df_resultados['costos_mantenimiento'], df_resultados['NPV_final'],
    #                     c=df_resultados['NPV_final'], marker='o', cmap='viridis', vmin=npv_min, vmax=npv_max)

    # ax.set_xlabel('Tasa de Descuento')
    # ax.set_ylabel('Costos Mantenimiento')
    # ax.set_zlabel('NPV Final')
    # ax.set_title('Gráfica de Dispersión 3D: Tasa de Descuento, Costos Mantenimiento y NPV Final')
    # cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    # cbar.set_label('NPV Final')
    # plt.show()

    # # Crear gráfico de dispersión 3D con cambio de colores tasa_descuento, inversion_inicial y NPV
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111, projection='3d')
    # npv_min = df_resultados['NPV_final'].min()
    # npv_max = df_resultados['NPV_final'].max()
    # scatter = ax.scatter(df_resultados['tasa_descuento'], df_resultados['inversion_inicial'], df_resultados['NPV_final'],
    #                     c=df_resultados['NPV_final'], marker='o', cmap='viridis', vmin=npv_min, vmax=npv_max)

    # ax.set_xlabel('Tasa de Descuento')
    # ax.set_ylabel('Inversión Inicial')
    # ax.set_zlabel('NPV Final')
    # ax.set_title('Gráfica de Dispersión 3D: Tasa de Descuento, Inversión Inicial y NPV Final')
    # cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    # cbar.set_label('NPV Final')
    # plt.show()

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
    plt.savefig("VPN_3D.png")
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
    fig, ax = plt.subplots(figsize=(10, 6))

    for index, row in df_resultados.iterrows():
        # ax.plot(row['vida_util'], row['NPV'], label=f"Tasa Desc. {row['tasa_descuento']:.0%}, Costos Oper. {row['costos_operativos']} USD, Crec. Demanda {row['crecimiento_demanda']:.0%}, Inv. Inicial {row['inversion_inicial']} USD")
        ax.plot(row['vida_util'], row['NPV'], label=f"Crec. Demanda {row['crecimiento_demanda']:.0%}, Tasa Desc. {row['tasa_descuento']:.0%}")

    ax.set_xlabel('Vida Útil (años)')
    ax.set_ylabel('Valor Presente Neto (NPV) (USD)')
    ax.set_title('Análisis de Sensibilidad - NPV vs Vida Útil')
    ax.legend()
    ax.grid()
    plt.savefig("VPN_All_Cases_10_Years.png")
    plt.show()

    # Encontrar el mejor y peor NPV_final
    mejor_idx = df_resultados['NPV_final'].idxmax()
    peor_idx = df_resultados['NPV_final'].idxmin()

    # # Graficar
    # plt.figure(figsize=(10, 6))
    # plt.plot(df_resultados['flujos_caja'].iloc[mejor_idx], label=f'Mejor NPV_final: {df_resultados["NPV_final"].iloc[mejor_idx]}', marker='o')
    # plt.plot(df_resultados['flujos_caja'].iloc[peor_idx], label=f'Peor NPV_final: {df_resultados["NPV_final"].iloc[peor_idx]}', marker='o')
    # plt.title('Flujo de Caja - Mejor y Peor NPV_final')
    # plt.xlabel('Periodo')
    # plt.ylabel('Flujo de Caja')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    
    # Graficar
    plt.figure(figsize=(12, 6))

    # Gráfico de barras para el mejor NPV_final
    plt.bar(range(len(df_resultados['flujos_caja'].iloc[mejor_idx])), 
            df_resultados['flujos_caja'].iloc[mejor_idx], 
            label=f'Mejor NPV_final: {df_resultados["NPV_final"].iloc[mejor_idx]}', 
            alpha=0.7)

    # Gráfico de barras para el peor NPV_final
    plt.bar(range(len(df_resultados['flujos_caja'].iloc[peor_idx])), 
            df_resultados['flujos_caja'].iloc[peor_idx], 
            label=f'Peor NPV_final: {df_resultados["NPV_final"].iloc[peor_idx]}', 
            alpha=0.7)

    plt.title('Flujo de Caja - Mejor y Peor NPV_final')
    plt.xlabel('Periodo')
    plt.ylabel('Flujo de Caja')
    plt.legend()
    plt.grid(True)
    plt.savefig("Cash_Flow_Best_Worst.png")
    plt.show()


if __name__ == '__main__':

    # Leer el DataFrame de costos de cargadores
    filePath = 'Total_costs_CS.csv'  # Costos de un solo cargador, la tabla contiene varios tipos de cargadores divididos entre lentos, semirápidos y rapídos
    df_costs = pd.read_csv(filePath, sep=';')

    # Se filtran los costos de las estaciones lentas porque no son útiles para estaciones de carga públicas o electrolineras
    df_costs = df_costs[df_costs['Charge_type'] != 'Slow']

    # Se toman los valores no repetidos porque los duplicados corresponden al mismo tipo de cargador en un contexto diferente (público, privado, etc.)
    df_diferent_costs = df_costs.loc[~df_costs['Charger'].duplicated(keep = 'first')]
    df_diferent_costs = df_diferent_costs[df_diferent_costs['Charger'].notnull()]

    # Toma los diferentes costos de cargadores semirápidos y rápidos, los dos primeros datos son semirápidos. Con esto se generan casos de inversión inicial. Se suma con el costo de instalación de ese cargador específico (no inlcuye obra civil)
    inversion_inicial_rango = df_diferent_costs['Charger'].to_numpy() + df_diferent_costs['Installation'].to_numpy() # USD
    # Se da el nombre Semifast_Basic al primer dato de inversión inicial, Semifast_Complex al segundo dato y Fast al tercer dato
    inversion_inicial_name = ['Semifast_Basic', 'Semifast_Complex', 'Fast']

    # Leer el DataFrame de tarifas de energía de CEDENAR
    filePath = 'Tarifas_energia.csv' 
    df_tarifas = pd.read_csv(filePath, sep=',')

    # Define una tasa de cambio
    T_C = 3951.65 # promedio dolar durante 2024 --> https://www.dolar-colombia.com/ano/2024 --> consultado el 28/08/2024

    tarifa_energia = df_tarifas['Costo_COP/kWh_Nivel_Tension_1'].iloc[-1] / T_C # Costo promedio año 2024 kWh nivel de tensión 1
    porcentaje_ganancia = 0.5
    tarifa_carga = tarifa_energia * (1 + porcentaje_ganancia)
    ganancia_tarifa = tarifa_carga - tarifa_energia
    print('Tarifa de energía = ', tarifa_energia * T_C, '; Tarifa de venta', tarifa_carga * T_C, '; Ganancia venta', ganancia_tarifa * T_C)
    
    # Define el porcentaje de inflación promedio anual en Colombia --> https://datosmacro.expansion.com/ipc-paises/colombia
    inflacion = 0.041

    # Un VE puede cargarse durante 2.5 y 5 horas en una estación semirápida según "Prediction of electric vehicle charging duration time using ensemble machine learning algorithm and Shapley additive explanations"
    cargas_diarias_promedio = 0.28 # --> se sume una promedio de 2 cargas por semana el primer año
    tiempo_carga_promedio = 2.5
    potencia_promedio_carga = 10 # --> Tesla S --> Business Case for EV Charging on the Motorway Network in Denmark

    # Rango de variaciones para el análisis de sensibilidad
    tasa_descuento_rango = np.arange(0.05, 0.2, 0.05)  # del 5% al 20% --> 9% Colombia 2022 --> https://2022.dnp.gov.co/DNP-Redes/Revista-Juridica/Paginas/Adopci%C3%B3n-de-la-Tasa-Social-de-Descuento-para-la-evaluaci%C3%B3n-de-proyectos-de-inversi%C3%B3n.aspx

    costos_mantenimiento_rango = [400, 800]  
    ''' costos anuales de 400 USD para lenta y semirápida 800 USD para DC rápidas --> https://afdc.energy.gov/fuels/electricity-infrastructure-maintenance-and-operation
    este costo no incluye costos operacionales por uso o alquiler de software de gestión --> https://driivz.com/blog/operation-maintenance-ev-charging-infrastructure/#:~:text=Charging%20station%20operators%20should%20anticipate,chargers%20costing%20double%20that%20amount.&text=EV%20charging%20stations%20are%20not%20just%20glorified%20electrical%20sockets.'''

    # Tomado del trabajo de Nohora. Valores para incremento de taxis VE los porcentajes de incremento son muy variables
    crecimiento_demanda_rango = [0.05, 0.15, 0.25] 

    vida_util_rango = np.arange(1, 11, 1)  # Vida útil de 1 a 10 años

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
    df_resultados.to_csv('Economic_results.csv', index=False)

