import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Crear un mapa detallado de Colombia
fig, ax = plt.subplots(figsize=(12, 12))
m = Basemap(projection='merc', llcrnrlat=-4, urcrnrlat=14, llcrnrlon=-82, urcrnrlon=-66, resolution='i')

m.drawmapboundary(fill_color='#92d6ec')
m.fillcontinents(color='#f2fcef', lake_color='#41493f')
m.drawcoastlines()
m.drawcountries(linewidth=2, color='black')
m.drawstates(linewidth=1, linestyle = 'dotted', color='grey')

# Agregar ciudades con tamaños de círculo proporcionales
ciudades = {
    'Bogotá - 49%': (-74.0721, 4.7110, 49),     # Tamaño más grande
    'Medellín - 27%': (-75.5636, 6.2518, 27),    # Tamaño intermedio
    'Cali - 5.7%': (-76.5225, 3.4516, 6),         # Tamaño más pequeño
    'Pasto - 0.1%': (-77.2811, 1.21361, 0.1)         # Tamaño más pequeño
}

for ciudad, (lon, lat, size) in ciudades.items():
    x, y = m(lon, lat)
    plt.plot(x, y, 'ro', markersize=size)  # Tamaño del círculo ajustado
    plt.text(x, y, ciudad, fontsize=12, ha='left')

plt.savefig("VE_Colombian_map.png", bbox_inches='tight')

plt.show()
