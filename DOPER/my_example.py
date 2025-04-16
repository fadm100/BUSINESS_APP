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

print("parameter 'system' object:")
pprint(parameter['system'])
print('')

print("parameter 'batteries' object:")
pprint(parameter['batteries'])
print('')

data = ts_inputs(parameter, load='B90', scale_load=10000, scale_pv=0)
data = ts_inputs_ev_schedule(parameter, data)
file_path = r"H:\\My Drive\Articulos tesis\\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\data.csv"
data.to_csv(file_path, sep=';', index=False, encoding='utf-8')
total_demand_0 = data['battery_EV0_demand'].sum()
print('La suma de battery_EV0_demand es = ', total_demand_0)
total_demand_1 = data['battery_EV1_demand'].sum()
print('La suma de battery_EV1_demand es = ', total_demand_1)
total_demand_2 = data['battery_EV2_demand'].sum()
print('La suma de battery_EV2_demand es = ', total_demand_2)

# Define the path to the solver executable
solver_path = 'H:\\My Drive\Articulos tesis\\DESARROLLO\\Ob2\\Simulations\\DOPER\\doper\\solvers\\Windows64\\cbc.exe'
# Initialize DOPER
smartDER = DOPER(model=control_model,
                 parameter=parameter,
                 solver_path=solver_path)

# Conduct optimization
res = smartDER.do_optimization(data)

# Get results
duration, objective, df, model, result, termination, parameter = res
file_path = r"H:\\My Drive\Articulos tesis\\DESARROLLO\\Ob2\\Simulations\\DOPER\\Dataframe\\df.csv"
df.to_csv(file_path, sep=';', index=False, encoding='utf-8')
print(standard_report(res))

plotData = my_plot_dynamic(df, parameter, plotFile = None, plot_reg=False)

total_charge = df['Battery Charging Power [kW]'].sum()
print('La carga total de las baterias es = ', total_charge)
print('El costo total de carga de las baterias es = ', total_charge * 0.08)

# Seleccionar la columna de interés
discharge_column = 'Battery Discharging Power [kW]'

# Crear una máscara booleana: True si el valor es mayor a 0
mask = df[discharge_column] > 0

# Crear un grupo único cada vez que comienza una nueva secuencia de valores > 0
group = (mask != mask.shift()).cumsum()

# Filtrar solo los grupos donde mask es True (i.e., valores > 0)
df['group'] = group.where(mask)

# Agrupar por los grupos válidos y sumar
group_sums = df.groupby('group')[discharge_column].sum().dropna()
print('Los grupos de descarga son = ', group_sums)

total_discharge = group_sums.tolist()
print('La descarga en el primer pico es = ', total_discharge[0])
print('El costo total de descarga en el primer pico es = ', total_discharge[0] * 0.48)
print('La descarga en el segundo pico es = ', total_discharge[1])
print('El costo total de descarga en el segundo pico es = ', total_discharge[1] * 0.48)
print('La descarga en el valle es = ', total_discharge[2])
print('El costo total de descarga en el valle es = ', total_discharge[2] * 0.48)

print('La descarga total de las baterias es = ', group_sums.sum())
print('El costo total de descarga de las baterias es = ', total_discharge[0] * 0.48 + total_discharge[1] * 0.48 + total_discharge[2] * 0.48)




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
