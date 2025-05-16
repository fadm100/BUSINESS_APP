import matplotlib.pyplot as plt

# Datos de los años 2009 a 2025
years = list(range(2009, 2026))

# Documentos para cada año
documents_a = [1, 4, 1, 2, 4, 6, 5, 9, 5, 12, 11, 8, 19, 21, 9, None, None]
documents_b = [1, 4, 1, 2, 4, 6, 5, 9, 5, 12, 11, 8, 19, 22, 26, 32, 16]

# Graficar ambas curvas completas
plt.figure(figsize=(12, 6))
plt.plot(years, documents_a, marker='o', linestyle='-', color='tab:blue', label='Búsqueda realizada en el 2023')
plt.plot(years, documents_b, marker='o', linestyle='--', color='tab:orange', label='Búsqueda realizada en el 2025')

plt.xlabel("Año", fontsize=16)
plt.ylabel("Documentos", fontsize=16)
# plt.title("Comparación de documentos por año", fontsize=18)
plt.legend(fontsize=14)
plt.grid(True)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.tight_layout()
plt.show()
