import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
df = pd.read_csv('H:\Mi unidad\Artículos tesis\DESARROLLO\Ob2\OUTCOMES\PrecBolsNaci_Enero_Septiembre.csv')

# Crear una lista con los nombres de las columnas correspondientes a las horas
hours_columns = [f'Values_Hour{str(i).zfill(2)}' for i in range(1, 25)]

# Calcular el promedio para cada hora
hourly_means = df[hours_columns].mean()

# Crear la gráfica del promedio por hora
plt.figure(figsize=(10, 6))
plt.plot(range(1, 25), hourly_means, marker='o')

# Agregar título y etiquetas
plt.title('Promedio de Valores por Hora del Día')
plt.xlabel('Hora del día')
plt.ylabel('Promedio de valor')
plt.xticks(range(1, 25))

# Mostrar la gráfica
plt.grid(True)
plt.show()