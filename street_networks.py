import osmnx as ox
import csv

def plot_network(state, country):
    filepath = f"networks/{country}/{state}.graphml"
    G = ox.load_graphml(filepath)
    ox.plot_graph(G)

def generate_network(state, country, filter):
    location = {'state': state, 'country': country}
    filepath = f"networks/{country}/{state}.graphml"

    G = ox.graph_from_place(location, network_type="drive", custom_filter = filter)

    save_stats(ox.project_graph(G), state, country)
    ox.save_graphml(G, filepath)

def save_stats(graph, state, country):
    savefile = f"networks/{country}/{state}.csv"
    stats = ox.basic_stats(graph, clean_int_tol=15)

    with open(savefile, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames= stats.keys())
        writer.writeheader()
        writer.writerow(stats)


states_dict = {"Austria": ["Vienna", "Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg"],\
                "Australia": ["Queensland", "New South Wales", "Australian Capital Territory", "Victoria", "Tasmania", "South Australia", "Northern Territory", "Western Australia"]}
cf = '["highway"~"motorway|primary"]'

# for country in states_dict.keys():
#     for state in states_dict[country]:
#         generate_network(state, country, cf)
#         plot_network(state, country)

# generate_network("Tasmania", "Australia", cf)
# plot_network("Tasmania", "Australia")

graph = ox.graph_from_xml('OSM-Data\northern_territory.osm.pbf')
