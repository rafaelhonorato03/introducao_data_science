import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualization:
    def __init__(self):

        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
    
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()

G = GraphVisualization()
G.addEdge(10, 2)
G.addEdge(1, 3)
G.addEdge(1, 44)
G.addEdge(1, 5)
G.addEdge(5, 6)
G.addEdge(1, 7)
G.addEdge(1, 80)
G.visualize()


# Formando graficos com aparencia 3D
G = nx.grid_graph([3, 3])

for line in nx.generate_adjlist(G):
    print(line)

nx.write_edgelist(G, path='grid.edgelist', delimiter=':')

H = nx.read_edgelist(path='grid.edgelist', delimiter=':')

pos = nx.spring_layout(H, seed=200)
nx.draw(H, pos)
plt.show()

# Analise de redes sociais
n = 1000
m = 2
seed = 20532
G = nx.barabasi_albert_graph(n, m, seed=seed)

node_and_degree = G.degree()
(largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]

hub_ego = nx.ego_graph(G, largest_hub)

pos = nx.spring_layout(hub_ego, seed=seed)
nx.draw(hub_ego, pos, node_color='b', nose_size=50, with_labeels=False)

options = {'node_size': 310, 'node_color': 'r'}
nx.draw_networkx_nodes(hub_ego, pos, nodelist={largest_hub}, **options)
plt.show()