import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def HeatMap_subplot(data1, data2, name, scale1, scale2, variable1, variable2, fmt):
    # Normalización y limpieza
    data1.replace('Null', np.nan, inplace=True)
    data2.replace('Null', np.nan, inplace=True)

    data1.set_index('Sensitivity', inplace=True)
    data2.set_index('Sensitivity', inplace=True)

    data_numeric1 = data1.apply(pd.to_numeric, errors='coerce') / scale1
    data_numeric2 = data2.apply(pd.to_numeric, errors='coerce') / scale2

    # Crear función para definir colores condicionales en los números
    def annotation_colors(values):
        return np.where(values > 0, 'black', 'white')  # Negro para positivos, blanco para negativos

    # Crear figura y subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    heatmap1 = sns.heatmap(
        data_numeric1,
        annot=True,
        annot_kws={"size": 12, "weight": "bold"},
        cmap='viridis',  # Paleta original
        center=0,  # Asegurar el punto neutro en 0
        fmt=fmt,
        linewidths=0.5,
        linecolor='black',
        cbar_kws={'label': variable1, 'shrink': 0.7},
        mask=data_numeric1.isnull(),
        square=True,
        ax=axes[0]
    )
    axes[0].set_title(variable1, fontsize=14, weight='bold')

    # Aplicar colores personalizados a las anotaciones
    for text, value in zip(heatmap1.texts, data_numeric1.values.flatten()):
        if not np.isnan(value):  # Evitar valores NaN
            text.set_color('black' if value > 0 else 'white')

    heatmap2 = sns.heatmap(
        data_numeric2,
        annot=True,
        annot_kws={"size": 12, "weight": "bold"},
        cmap='viridis',  # Paleta original
        center=0,  # Asegurar el punto neutro en 0
        fmt=fmt,
        linewidths=0.5,
        linecolor='black',
        cbar_kws={'label': variable2, 'shrink': 0.7},
        mask=data_numeric2.isnull(),
        square=True,
        ax=axes[1]
    )
    axes[1].set_title(variable2, fontsize=14, weight='bold')

    # Aplicar colores personalizados a las anotaciones
    for text, value in zip(heatmap2.texts, data_numeric2.values.flatten()):
        if not np.isnan(value):  # Evitar valores NaN
            text.set_color('black' if value > 0 else 'white')

    # Ajustar y guardar
    plt.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.show()

def HeatMap(data, name, scale, variable, vmin=None, vmax=None, color='white', fmt=".1f", cmap='viridis'):
    """
    Genera un heatmap con la escala de colores 'viridis' y permite ajustar los límites de la escala.

    Parameters:
    - data: DataFrame de entrada.
    - name: Nombre del archivo para guardar el gráfico.
    - scale: Escala para normalizar los valores.
    - variable: Etiqueta para la barra de color.
    - vmin: Límite mínimo de la escala de colores (opcional).
    - vmax: Límite máximo de la escala de colores (opcional).
    """

    # Reemplazar 'Null' con NaN
    data.replace('Null', np.nan, inplace=True)

    # Configurar el índice y seleccionar las columnas numéricas
    data.set_index('Sensitivity', inplace=True)
    data_numeric = data.apply(pd.to_numeric, errors='coerce') / scale  # Convertir todo a numérico

    # Crear el heatmap
    plt.figure(figsize=(12, 8))
    heatmap = sns.heatmap(
        data_numeric,
        annot=True,
        annot_kws={"size": 12, "weight": "bold"},  # Personalizar tamaño y estilo de los números
        cmap=cmap,
        fmt=fmt,
        linewidths=0.5,
        linecolor='black',
        cbar_kws={'label': variable},
        mask=data_numeric.isnull(),  # Enmascarar los valores NaN
        square=True,  # Asegurar celdas cuadradas
        vmin=vmin,  # Límite mínimo de la escala de colores
        vmax=vmax   # Límite máximo de la escala de colores
    )

    # Personalizar fuente de la barra de color
    cbar = heatmap.collections[0].colorbar
    cbar.ax.yaxis.label.set_size(14)  # Tamaño de la etiqueta
    cbar.ax.yaxis.label.set_weight('bold')  # Negrita para la etiqueta

    # Cambiar colores de las anotaciones a blanco
    for text in heatmap.texts:
        text.set_color(color)  # Siempre blanco

    # Guardar y mostrar el gráfico
    plt.savefig(name, bbox_inches='tight')  # Ajustar los márgenes
    plt.show()


# Función para normalizar los datos a 1
def normalize_dataframe(df):
    # Convierte todas las columnas a numéricas cuando sea posible y ignora errores
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    # Encuentra el valor máximo
    max_value = df_numeric.max().max()  # Encuentra el máximo en todo el DataFrame
    # Divide todos los valores del DataFrame por el valor máximo
    df_normalized = df_numeric / max_value
    # df_normalized = df_normalized.fillna(df)
    return df_normalized

def normalize_row(df):
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    max_value = df_numeric.max(axis=1)  # Encuentra el máximo en todo el DataFrame
    # Dividir cada fila entre su valor máximo
    normalized_df = df_numeric.div(max_value, axis=0)
    return normalized_df

# Cargar los datos
file_path = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\HeatMapYear.csv'
data1 = pd.read_csv(file_path)

# Normalizar los DataFrames
df1_normalized = normalize_dataframe(data1)

# Cargar los datos
file_path = 'H:\\My Drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\HeatMapNPV.csv'
data2 = pd.read_csv(file_path)

df2_normalized = normalize_dataframe(data2)

df_weighted = (1 - df1_normalized) * 0.6 +  df2_normalized * 0.4
df_weighted = df_weighted.fillna(data1)

df_row_normalized = normalize_row(data2)
df_row_weighted = (1 - df1_normalized) * 0.6 +  df_row_normalized * 0.4
df_row_weighted = df_row_weighted.fillna(data1)

# HeatMap(data1, 'Years_HeatMap', scale=1, variable='Payback period', vmin=0, vmax=20, color='black', cmap='RdBu_r')
custom_cmap = LinearSegmentedColormap.from_list(
    "CustomMultiColor",
    ["#FF2300", "#ff745e", "#35B779", "#FDE725"]  # Lista de colores
)
HeatMap(data2, 'NPV_HeatMap', scale=1000, variable='NPV', vmin=-350.0, vmax=180, color='black', fmt=".1f", cmap=custom_cmap)
# HeatMap(df_weighted, 'Weighted_HeatMap', scale=1, variable='', vmin=0.0, vmax=0.8, color='black', fmt=".2f", cmap=sns.diverging_palette(0, 120, as_cmap=True))
# HeatMap(df_row_weighted, 'Row_Weighted_HeatMap', scale=1, variable='', vmin=-0.5, vmax=1, color='black', fmt=".2f")

# # Usar las nuevas funciones
# HeatMap_subplot(data1, data2, 'Years_and_NPV_HeatMap', scale1=1, scale2=1000, variable1='Payback period', variable2='NPV', fmt=".1f")
# HeatMap_subplot(df_weighted, df_row_weighted, 'Weighted_and_Row_Weighted_HeatMap', scale1=1, scale2=1, variable1='Weighted', variable2='Row Weighted', fmt=".2f")