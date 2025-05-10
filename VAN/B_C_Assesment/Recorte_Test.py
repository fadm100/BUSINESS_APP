import pandas as pd
import ast
import re

def limpiar_lista(texto):
    texto = texto.strip().replace('[', '').replace(']', '')
    elementos = re.split(r'\s+', texto.strip())

    # Eliminar comas y espacios extra en cada elemento
    elementos = [x.strip().replace(',', '') for x in elementos if x.strip() != '']

    try:
        lista = [int(x) for x in elementos]
    except ValueError:
        lista = [float(x) for x in elementos]
    return lista

def truncar_listas(row):
    vida_util = limpiar_lista(row['vida_util'])
    if max(vida_util) == 30:
        row['vida_util'] = str(vida_util[:20])
        row['flujos_caja'] = str(limpiar_lista(row['flujos_caja'])[:20])
        nuevos_npv = limpiar_lista(row['NPV'])[:20]
        row['NPV'] = str(nuevos_npv)
        row['NPV_final'] = nuevos_npv[-1]
    return row

if __name__ == '__main__':
    # Cargar tu archivo CSV
    df = pd.read_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\OUTCOMES\\15-11-2024\\todo\\L3_TF_SB.csv')
    df = df.apply(truncar_listas, axis=1)
    df.to_csv('resultado_acortado.csv', index=False)

