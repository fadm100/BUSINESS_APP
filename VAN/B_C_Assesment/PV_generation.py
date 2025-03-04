import pvlib
import pandas as pd
import matplotlib.pyplot as plt
import json

# Cargar datos de irradiancia y temperatura estación Davis
filePath = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\Datos_davis.csv'
df_davis = pd.read_csv(filePath, sep=';')

irradiancia = df_davis['Solar rad.']
temperatura_celda = (df_davis['Temp out'] - 32) * 5 / 9

# Parámetros del módulo fotovoltaico
parametros_modulo = {
    'pdc0': 500,  # Potencia nominal en condiciones estándar (W)
    'gamma_pdc': -0.004,  # Coeficiente de temperatura de la potencia (1/°C)
}

numero_paneles = 80

# Crear el sistema fotovoltaico
sistema_pv = pvlib.pvsystem.PVSystem(module_parameters=parametros_modulo)

# Calcular la potencia generada usando el modelo PVWatts y agregar la nueva columna a df_davis
df_davis['Power_Gen'] = sistema_pv.pvwatts_dc(g_poa_effective=irradiancia, temp_cell=temperatura_celda) / 1e3 * numero_paneles

# Reemplazar 'p. m.' y 'a. m.' con 'PM' y 'AM' (quitando espacios adicionales)
df_davis['Time'] = df_davis['Time'].str.replace('p. m.', 'PM').str.replace('a. m.', 'AM')

# Combinar las columnas 'Date' y 'Time' en una sola columna de tipo datetime
df_davis['DateTime'] = pd.to_datetime(df_davis['Date'] + ' ' + df_davis['Time'], format='%d/%m/%Y %I:%M %p')

# Configurar la columna DateTime como índice
df_davis.set_index('DateTime', inplace=True)

# Crear la figura y el primer eje
fig, ax1 = plt.subplots()

# Graficar la potencia generada en el primer eje (izquierda)
ax1.plot(df_davis.index, df_davis['Power_Gen'], label='Generated power [kW]', color='green')
ax1.plot(df_davis.index, irradiancia / 1000, label='Solar radiation [kW/m^2]', color='orange')

# Etiquetas y título para el primer eje
# ax1.set_xlabel('Time')
ax1.tick_params(axis='y', labelcolor='black', labelsize=12)

# Cambiar el tamaño de la fuente de las etiquetas del eje X usando plt.xticks
plt.xticks(fontsize=12)  # Cambia 12 por el tamaño que prefieras

# Crear el segundo eje
ax2 = ax1.twinx()

# Graficar la temperatura externa en el segundo eje (derecha)
ax2.plot(df_davis.index, temperatura_celda, label='Temperature [°C]', color='blue')

# Etiquetas para el segundo eje
ax2.tick_params(axis='y', labelcolor='blue', labelsize=12)
ax2.set_ylim(0, 30)

# Agregar título y leyenda
ax1.legend(loc='upper left', fontsize=12)
ax2.legend(loc='upper right', fontsize=12)

# Mostrar la gráfica
plt.show()

############# Calcular la energía en kWh
# Convertir la columna 'Date' a tipo datetime
df_davis['Date'] = pd.to_datetime(df_davis['Date'], format='%d/%m/%Y')

# Agrupar por la columna 'Date' y sumar la columna 'Solar energy' para cada día
daily_solar_energy = df_davis.groupby('Date')['Power_Gen'].sum().reset_index()
# Pasa de min a horas para tener kWh cada intervalo de 5min corresponde a 5/60 horas
daily_solar_energy['Power_Gen'] = daily_solar_energy['Power_Gen'] * 1 / 12 
# se filtra el primer y ultimo día ya que estan incompletos, ambos generan menos de 5 kWh en el día
promedio = daily_solar_energy['Power_Gen'][daily_solar_energy['Power_Gen']>5].mean()

# Guardar el promedio en kWh/día, kWh/mes y el costo de inversión en en un archivo JSON
# Costo inversión sistema 3 o 4 kWpico 11.075.822 $COP --> https://autosolar.co/kits-solares-red/kit-solar-ongrid-3000w-12800whdia-growatt
# Costo instalación 7.1% del costo de compra del sistema --> U.S. Solar Photovoltaic System and Energy Storage Cost Benchmarks Q1 2023
# Mantenimiento 150 Euros = 700000 COP al año--> https://autosolar.co/kits-solares-red/kit-solar-ongrid-3000w-12800whdia-growatt

acquisition_cost = 11075822
installation_cost = acquisition_cost * 0.071

datos_PV_syst = {
    'Costo compra': acquisition_cost,
    'Costo instalación': installation_cost,
    'Costo mantenimiento': 700000,
    'Promedio kWh/dia': promedio,
    'Promedio kWh/mes': promedio * 30
}

print(datos_PV_syst)

with open('H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\promedios.json', 'w') as file:
    json.dump(datos_PV_syst, file, indent=4)

###############################################################################################################################################

# Cargar el archivo con el separador correcto

# Renombrar la columna de fecha correctamente
df_davis.rename(columns={df_davis.columns[0]: "Date"}, inplace=True)

# Filtrar los datos para el 14 de marzo de 2024 y seleccionar la columna "Solar rad."
df_filtered = df_davis[df_davis["Date"] == "14/03/2024"][["Time", "Solar rad."]]

lista_datos = df_filtered["Solar rad."].values.tolist()
print(lista_datos)
print(len(lista_datos))