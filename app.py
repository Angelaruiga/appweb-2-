import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Cargar los datos
data = pd.read_csv('data_interacciones.csv')

# Función para ajustar las etiquetas de los nodos, poner en mayúsculas y reemplazar información tras "_"
def adjust_labels_column(column):
    adjusted_column = column.apply(lambda x: x.split('_')[0].replace(';', '\n').upper() if ';' in x else x.split('_')[0].upper())
    return adjusted_column

# Ajustar las etiquetas de las columnas 'Grupo1' y 'Grupo2'
data['Grupo1'] = adjust_labels_column(data['Grupo1'])
data['Grupo2'] = adjust_labels_column(data['Grupo2'])

# Calcular el tamaño de los nodos basado en el total de interacciones
node_interactions = data.groupby('Grupo1')['Suma de Interacciones'].sum().to_dict()
node_interactions.update(data.groupby('Grupo2')['Suma de Interacciones'].sum().to_dict())

# Crear un widget de lista desplegable para los grupos
unique_groups = list(set(data['Grupo1']).union(set(data['Grupo2'])))
group_selector = st.selectbox('Selecciona un Grupo:', ['All'] + unique_groups)

# Filtrar los datos según el grupo seleccionado
if group_selector != 'All':
    filtered_data = data[(data['Grupo1'] == group_selector) | (data['Grupo2'] == group_selector)]
else:
    filtered_data = data

# Crear el gráfico de red dirigido
G = nx.DiGraph()
for index, row in filtered_data.iterrows():
    G.add_edge(row['Grupo1'], row['Grupo2'], weight=row['Suma de Interacciones'])

pos = nx.spring_layout(G, k=0.5)
labels = {node: node for node in G.nodes()}

# Calcular el tamaño de los nodos basado en el total de interacciones
node_size = [node_interactions.get(node, 1) * 500 for node in G.nodes()]  # Aumentado el tamaño de los nodos

# Configurar el Streamlit
st.title("Publicaciones 2023 en colaboración")

# Crear gráfico con matplotlib y mostrarlo en Streamlit
fig, ax = plt.subplots(figsize=(35, 20))  # Aumentado el tamaño del gráfico
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='orange', alpha=0.9, ax=ax)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.5, edge_color='grey', ax=ax, arrows=True)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=15, font_family="sans-serif", ax=ax)  # Aumentada la fuente de las etiquetas
ax.set_axis_off()
st.pyplot(fig)
