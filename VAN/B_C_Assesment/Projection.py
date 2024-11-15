# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error

# # Cargar los datos desde el archivo CSV
# file_path = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\PrecBolsNaci_2000_2024.csv'
# df = pd.read_csv(file_path)

# # Convertir la columna 'Date' a tipo datetime
# df['Date'] = pd.to_datetime(df['Date'])

# # Organizar el DataFrame por la columna 'Date' de forma ascendente
# df = df.sort_values(by='Date').reset_index(drop=True)

# # Convertir la columna 'Date' en un índice de tipo datetime
# df.set_index('Date', inplace=True)

# # Seleccionar la serie temporal a modelar
# time_series = df['Values_Hour01']

# # Crear características (lags) para usar como entradas al modelo
# def create_features(series, lags):
#     X, y = [], []
#     for i in range(lags, len(series)):
#         X.append(series[i-lags:i].values)
#         y.append(series[i])
#     return np.array(X), np.array(y)

# # Crear las características con lags
# lags = 1000  # Número de lags a considerar
# X, y = create_features(time_series, lags)

# # Dividir los datos en entrenamiento y prueba
# split_index = int(0.8 * len(y))
# X_train, X_test = X[:split_index], X[split_index:]
# y_train, y_test = y[:split_index], y[split_index:]

# # Obtener las fechas correspondientes al conjunto de prueba
# dates = time_series.index[lags:]  # Las fechas correspondientes a y
# dates_train = dates[:split_index]
# dates_test = dates[split_index:]

# # Configurar y entrenar el modelo Random Forest
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Realizar predicciones en el conjunto de prueba
# predictions = model.predict(X_test)

# # Calcular el error cuadrático medio (MSE)
# mse = mean_squared_error(y_test, predictions)
# print(f"Mean Squared Error: {mse:.2f}")

# # Generar nuevas fechas desde la última fecha hasta el 31 de diciembre de 2054
# last_date = time_series.index[-1]
# future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), end='2054-12-31', freq='D')

# # Crear un conjunto de datos de predicción para las fechas futuras
# future_predictions = []

# # Usar los últimos `lags` valores de la serie original para comenzar las predicciones
# current_values = time_series[-lags:].values

# for _ in range(len(future_dates)):
#     # Predecir el siguiente valor
#     next_prediction = model.predict([current_values])[0]
#     future_predictions.append(next_prediction)
    
#     # Actualizar los valores actuales con el nuevo valor predicho
#     current_values = np.append(current_values[1:], next_prediction)

# # Crear un DataFrame para los datos de entrenamiento
# train_df = pd.DataFrame({
#     'Date': dates_train,
#     'Values': y_train,
#     'Type': 'Training'
# })

# # Crear un DataFrame para los datos reales de prueba
# test_df = pd.DataFrame({
#     'Date': dates_test,
#     'Values': y_test,
#     'Type': 'Actual'
# })

# # Crear un DataFrame para las predicciones en el conjunto de prueba
# predictions_df = pd.DataFrame({
#     'Date': dates_test,
#     'Values': predictions,
#     'Type': 'Prediction'
# })

# # Crear un DataFrame para las predicciones futuras
# future_predictions_df = pd.DataFrame({
#     'Date': future_dates,
#     'Values': future_predictions,
#     'Type': 'Future Prediction'
# })

# # Combinar todos los DataFrames en uno solo
# train_prediction = pd.concat([train_df, test_df, predictions_df, future_predictions_df], ignore_index=True)
# # train_prediction.to_csv('H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\Values_Hour01_prediction.csv', index=False)


# # Visualizar los resultados con las fechas en el eje x
# plt.figure(figsize=(14, 8))
# plt.plot(dates_train, y_train, label='Entrenamiento')
# plt.plot(dates_test, y_test, label='Datos reales', color='orange')
# plt.plot(dates_test, predictions, label='Predicción', color='red')
# plt.plot(future_dates, future_predictions, label='Predicciones futuras', color='green')
# plt.legend()
# plt.xlabel('Fecha')
# plt.ylabel('Valores')
# plt.title('Random Forest - Predicción hasta 2054')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig("Values_Hour01_prediction_lags=1000_oct.png", bbox_inches='tight')
# plt.show()

























# # import pandas as pd
# # from pmdarima import auto_arima
# # import numpy as np

# # # Cargar los datos desde el archivo CSV
# # file_path = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\PrecBolsNaci_2000_2024.csv'
# # df = pd.read_csv(file_path)

# # # Asegúrate de que la columna Date sea de tipo datetime
# # df['Date'] = pd.to_datetime(df['Date'])

# # # Establecer la columna Date como índice
# # df.set_index('Date', inplace=True)

# # # Proyección para cada columna de Values_Hour
# # results = {}

# # # Definir el rango de proyección en años y horas
# # n_years = 30
# # n_hours = n_years * 365 * 24  # Número total de horas en 30 años

# # # Iterar sobre las columnas de Values_Hour
# # for col in df.columns[2:]:  # Asumiendo que las primeras dos columnas no son de Values_Hour
# #     # Ajustar el modelo ARIMA usando auto_arima
# #     model = auto_arima(df[col], seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)

# #     # Hacer la proyección
# #     forecast, conf_int = model.predict(n_periods=n_years, return_conf_int=True)

# #     # Guardar los resultados
# #     results[col] = forecast

# # # Convertir los resultados a un DataFrame para facilitar el uso
# # forecast_df = pd.DataFrame(results)

# # # Mostrar el DataFrame de proyección
# # print(forecast_df)





# # import pandas as pd

# # # Cargar el archivo CSV
# # file_path = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\PrecBolsNaci_2000_2024.csv'
# # df = pd.read_csv(file_path)

# # # Convertir la columna 'Date' a tipo datetime
# # df['Date'] = pd.to_datetime(df['Date'])

# # # Organizar el DataFrame por la columna 'Date' de forma ascendente
# # df = df.sort_values(by='Date').reset_index(drop=True)

# # # Convertir la columna de fecha a un formato de fecha y configurar como índice
# # df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  # Ajusta el formato de fecha si es necesario
# # df.set_index('Date', inplace=True)

# # # Verifica el formato de tu DataFrame
# # print(df.head())

# # from nixtla import NixtlaClient

# # # Configura tu cliente con la clave API
# # api_key = "nixak-6vvdydamDBMSTsw9q7XIJFz1Ut2R6ZeA9TI7Yz3NBZdsPGN30SaUzJ5n2KO3eTH4sh8zJ9N34lYEy2gH"
# # nixtla_client = NixtlaClient(api_key=api_key)

# # # Realizar la predicción, ajustando 'h' al número de periodos futuros deseados
# # h = 365 * 30  # Por ejemplo, predicción para los próximos 24 meses, semanas, etc., según tu frecuencia
# # fcst_df = nixtla_client.forecast(df, h=h, time_col='Date', target_col='Values_Hour01', freq='D')  # Ajusta la frecuencia (M, W, D)

# # # Mostrar el resultado
# # print(fcst_df)

# # import matplotlib.pyplot as plt

# # # Graficar los datos originales y las predicciones
# # plt.figure(figsize=(10, 6))
# # plt.plot(df.index, df['Values_Hour01'], label='Datos Históricos')
# # plt.plot(fcst_df['Date'], fcst_df['TimeGPT'], label='Predicciones', linestyle='--')
# # plt.legend()
# # plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# Cargar los datos
df = pd.read_csv('H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\PrecBolsNaci_2000_2024.csv')

# Convertir la columna 'Date' a tipo datetime
df['Date'] = pd.to_datetime(df['Date'])

# Organizar el DataFrame por la columna 'Date' de forma ascendente
df = df.sort_values(by='Date').reset_index(drop=True)

# Convertir la columna 'Date' en un índice de tipo datetime
df.set_index('Date', inplace=True)

# Verificar que la columna 'Values_Hour01' exista
if 'Values_Hour01' in df.columns:
    # Extraer los datos de la columna
    x = np.arange(len(df['Values_Hour01']))  # Asumimos que x es el índice de cada valor
    y = df['Values_Hour01'].dropna()  # Remover valores nulos si existen

    # Ajuste polinomial (puedes cambiar el grado según lo necesario)
    grado = 1  # Grado del polinomio
    coeficientes = np.polyfit(x[:len(y)], y, grado)
    print(coeficientes)
    polinomio = np.poly1d(coeficientes)
    print(polinomio)

    x_p = np.arange(len(df['Values_Hour01']) + 7300)
    # Generar valores ajustados
    y_ajustado = polinomio(x_p)

    # Graficar los datos originales y el ajuste polinomial
    plt.figure(figsize=(10, 6))
    plt.scatter(x[:len(y)], y, label='Datos originales', color='blue', s = 5)
    plt.plot(x_p, y_ajustado, label=f'Ajuste polinomial de grado {grado}', color='red')
    plt.xlabel('Índice')
    plt.ylabel('Values_Hour01')
    plt.legend()
    plt.title('Ajuste polinomial a los datos de Values_Hour01')
    plt.show()
else:
    print("La columna 'Values_Hour01' no se encuentra en el archivo.")

# Calcular el promedio de cada columna
promedios = df.mean(numeric_only=True)

# Mostrar los resultados
print("Promedio de cada columna:")
print(promedios)