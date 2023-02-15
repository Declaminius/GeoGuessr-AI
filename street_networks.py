import osmnx as ox
import csv

states = ["Vienna", "Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg"]

for state in states:
    location = f"{state}, Austria"
    directory = f"networks/Austria/{location}-cf"

    cf = '["highway"~"motorway|primary|secondary"]'

    G = ox.graph_from_place(location, network_type="drive", custom_filter=cf)
    G_proj = ox.project_graph(G)
    stats = ox.basic_stats(G_proj, clean_int_tol=15)
    print(stats)

    with open(directory + ".csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames= stats.keys())
        writer.writeheader()
        writer.writerow(stats)


    filepath = directory + ".graphml"
    ox.save_graphml(G, filepath)

    fig, ax = ox.plot_graph(G)

def plot_networks():
    for state in states:
        filepath = "networks/gaming.graphml"
        G = ox.load_graphml(filepath)
