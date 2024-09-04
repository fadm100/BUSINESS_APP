import tabula
import pandas as pd

############## Calcula el porcentaje de incremento de vehículos ################
# Leer el DataFrame de costos de cargadores
filePath = 'evProjections.csv'  # Costos de un solo cargador, la tabla contiene varios tipos de cargadores divididos entre lentos, semirápidos y rapídos
df = pd.read_csv(filePath, sep=',')

# Calcular el porcentaje de incremento para cada columna
df['Taxis projection % Incremento'] = df['Taxis projection'].pct_change() * 100
df['Annual EV % Incremento'] = df['Annual EV'].pct_change() * 100

# Mostrar el resultado
print(df[['Year', 'Taxis projection % Incremento', 'Annual EV % Incremento']].round(2))
