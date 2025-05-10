import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os

def bar_subplots(df1, df2):
    # Define una tasa de cambio
    T_C = 3951.65  # Promedio dólar durante 2024

    # Función para calcular las métricas
    def calculate_metrics(df):
        grouped = df.groupby('vehicle_id')
        totalEnergyConsumed = (grouped['vehicle_totalEnergyConsumed'].last() - grouped['vehicle_totalEnergyRegenerated'].last()) / 1000
        totalCapacity = 80000
        batterySoC = grouped['vehicle_actualBatteryCapacity'].last() / totalCapacity * 100
        chargingTime = df.groupby('vehicle_id')['vehicle_chargingStationId'].apply(lambda x: x.notnull().sum()) / 60
        energyCharged = df.groupby('vehicle_id')['vehicle_energyCharged'].sum() / 1000
        totalEnergyCost = energyCharged * 1450 / T_C  # Dividir entre T_C para mostrar en USD
        initialCharge = pd.Series(25, index=grouped.groups.keys())  # Carga inicial de 25 para cada vehículo
        vehicleSpeed = df.groupby('vehicle_id')['vehicle_speed'].sum() / 1000
        chargingRate = energyCharged / chargingTime
        print(chargingRate)
        
        # metrics = {
        #     'Initial Charge [kWh]': initialCharge,
        #     'Charged energy [kWh]': energyCharged,
        #     'Total energy consumed [kWh]': totalEnergyConsumed,
        #     'Battery SoC [%]': batterySoC,
        #     'Total charging time [min]': chargingTime,
        #     'Cost per charge [USD]': totalEnergyCost,
        #     'Total distance covered [km]': vehicleSpeed
        # }
        metrics = {
            'Carga inicial [kWh]': initialCharge,
            'Energía cargada [kWh]': energyCharged,
            'Energía total consumida [kWh]': totalEnergyConsumed,
            'SoC [%]': batterySoC,
            'Tiempo total de carga [min]': chargingTime,
            'Costo por carga [USD]': totalEnergyCost,
            'Distancia total cubierta [km]': vehicleSpeed
        }
        return metrics, totalEnergyConsumed.index

    # Calcular métricas para ambos DataFrames
    metrics1, index1 = calculate_metrics(df1)
    metrics2, index2 = calculate_metrics(df2)

    # Crear una figura combinada con dos subgráficas (2x1)
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Asignar colores a las métricas
    patterns = ['/', '\\', '|', '-', '+', 'x']  # Patrones para las barras
    colors = sns.color_palette("magma", len(metrics1))

    # Graficar las métricas para el primer DataFrame (df1)
    positions = list(range(len(index1)))
    width = 0.12  # Ancho de las barras
    for i, (label, data) in enumerate(metrics1.items()):
        axes[0].bar(
            [p + i * width for p in positions],
            data.values,
            width=width,
            label=label,
            color=colors[i]#,
            # hatch=patterns[i % len(patterns)]  # Patrón cíclico
        )
    
    # Configurar ejes y leyendas para el primer subplot
    axes[0].set_xticks([p + width * (len(metrics1) / 2 - 0.5) for p in positions])
    axes[0].set_xticklabels('', rotation=45, fontsize=12, fontweight='bold')
    axes[0].set_xlabel('a)', fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=12)
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Asignar colores a las métricas para el segundo DataFrame
    colors = sns.color_palette("magma", len(metrics2))

    # Graficar las métricas para el segundo DataFrame (df2)
    positions = list(range(len(index2)))
    for i, (label, data) in enumerate(metrics2.items()):
        axes[1].bar(
            [p + i * width for p in positions],
            data.values,
            width=width,
            label=label,
            color=colors[i]#,
            # hatch=patterns[i % len(patterns)]  # Patrón cíclico
        )
    
    # Configurar ejes y leyendas para el segundo subplot
    axes[1].set_xticks([p + width * (len(metrics2) / 2 - 0.5) for p in positions])
    axes[1].set_xticklabels(index2, fontsize=12)
    axes[1].set_xlabel('b)', fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=12)
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar la disposición de las subgráficas
    plt.tight_layout()
    plt.show()


def bar_plots(df):
    # Define una tasa de cambio
    T_C = 3951.65  # Promedio dólar durante 2024

    # Agrupar por vehicle_id y realizar análisis
    grouped = df.groupby('vehicle_id')
    totalEnergyConsumed = (grouped['vehicle_totalEnergyConsumed'].last() - grouped['vehicle_totalEnergyRegenerated'].last()) / 1000
    totalCapacity = 80000
    batterySoC = grouped['vehicle_actualBatteryCapacity'].last() / totalCapacity * 100
    chargingTime = df.groupby('vehicle_id')['vehicle_chargingStationId'].apply(lambda x: x.notnull().sum()) / 60
    energyCharged = df.groupby('vehicle_id')['vehicle_energyCharged'].sum() / 1000
    totalEnergyCost = energyCharged * 1450 / T_C  # Dividir entre T_C para mostrar en USD 
    initialCharge = pd.Series(25, index=grouped.groups.keys())  # Carga inicial de 25 para cada vehículo
    vehicleSpeed = df.groupby('vehicle_id')['vehicle_speed'].sum() / 1000
    chargingRate = energyCharged / chargingTime
    print(chargingRate)

    # Preparar datos para graficar
    metrics = {
        'Initial Charge [kWh]': initialCharge,
        'Charged energy [kWh]': energyCharged,
        'Total energy consumed [kWh]': totalEnergyConsumed,
        'Battery SoC [%]': batterySoC,
        'Total charging time [min]': chargingTime,
        'Cost per charge [USD]': totalEnergyCost,
        'Total distance covered [km]': vehicleSpeed
    }

    # Crear una figura combinada
    plt.figure(figsize=(14, 8))

    # Asignar colores a las métricas
    colors = sns.color_palette("magma", len(metrics))

    # Graficar cada métrica
    width = 0.12  # Ancho de las barras
    positions = list(range(len(totalEnergyConsumed)))
    for i, (label, data) in enumerate(metrics.items()):
        plt.bar(
            [p + i * width for p in positions],
            data.values,
            width=width,
            label=label,
            color=colors[i]
        )

    # Configurar ejes y leyendas
    plt.xticks([p + width * (len(metrics) / 2 - 0.5) for p in positions], totalEnergyConsumed.index, rotation=45, fontsize=12, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar figura
    plt.tight_layout()
    plt.show()

def create_subplots(data):
    # Convertir segundos a timedelta
    data['timedelta'] = pd.to_timedelta(data['timestep_time'], unit='s')

    # Usar una fecha base para calcular tiempos en un día
    data['time'] = pd.to_datetime('2024-11-28') + data['timedelta']



    # Crear subplots: 6 filas, 1 columna
    fig, axes = plt.subplots(6, 1, figsize=(12, 8), sharex=True)  # `sharex=True` para compartir el eje X
    fig.tight_layout(pad=2)  # Ajustar espacio entre subplots

    # Graficar cada vehículo en su subplot
    for i, (vehicle_id, group) in enumerate(data.groupby('vehicle_id')):
        ax = axes[i]  # Seleccionar subplot correspondiente
        ax.plot(group['time'], group['vehicle_energyCharged'], label=vehicle_id)
        ax.set_title(f'{vehicle_id}')  # Título con el nombre del vehículo
        ax.set_ylabel('Potencia (kW)')
        ax.grid()

        # Configurar marcas de tiempo en el eje X
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))  # Marcas principales cada hora
        # ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))  # Marcas secundarias cada 15 minutos
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Formato HH:MM:SS

    # Configurar el último subplot con etiquetas del eje X
    # axes[-1].set_xlabel('Time (HH:MM)')
    plt.xticks(rotation=45)

    # Mostrar gráfico
    plt.show()
    # plt.savefig("H:\\My Drive\\Articulos tesis\\FINAL\\EVCS\\charging.png")

def legend_plot(data):
    
    # Convertir segundos a timedelta
    data['timedelta'] = pd.to_timedelta(data['timestep_time'], unit='s')

    # Usar una fecha base para calcular tiempos en un día
    data['time'] = pd.to_datetime('2024-11-28') + data['timedelta']
    
    # Crear un solo gráfico
    plt.figure(figsize=(12, 6))

    # Graficar cada vehículo en el mismo plot
    for vehicle_id, group in data.groupby('vehicle_id'):
        plt.plot(group['time'], group['vehicle_energyCharged'], label=vehicle_id)

    # Configurar título, etiquetas y leyenda
    plt.xlabel('Time (HH:MM)')
    plt.ylabel('Power (kW)')
    plt.grid()

    # Personalizar el formato del eje X a HH:MM:SS
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Configurar marcas en el eje X
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))  # Marcas principales cada hora

    # Ajustar las etiquetas del eje X
    plt.xticks(rotation=45)

    # Agregar la leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.show()

def Change2spanish(df):
    
    # Reemplazar "vehicle" por "vehículo" en todo el DataFrame
    df = df.applymap(lambda x: x.replace('Vehicle_0', 'Vehículo_0') if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('Vehicle_1', 'Vehículo_1') if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('Vehicle_2', 'Vehículo_2') if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('Vehicle_3', 'Vehículo_3') if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('Vehicle_4', 'Vehículo_4') if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('Vehicle_5', 'Vehículo_5') if isinstance(x, str) else x)

    return df


# 200kW
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\19-09-2024\\Battery.out.csv'  
df200 = pd.read_csv(filePath, sep=';')

# 20kW ?
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\20-09-2024\\Battery.out.csv'  
df20 = pd.read_csv(filePath, sep=';')

# 50kW
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\28-11-2024\\Battery.out_es.csv' 
df50 = pd.read_csv(filePath, sep=';')

# 7.4kW
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\29-11-2024\\Battery.out.csv' 
df7 = pd.read_csv(filePath, sep=';')

# 200kW 5 days
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\19-09-2024\\Battery5days.out.csv'  
df200_5d = pd.read_csv(filePath, sep=';')

## figures
# legend_plot(df7)
# bar_plots(df7)
# bar_plots(df50)
# bar_subplots(df7, df50)
Change2spanish(df200_5d)
create_subplots(Change2spanish(df200_5d))