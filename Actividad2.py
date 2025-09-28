import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Base de conocimientos - Diccionario
datos = {
    'Source': ['Terminal', 'Terminal', 'Unicentro', 'Alkosto', 'Alkosto', 'Primavera', 'Parque Fundadores'],
    'Target': ['Unicentro', 'Alkosto', 'Primavera', 'Primavera', 'Parque Fundadores', 'Parque Central', 'Parque Central'],
    'Cost':   [
        5000,   # Terminal -> Unicentro
        50000,  # Terminal -> Alkosto 
        5000,   # Unicentro -> Primavera
        5000,
        3000,
        1000,   # Primavera -> Parque Central
        5000
    ]
}

df = pd.DataFrame(datos)
G = nx.DiGraph()

for index, row in df.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Cost'])

# Motor de inferencia
def the_best_Road(graph, start_node, end_node):
    try:
        costo = nx.dijkstra_path_length(graph, start_node, end_node, weight='weight')
        ruta = nx.dijkstra_path(graph, start_node, end_node, weight='weight')
        return ruta, costo
    except nx.NetworkXNoPath:
        return None, float('inf')

# Indicamos nuestro punto de origen y detino
inicio = 'Alkosto'
fin = 'Parque Central'
ruta_optima, costo_total = the_best_Road(G, inicio, fin)

costo_formateado = f"${costo_total:,.0f}"

print(f"La ruta óptima desde {inicio} hasta {fin} es: {', '.join(ruta_optima)}")
print(f"El costo total (en COP) es de: {costo_formateado}")

# Se crea el grafo con networkx
if ruta_optima:

    path_edges = list(zip(ruta_optima, ruta_optima[1:]))

    
    pos = nx.shell_layout(G)

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1200)
    # Resaltar la ruta
    nx.draw_networkx_nodes(G, pos, nodelist=ruta_optima, node_color='red', node_size=1200)

    # Dibujar aristas (rutas)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', width=1, arrows=True)
    # Resaltar las aristas de la ruta
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, arrows=True)

    # Ajustamos la posición de las etiquetas para que no se superpongan
    nx.draw_networkx_labels(G, pos, font_weight='bold', font_size=10)

    # Añadir etiquetas de los costos
    edge_labels = nx.get_edge_attributes(G, 'weight')
    display_labels = {k: f"{v:,.0f}" for k, v in edge_labels.items()}

    nx.draw_networkx_edge_labels(G, pos, edge_labels=display_labels, font_color='blue', font_size=9)

    # Configuración final y visualización
    plt.title(f"RUTA DESVÍO: {inicio} a {fin} | Total: COP {costo_formateado}", fontsize=14)
    plt.axis('off')
    plt.show()