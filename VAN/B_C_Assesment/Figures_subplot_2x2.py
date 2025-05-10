# import pandas as pd

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_BC.csv'
# df_L2_BC = pd.read_csv(filePath, sep=',')

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_PV4k.csv'
# df_L2_PV4k = pd.read_csv(filePath, sep=',')

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_PV4k_TF.csv'
# df_L2_PV4k_TF = pd.read_csv(filePath, sep=',')

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_PV4k_TF_SB.csv'
# df_L2_PV4k_TF_SB = pd.read_csv(filePath, sep=',')

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_PV40k_TF_SB.csv'
# df_L2_PV40k_TF_SB = pd.read_csv(filePath, sep=',')

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_TF_SB.csv'
# df_L2_TF_SB = pd.read_csv(filePath, sep=',')


# df_total = pd.concat([df_L2_BC, df_L2_PV4k, df_L2_PV4k_TF, df_L2_PV4k_TF_SB, df_L2_PV40k_TF_SB, df_L2_TF_SB], ignore_index=True)
# df_total.to_csv('H:\\My drive\\Artículos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_total.csv', index=False)

###############################################################################################################################################################

# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\fast\\L3_BC.csv'
# df_L2_BC = pd.read_csv(filePath, sep=',')
# # Leer el DataFrame de costos de cargadores
# filePath = 'H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\fast\\L3_PV40k_TF_SB.csv'
# df_L2_PV40k_TF_SB = pd.read_csv(filePath, sep=',')

# def graficar(df_left, df_right):
    
#     df_left['vida_util'] = df_left['vida_util'].apply(eval)
#     df_left['NPV'] = df_left['NPV'].apply(eval)
#     df_left['flujos_caja'] = df_left['flujos_caja'].apply(eval)
    
#     fig, axes = plt.subplots(2, 2, figsize=(16, 8))  # Tamaño de la figura: 10x8 pulgadas
#     fig.subplots_adjust(hspace=0.3, wspace=0.3)  # Ajuste del espacio entre los subgráficos


#     # Graficar NPV para cada resultado
#     for _, row in df_left.iterrows():
#         axes[0,0].plot(row['vida_util'], row['NPV'], label=f"DI {row['crecimiento_demanda']:.0%}, DR {row['tasa_descuento']:.0%}")

#     # Configurar etiquetas y título
#     axes[0,0].set_xlabel('a)', fontsize=14, fontweight='bold')
#     axes[0,0].set_ylabel('NPV (USD)', fontsize=14, fontweight='bold')
#     axes[0,0].legend()
#     axes[0,0].set_xticklabels(axes[0,0].get_xticks(), fontsize=12, fontweight='normal')
#     axes[0,0].set_yticklabels(axes[0,0].get_yticks(), fontsize=12, fontweight='normal')
#     axes[0,0].grid()

#     # Encontrar índices de mejor y peor NPV_final
#     mejor_idx = df_left['NPV_final'].idxmax()
#     peor_idx = df_left['NPV_final'].idxmin()

#     # Graficar flujos de caja para el mejor y peor NPV_final
#     for idx, color, label in zip([mejor_idx, peor_idx], ['green', 'red'], ['Best NPV', 'Worst NPV']):
#         axes[1,0].bar(range(len(df_left['flujos_caja'].iloc[idx])),
#                 df_left['flujos_caja'].iloc[idx],
#                 label=f'{label}: {df_left["NPV_final"].iloc[idx]:.2f}',
#                 alpha=0.7, width=0.4, align='center' if idx == mejor_idx else 'edge', color=color)

#     # Configurar título y etiquetas
#     axes[1,0].set_xlabel('Year\nb)', fontsize=14, fontweight='bold')
#     axes[1,0].set_ylabel('Cash Flow (USD)', fontsize=14, fontweight='bold')
#     axes[1,0].legend(fontsize=12, title_fontsize='13', loc='best', frameon=True)

#     # Configurar etiquetas de los ejes
#     axes[1,0].set_xticklabels(axes[1,0].get_xticks(), fontsize=12, fontweight='normal')
#     axes[1,0].set_yticklabels(axes[1,0].get_yticks(), fontsize=12, fontweight='normal')

#     axes[1,0].grid(True)
    
#     #####################
    
#     df_right['vida_util'] = df_right['vida_util'].apply(eval)
#     df_right['NPV'] = df_right['NPV'].apply(eval)
#     df_right['flujos_caja'] = df_right['flujos_caja'].apply(eval)

#     # Graficar NPV para cada resultado
#     for _, row in df_right.iterrows():
#         axes[0,1].plot(row['vida_util'], row['NPV'], label=f"DI {row['crecimiento_demanda']:.0%}, DR {row['tasa_descuento']:.0%}")

#     # Configurar etiquetas y título
#     axes[0,1].set_xlabel('b)', fontsize=14, fontweight='bold')
#     # axes[0,1].set_ylabel('Net Present Value (NPV) (USD)', fontsize=14, fontweight='bold')
#     axes[0,1].legend()
#     axes[0,1].set_xticklabels(axes[0,1].get_xticks(), fontsize=12, fontweight='normal')
#     axes[0,1].set_yticklabels(axes[0,1].get_yticks(), fontsize=12, fontweight='normal')
#     axes[0,1].grid()

#     # Encontrar índices de mejor y peor NPV_final
#     mejor_idx = df_right['NPV_final'].idxmax()
#     peor_idx = df_right['NPV_final'].idxmin()

#     # Graficar flujos de caja para el mejor y peor NPV_final
#     for idx, color, label in zip([mejor_idx, peor_idx], ['green', 'red'], ['Best NPV', 'Worst NPV']):
#         axes[1,1].bar(range(len(df_right['flujos_caja'].iloc[idx])),
#                 df_right['flujos_caja'].iloc[idx],
#                 label=f'{label}: {df_right["NPV_final"].iloc[idx]:.2f}',
#                 alpha=0.7, width=0.4, align='center' if idx == mejor_idx else 'edge', color=color)

#     # Configurar título y etiquetas
#     axes[1,1].set_xlabel('Year\nd)', fontsize=14, fontweight='bold')
#     # axes[1,1].set_ylabel('Cash Flow', fontsize=14, fontweight='bold')
#     axes[1,1].legend(fontsize=12, title_fontsize='13', loc='best', frameon=True)

#     # Configurar etiquetas de los ejes
#     axes[1,1].set_xticklabels(axes[1,1].get_xticks(), fontsize=12, fontweight='normal')
#     axes[1,1].set_yticklabels(axes[1,1].get_yticks(), fontsize=12, fontweight='normal')

#     axes[1,1].grid(True)
    
    
#     plt.savefig("BC_&_PV40k_TF_SB.png", bbox_inches='tight')
#     plt.tight_layout()
#     plt.show()


# graficar(df_L2_BC, df_L2_PV40k_TF_SB)

######################################################################################################################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast

filePath = 'H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_BC.csv'
df_L2_BC = pd.read_csv(filePath, sep=',')

filePath = 'H:\\My drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\semifast\\L2_PV40k_TF_SB.csv'
df_L2_PV40k_TF_SB = pd.read_csv(filePath, sep=',')

def Add_Investment(df):
    # Convertir las columnas 'flujos_caja' y 'NPV' de cadenas a listas
    df['flujos_caja'] = df['flujos_caja'].apply(eval)
    df['NPV'] = df['NPV'].apply(eval)

    # Agregar el primer valor de flujos_caja al inicio de cada lista de NPV
    df['NPV'] = df.apply(lambda row: [row['flujos_caja'][0]] + row['NPV'], axis=1)
    return df

df_L2_BC = Add_Investment(df_L2_BC)
df_L2_BC['NPV_final'] = df_L2_BC['NPV'].apply(lambda x: x[-2] if len(x) >= 2 else None)
# Guardar el resultado si lo necesitas
df_L2_BC.to_csv('archivo_modificado.csv', index=False)
df_L2_PV40k_TF_SB = Add_Investment(df_L2_PV40k_TF_SB)
df_L2_PV40k_TF_SB['NPV_final'] = df_L2_PV40k_TF_SB['NPV'].apply(lambda x: x[-2] if len(x) >= 2 else None)


########################################################

def graficar(df_left, df_right):
    for df in [df_left, df_right]:
        df['vida_util'] = df['vida_util'].apply(lambda x: list(range(20)))  # Ahora es siempre de 0 a 19
        def safe_eval(val):
            if isinstance(val, str):
                return ast.literal_eval(val)
            return val

        df['NPV'] = df['NPV'].apply(safe_eval)
        df['NPV'] = df['NPV'].apply(lambda x: x[:-1])  # Excluir el valor de año 20
        def safe_eval(val):
            if isinstance(val, str):
                return ast.literal_eval(val)
            return val

        df['flujos_caja'] = df['flujos_caja'].apply(safe_eval)
        df['flujos_caja'] = df['flujos_caja'].apply(lambda x: x[:-1])  # Excluir último año

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    # --- LEFT PLOTS ---
    for _, row in df_left.iterrows():
        axes[0,0].plot(row['vida_util'], row['NPV'], label=f"DI {row['crecimiento_demanda']:.0%}, DR {row['tasa_descuento']:.0%}")

    axes[0,0].set_ylabel('VPN (USD)', fontsize=14, fontweight='bold')
    axes[0,0].set_xlabel('a)', fontsize=14, fontweight='bold')
    axes[0,0].legend()
    axes[0,0].tick_params(axis='both', labelsize=12)
    axes[0,0].grid()

    mejor_idx = df_left['NPV_final'].idxmax()
    peor_idx = df_left['NPV_final'].idxmin()

    for idx, color, label in zip([mejor_idx, peor_idx], ['green', 'red'], ['Mejor VPN', 'Peor VPN']):
        flujo = df_left['flujos_caja'].iloc[idx]
        axes[1,0].bar(range(len(flujo)), flujo,
                      label=f'{label}: {df_left["NPV_final"].iloc[idx]:.2f}',
                      alpha=0.7, width=0.4, align='center' if idx == mejor_idx else 'edge', color=color)

    axes[1,0].set_xlabel('Año\nc)', fontsize=14, fontweight='bold')
    axes[1,0].set_ylabel('Flujo de Caja (USD)', fontsize=14, fontweight='bold')
    axes[1,0].legend(fontsize=12, title_fontsize='13', loc='best', frameon=True)
    axes[1,0].tick_params(axis='both', labelsize=12)
    axes[1,0].grid(True)

    # --- RIGHT PLOTS ---
    for _, row in df_right.iterrows():
        axes[0,1].plot(row['vida_util'], row['NPV'], label=f"DI {row['crecimiento_demanda']:.0%}, DR {row['tasa_descuento']:.0%}")

    axes[0,1].set_xlabel('b)', fontsize=14, fontweight='bold')
    axes[0,1].legend()
    axes[0,1].tick_params(axis='both', labelsize=12)
    axes[0,1].grid()

    mejor_idx = df_right['NPV_final'].idxmax()
    peor_idx = df_right['NPV_final'].idxmin()

    for idx, color, label in zip([mejor_idx, peor_idx], ['green', 'red'], ['Mejor VPN', 'Peor VPN']):
        flujo = df_right['flujos_caja'].iloc[idx]
        axes[1,1].bar(range(len(flujo)), flujo,
                      label=f'{label}: {df_right["NPV_final"].iloc[idx]:.2f}',
                      alpha=0.7, width=0.4, align='center' if idx == mejor_idx else 'edge', color=color)

    axes[1,1].set_xlabel('Año\nd)', fontsize=14, fontweight='bold')
    axes[1,1].legend(fontsize=12, title_fontsize='13', loc='best', frameon=True)
    axes[1,1].tick_params(axis='both', labelsize=12)
    axes[1,1].grid(True)

    plt.savefig("BC_&_PV40k_TF_SB.png", bbox_inches='tight')
    plt.tight_layout()
    plt.show()

graficar(df_L2_BC, df_L2_PV40k_TF_SB)