import pandas as pd
import os
import Recorte_Test as RT

def Add_Investment(df):
    df['flujos_caja'] = df['flujos_caja'].apply(eval)
    df['NPV'] = df['NPV'].apply(eval)
    df['NPV'] = df.apply(lambda row: [row['flujos_caja'][0]] + row['NPV'], axis=1)
    return df

# Ruta de la carpeta con los CSV
carpeta = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\todo'  # <- Cambia esto por la ruta real

# Etiquetas de sensibilidad
etiquetas = [
    "Sensitivity",
    "DI5_DR5",
    "DI15_DR5",
    "DI25_DR5",
    "DI5_DR10",
    "DI15_DR10",
    "DI25_DR10",
    "DI5_DR15",
    "DI15_DR15",
    "DI25_DR15"
]

# Orden deseado de las columnas finales
orden_columnas = [
    "Sensitivity",
    "L2_BC",
    "L2_PV4k",
    "L2_PV4k_TF",
    "L2_PV4k_TF_SB",
    "L2_TF_SB",
    "L2_PV40k_TF_SB",
    "L3_BC",
    "L3_PV4k",
    "L3_PV4k_TF",
    "L3_PV4k_TF_SB",
    "L3_TF_SB",
    "L3_PV40k_TF_SB",
    "L2_L3_PV40k_TF_SB",
    "L3_PV4k_TF_SB_DF"
]

# Cargar y procesar los CSV
archivos_csv = [f for f in os.listdir(carpeta) if f.endswith('.csv')]
df_acumulado = pd.DataFrame()

for archivo in archivos_csv:
    ruta_completa = os.path.join(carpeta, archivo)
    nombre_base = os.path.splitext(archivo)[0]
    try:
        df = pd.read_csv(ruta_completa)
        df = df.apply(RT.truncar_listas, axis=1)
        df = Add_Investment(df)
        df['NPV_final'] = df['NPV'].apply(lambda x: x[-2] if len(x) >= 2 else None)
        df_acumulado[nombre_base] = df['NPV_final'].iloc[:len(etiquetas)-1]
    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

# Insertar la columna de sensibilidad
df_acumulado.insert(0, 'Sensitivity', etiquetas[1:])

# Eliminar valores negativos
df_acumulado.iloc[:, 1:] = df_acumulado.iloc[:, 1:].applymap(lambda x: x if pd.isna(x) or x >= 0 else None)

# Reordenar columnas
columnas_disponibles = [col for col in orden_columnas if col in df_acumulado.columns]
df_acumulado = df_acumulado[columnas_disponibles]

# Guardar archivo
salida = os.path.join(carpeta, 'resultado_acumulado.csv')
df_acumulado.to_csv(salida, index=False)

print(f"Archivo guardado en: {salida}")
