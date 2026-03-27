import networkx as nx
import matplotlib.pyplot as plt
import random


# ---------------- CREATE COMPLETE GRAPH ----------------
def create_complete_graph(n):
    G = nx.Graph()

    for i in range(n):
        for j in range(i + 1, n):
            weight = random.randint(1, 10)
            G.add_edge(i, j, weight=weight)

    return G


# ---------------- DRAW GRAPHS ----------------
def draw_graphs(G):

    # 🔷 MST using Kruskal
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

    # 🔷 Circular layout (same for both)
    pos = nx.circular_layout(G)

    # ---------------- ORIGINAL GRAPH ----------------
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Complete Graph (9 Nodes)")
    plt.savefig("complete_graph.png")
    plt.show()

    # ---------------- MST GRAPH ----------------
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=700)

    nx.draw_networkx_edges(
        G, pos,
        edgelist=mst.edges(),
        width=4
    )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Minimum Spanning Tree (MST)")
    plt.savefig("mst_graph.png")
    plt.show()

    # ---------------- PRINT MST ----------------
    print("\nMST Edges:")
    total_cost = 0

    for u, v, d in mst.edges(data=True):
        print(f"{u} - {v} : {d['weight']}")
        total_cost += d['weight']

    print("\nTotal MST Cost:", total_cost)


# ---------------- RUN ----------------
if __name__ == "__main__":

    n = 9

    G = create_complete_graph(n)

    print("Nodes:", len(G.nodes()))
    print("Edges:", len(G.edges()))  # should be 36

    draw_graphs(G)
