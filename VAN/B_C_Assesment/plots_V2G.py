import pandas as pd
import matplotlib.pyplot as plt
import ast
import re
import numpy as np

archivo1 = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\24-04-2025\\3_4_5_USD_kw.csv'
archivo2 = 'H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\25-04-2025\\3_4_5_USD_kw.csv'

df1 = pd.read_csv(archivo1)
df2 = pd.read_csv(archivo2)
df = pd.concat([df1, df2], ignore_index=True)

# Arreglar listas mal formateadas
def corregir_lista_mal_formateada(x):
    x = x.strip('[]')
    x = re.sub(r'\s+', ',', x.strip())
    return ast.literal_eval(f"[{x}]")

df['vida_util'] = df['vida_util'].apply(corregir_lista_mal_formateada)
df['flujos_caja'] = df['flujos_caja'].apply(ast.literal_eval)
df['NPV'] = df['NPV'].apply(ast.literal_eval)
df['label'] = df.apply(lambda row: f"{row['capacity_kw']}kW | {row['USD_kW']}USD/kW", axis=1)

# --- Gráfico de flujos de caja con barras ---
plt.figure(figsize=(10, 5))
num_series = len(df)
bar_width = 0.8 / num_series  # Ajuste para evitar superposición
offsets = np.linspace(-0.4 + bar_width / 2, 0.4 - bar_width / 2, num_series)

for i, (_, row) in enumerate(df.iterrows()):
    x = np.array(row['vida_util']) + offsets[i]
    plt.bar(x, row['flujos_caja'], width=bar_width, label=row['label'])

plt.title('Flujos de caja vs Vida útil', fontsize=16, fontweight='bold')
plt.xlabel('Año', fontsize=14, fontweight='bold')
plt.ylabel('Flujos de caja (USD)', fontsize=14, fontweight='bold')
plt.grid(True, axis='y')
plt.legend()
plt.tight_layout()
plt.show()


# --- Gráfico 2: NPV ---
plt.figure(figsize=(8, 5))
for _, row in df.iterrows():
    x = row['vida_util']
    y = row['NPV']
    plt.plot(x, y, label=row['label'])
    
    # Imprimir el último valor de NPV al final de la línea
    plt.text(x[-2], y[-2], f"{y[-1]:.1f}", fontsize=12, fontweight='bold', va='top', ha='left')

plt.title('VPN vs Vida útil', fontsize=16, fontweight='bold')
plt.xlabel('Año', fontsize=14, fontweight='bold')
plt.ylabel('VPN (USD)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

