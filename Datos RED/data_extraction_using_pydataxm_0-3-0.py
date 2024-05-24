from pydataxm import *                           #Se realiza la importación de las librerias necesarias para ejecutar
import datetime as dt  
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


objetoAPI = pydataxm.ReadDB()                    #Se almacena el servicio en el nombre objetoAPI

# df =objetoAPI.get_collections() #El método get_collection sin argumentos retorna todas las variables que se tienen disponible en la API y que se pueden consultar  
# df.head()                       #Se presentan como ejemplo las 5 primeras varibles disponibles

# df = df.to_json()

# # with open('MetricsList.json', 'w') as outfile:
# #     json.dump(df, outfile)

df_variable = objetoAPI.request_data(
                    "DemaReal",                    #Se indica el nombre de la métrica tal como se llama en el campo metricId
                    "Agente",                      #Se indica el nombre de la entidad tal como se llama en el campo Entity
                    dt.date(2021, 4, 29),           #Corresponde a la fecha inicial de la consulta
                    dt.date(2021, 4, 30),          #Corresponde a la fecha final de la consulta
                    filtros =['CDNC'])     #Se indican los códigos SIC de plantas dentro de una lista

print(df_variable)

# df_variable.to_csv('DemandaRealCEDENARComercializador_2024_4_29_a_2024_4_30.csv', header=False, index=False)
# plt.plot(df_variable.0)

# df_variable = df_variable.to_json()

# with open('DemandaRealCEDENARComercializador_2024_4_29_a_2024_4_30.json', 'w') as outfile:
#     json.dump(df_variable, outfile)

# df_cruces =objetoAPI.get_collections("DemaReal") #El método get_collection con argumentos retorna los cruces de las varibles que se quieren consultar
# df_cruces = df_cruces.to_json()

# with open('CrucesMetricaDemaReal.json', 'w') as outfile:
#     json.dump(df_cruces, outfile)