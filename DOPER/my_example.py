import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from doper import DOPER, get_solver, get_root, standard_report
from doper.models.basemodel import base_model
from doper.models.battery import add_battery, plot_battery1
from doper.examples.example import parameter_add_evfleet, ts_inputs, test_default_parameter, ts_inputs_ev_schedule
from doper.plotting import my_plot_dynamic

from pyomo.environ import Objective, minimize

def control_model(inputs, parameter):
    model = base_model(inputs, parameter)
    model = add_battery(model, inputs, parameter)
    
    def objective_function(model):
        return model.sum_energy_cost * parameter['objective']['weight_energy'] \
               + model.sum_export_revenue * parameter['objective']['weight_export']
              
    model.objective = Objective(rule=objective_function, sense=minimize, doc='objective function')
    return model

parameter = test_default_parameter()
parameter = parameter_add_evfleet(parameter)

# print("parameter 'system' object:")
# pprint(parameter['system'])
# print('')

# print("parameter 'batteries' object:")
# pprint(parameter['batteries'])
# print('')

data = ts_inputs(parameter, load='B90', scale_load=100000, scale_pv=0)
data = ts_inputs_ev_schedule(parameter, data)
file_path = r"H:\\My Drive\Articulos tesis\\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\data.csv"
data.to_csv(file_path, sep=';', index=False, encoding='utf-8')

cols = [col for col in data.columns if col.startswith('battery_EV') and col.endswith('_demand')]
total_demand = data[cols].sum().sum()

# for col in cols:
#     print(f'La suma de {col} es = {data[col].sum()}')
#     print(f'El máximo de {col} es = {data[col].max()}')

print('La demanda de todos los buses es =', total_demand)

# Define the path to the solver executable
solver_path = 'H:\\My Drive\Articulos tesis\\DESARROLLO\\Ob2\\Simulations\\DOPER\\doper\\solvers\\Windows64\\cbc.exe'
# Initialize DOPER

# print('DEPURATION')
# parameter['print_infeasible_constraints'] = True

smartDER = DOPER(model=control_model,
                 parameter=parameter,
                 solver_path=solver_path)

# Conduct optimization
res = smartDER.do_optimization(data)

# # Configurar logger para permitir impresión de restricciones infactibles
# import logging
# for handler in logging.root.handlers[:]:
#     logging.root.removeHandler(handler)
# logging.basicConfig(level=logging.INFO)

# from pyomo.util.infeasible import log_infeasible_constraints
# log_infeasible_constraints(smartDER.model)



# Get results
duration, objective, df, model, result, termination, parameter = res
file_path = r"H:\\My Drive\Articulos tesis\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\df.csv"
df.to_csv(file_path, sep=';', index=False, encoding='utf-8')
print(standard_report(res))

plotData = my_plot_dynamic(df, parameter, plotFile = None, plot_reg=False)

total_charge = df['Battery Charging Power [kW]'].sum() / 12 # en una hora hay 12 paquetes de 5min entonces el resultado son kWh
print('La carga total de las baterías es = ', total_charge)
charging_Cost = df['Battery Charging Power [kW]'] * df['Tariff Energy [$/kWh]'] 
print('El costo total de carga de las baterías es = ', charging_Cost.sum() / 12)
total_discharge = df['Battery Discharging Power [kW]'].sum() / 12 # en una hora hay 12 paquetes de 5min entonces el resultado son kWh
print('La descarga total de las baterías es = ', total_discharge)
print('El costo total de descarga de las baterías es = ', total_discharge * 0.08)

def availability_matrix_figure(condition):
    if condition:
        import seaborn as sns
        from matplotlib.colors import ListedColormap
        import numpy as np


        # Crear una tabla solo con las columnas de disponibilidad de batería
        battery_cols = [col for col in data.columns if 'battery_EV' in col and '_avail' in col]
        battery_matrix = data[battery_cols].T  # transponer para que EVs sean filas y pasos de tiempo columnas

        # Asegurar que la columna date_time sea de tipo datetime
        data['date_time'] = pd.to_datetime(data['date_time'])

        # Crear etiquetas de tiempo (horas:minutos)
        time_labels = data['date_time'].dt.strftime('%H:%M')

        # Crear un mapa de colores personalizado: 0 -> blanco, 1 -> verde
        custom_cmap = ListedColormap(['white', 'green'])

        # Crear heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(battery_matrix, cmap=custom_cmap, cbar=False, linewidths=0.5, linecolor='lightgray', vmin=0, vmax=1)

        # Personalizar ejes con etiquetas espaciadas
        step = 12  # Ajusta según la cantidad de etiquetas que quieras mostrar
        plt.xticks(ticks=range(0, len(time_labels), step), labels=time_labels[::step], rotation=45, ha='right')
        plt.yticks(ticks=np.arange(len(battery_cols)) + 0.5, labels=battery_cols, rotation=0)
        plt.xlabel("Hora")
        plt.ylabel("EV")
        plt.title("Disponibilidad de batería por EV (1 = verde, 0 = blanco)")
        plt.tight_layout()
        plt.show()

availability_matrix_figure(False)

##############################################################################################################################

# # Crear el gráfico
# plt.figure(figsize=(12, 6))

# # Graficar cada una de las columnas
# plt.plot(data.index, data['battery_EV0_avail'], label='Battery 0 Availability', linestyle='-', marker='o')
# plt.plot(data.index, data['battery_EV1_avail'], label='Battery 1 Availability', linestyle='--', marker='s')
# plt.plot(data.index, data['battery_EV2_avail'], label='Battery 2 Availability', linestyle=':', marker='^')

# # Configurar etiquetas y título
# plt.xlabel('Time', fontsize=12)
# plt.ylabel('Availability (0 or 1)', fontsize=12)
# plt.title('Battery Availability Over Time', fontsize=14)

# # Agregar leyenda
# plt.legend(loc='upper right', fontsize=10)

# # Mejorar formato del eje x
# plt.xticks(rotation=45)
# plt.grid(alpha=0.5)

# # Mostrar el gráfico
# plt.tight_layout()
# plt.show()

# import csv
# from pyomo.core import Var

# # Archivo CSV donde se guardará la salida
# output_csv = "H:\\My Drive\Articulos tesis\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\model_variables.csv"

# with open(output_csv, mode="w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Variable", "Index", "Value"])  # Encabezados del CSV
    
#     for v in model.component_objects(Var, active=True):
#         for index in v:
#             writer.writerow([str(v), str(index), v[index].value])

# print(f"Variables exportadas a {output_csv}")

# import pandas as pd
# import matplotlib.pyplot as plt
# from pyomo.core import Var
# import os

# # Crear una carpeta para guardar las gráficas y archivos CSV
# output_folder = "H:\\My Drive\Articulos tesis\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\ev_variable_results"
# os.makedirs(output_folder, exist_ok=True)

# # Procesar las variables relacionadas con los EV
# for v in model.component_objects(Var, active=True):
#     variable_name = str(v)

#     # Verificar si la variable está relacionada con los EV
#     if "battery" in variable_name.lower():
#         # Inicializar un diccionario para almacenar valores por EV
#         ev_data = {}

#         # Organizar los datos por EV
#         for index in v:
#             if isinstance(index, tuple) and len(index) > 1:  # Asegurar que el índice es un tuple
#                 ev_id = index[1]  # Extraer el ID del EV
#                 timestamp = index[0]  # Timestamp
#                 value = v[index].value  # Valor de la variable

#                 if ev_id not in ev_data:
#                     ev_data[ev_id] = {"timestamps": [], "values": []}
#                 ev_data[ev_id]["timestamps"].append(timestamp)
#                 ev_data[ev_id]["values"].append(value)

#         # Convertir datos a DataFrame y guardar como CSV
#         for ev_id, data in ev_data.items():
#             df1 = pd.DataFrame({
#                 "Timestamp": data["timestamps"],
#                 f"{variable_name}_EV_{ev_id}": data["values"]
#             })
            
#             # Convertir la columna a formato de fecha y hora en UTC
#             df1['datetime'] = pd.to_datetime(df1['Timestamp'], unit='s', utc=True)

#             # Guardar DataFrame en un archivo CSV
#             csv_path = os.path.join(output_folder, f"{variable_name}_EV_{ev_id}.csv")
#             df1.to_csv(csv_path, index=False)
#             print(f"Resultados guardados como CSV: {csv_path}")

#             # Graficar los datos
#             plt.figure(figsize=(10, 6))
#             plt.plot(df1["datetime"], df1[f"{variable_name}_EV_{ev_id}"], marker="o", linestyle="-", label=f"{variable_name} (EV {ev_id})")
#             plt.title(f"Variable: {variable_name} - EV {ev_id}")
#             plt.xlabel("datetime")
#             plt.ylabel("Value")
#             plt.xticks(rotation=45, fontsize=8)
#             plt.legend()
#             plt.grid(True)

#             # Guardar la gráfica como archivo PNG
#             plot_path = os.path.join(output_folder, f"{variable_name}_EV_{ev_id}.png")
#             plt.savefig(plot_path)
#             plt.close()
#             print(f"Gráfica guardada: {plot_path}")

#     else:
#         # Si la variable no está relacionada con EVs, se ignora
#         continue

# # Crear un DataFrame para almacenar los resultados
# availability_data = []

# # Iterar sobre los valores de ts (intervalos de tiempo) y battery (baterías)
# for ts in model.ts:
#     for battery in model.batteries:
#         # Acceder al valor de disponibilidad de la batería en el tiempo ts
#         availability = model.battery_available[ts, battery]  # No es necesario usar .value para parámetros
#         availability_data.append([ts, battery, availability])

# # Convertir los datos a un DataFrame de pandas para mayor claridad
# availability_df = pd.DataFrame(availability_data, columns=["Time Step", "Battery", "Availability"])

# # Graficar la disponibilidad para cada EV (batería)
# plt.figure(figsize=(10, 6))

# for battery in model.batteries:
#     # Filtrar los datos por cada batería (EV)
#     battery_data = availability_df[availability_df["Battery"] == battery]
#     plt.plot(battery_data["Time Step"], battery_data["Availability"], label=f'EV {battery}')

# # Añadir etiquetas y título
# plt.xlabel("Time Step")
# plt.ylabel("Availability")
# plt.title("Battery Availability Over Time")
# plt.legend(title="EVs")
# plt.grid(True)
# plt.show()

# for comp in model.component_objects():
#     print(comp)
# print('')
# print(model.sum_regulation_revenue.value)
