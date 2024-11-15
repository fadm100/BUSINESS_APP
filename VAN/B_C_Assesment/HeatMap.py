import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos
file_path = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\HeatMapYear.csv'
data = pd.read_csv(file_path)

# Reemplazar 'Null' con NaN
data.replace('Null', np.nan, inplace=True)

# Configurar el índice y seleccionar las columnas numéricas
data.set_index('Sensitivity', inplace=True)
data_numeric = data.apply(pd.to_numeric, errors='coerce')  # Convertir todo a numérico

# Crear el heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    data_numeric,
    annot=True,
    cmap='viridis',
    fmt=".1f",
    linewidths=0.5,
    linecolor='black',
    cbar_kws={'label': 'Valor'},
    mask=data_numeric.isnull(),  # Enmascarar los valores NaN
    square=True  # Asegurar celdas cuadradas
)

# Títulos y ajustes
plt.title("Heatmap con valores NaN en blanco", fontsize=16)
plt.show()
