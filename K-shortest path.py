import networkx as nx
import matplotlib.pyplot as plt


# ---------------- CREATE GRAPH ----------------
def create_graph():
    G = nx.Graph()

    edges = [
        (0,1,1),(0,2,1),(0,3,1),
        (1,4,2),(2,5,2),(3,6,2),
        (4,7,2),(5,8,2),(6,9,2),
        (7,10,1),(8,11,1),(9,12,1),
        (10,13,1),(11,13,1),(12,13,1),
        (4,5,3),(5,6,3),
        (7,8,3),(8,9,3),
        (1,2,2),(2,3,2)
    ]

    G.add_weighted_edges_from(edges)
    return G


# ---------------- MAIN FUNCTION ----------------
def k_link_disjoint_paths(G, source, target, k):

    working_graph = G.copy()
    results = []

    # Color names (for TXT mapping)
    color_names = [
        "RED", "BLUE", "GREEN", "ORANGE", "PURPLE",
        "BROWN", "PINK", "GRAY", "OLIVE", "CYAN"
    ]

    # ---------------- TXT FILE ----------------
    with open("k_link_disjoint_output.txt", "w") as file:

        file.write("K LINK-DISJOINT PATHS (WITH COLOR MAPPING)\n")
        file.write("============================================\n\n")
        file.write(f"Source: {source} | Target: {target}\n")
        file.write(f"K = {k}\n\n")

        for i in range(k):

            try:
                # 🔷 Find shortest path
                path = nx.shortest_path(
                    working_graph, source, target, weight='weight'
                )

                cost = sum(
                    working_graph[u][v]['weight']
                    for u, v in zip(path[:-1], path[1:])
                )

            except nx.NetworkXNoPath:
                file.write("\nNo more link-disjoint paths available.\n")
                break

            results.append((path, cost))

            color = color_names[i % len(color_names)]

            # 🔷 Write to TXT
            file.write(f"\n🔷 PATH {i+1} (Color: {color})\n")
            file.write("----------------------------------\n")
            file.write(f"Nodes: {path}\n")
            file.write(f"Cost: {cost}\n")

            file.write("Edges Used:\n")
            used_edges = list(zip(path[:-1], path[1:]))

            for u, v in used_edges:
                w = working_graph[u][v]['weight']
                file.write(f"  {u} -- {v} (weight {w})\n")

            file.write("Edges Removed (Link-Disjoint):\n")
            for u, v in used_edges:
                file.write(f"  Removing {u} -- {v}\n")
                working_graph.remove_edge(u, v)

            file.write("----------------------------------\n")

    print("TXT file generated!")

    return results


# ---------------- GRAPH VISUALIZATION ----------------
def draw_graph(G, results):

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10,7))

    # base graph
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=700)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # colors for paths
    colors = plt.cm.tab10.colors

    for i, (path, cost) in enumerate(results):
        edges = list(zip(path[:-1], path[1:]))

        nx.draw_networkx_edges(
            G, pos,
            edgelist=edges,
            width=4,
            edge_color=[colors[i % len(colors)]]
        )

    plt.title("K Link-Disjoint Paths (Different Colors)")

    plt.savefig("link_disjoint_paths.png")

    plt.show()
# ---------------- RUN ----------------
if __name__ == "__main__":

    G = create_graph()

    k = 5   # 🔥 CHANGE THIS VALUE (10, 50, 100...)

    results = k_link_disjoint_paths(G, 0, 13, k)

    print("\nPaths Found:")
    for i, (path, cost) in enumerate(results):
        print(f"{i+1}: Cost={cost}, Path={path}")

    draw_graph(G, results)
