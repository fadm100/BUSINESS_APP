import pandas as pd

# Cargar el archivo
df = pd.read_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\buses_availability_5min.csv')

# Invertir ceros y unos, excluyendo la columna 'hora'
df.iloc[:, 1:] = 1 - df.iloc[:, 1:]

# Guardar el resultado
df.to_csv('H:\\My Drive\\Articulos tesis\\DESARROLLO\\Ob2\\Simulation_Files\\buses_availability_5min_inverted.csv', sep=",", index=False)
