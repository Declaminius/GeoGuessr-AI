import osmnx as ox
import csv

# ox.settings.timeout = 600
# ox.overpass_settings = "[out:json][timeout:{600}]"

def plot_network(state, country):
    filepath = f"networks/{country}/{state}.graphml"
    G = ox.load_graphml(filepath)
    ox.plot_graph(G)

def generate_network(state, country, filter):
    if state == "Vienna":
        location = {'city': state, 'country': country}
    else:
        location = {'state': state, 'country': country}
    filepath = f"networks/{country}/{state}.graphml"

    G = ox.graph_from_place(location, network_type="drive", custom_filter = filter)
    G = ox.project_graph(G)

    save_stats(G, state, country)
    ox.save_graphml(G, filepath)

def save_stats(graph, state, country):
    savefile = f"networks/{country}/{state}.csv"
    stats = ox.basic_stats(graph, clean_int_tol=15)

    with open(savefile, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames= stats.keys())
        writer.writeheader()
        writer.writerow(stats)


states_dict = {"Austria": ["Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg"],\
                "Australia": ["Australian Capital Territory", "Tasmania", "Northern Territory", "Western Australia", "South Australia", "Queensland", "Victoria", "New South Wales"],\
                "New Zealand": ["West Coast", "Marlborough", "Gisborne", "Nelson", "Tasman", "Southland", "Taranaki", "Hawke's Bay", "Northland", "Otago", "Manawatū-Whanganui", "Bay of Plenty", "Waikato", "Wellington", "Canterbury", "Auckland"]}
cf = '["highway"~"motorway|trunk|primary|secondary"]'

for state in states_dict["New Zealand"]:
    try:
        generate_network(state, "New Zealand", cf)
        plot_network(state, "New Zealand")
    except ox._errors.EmptyOverpassResponse:
        print(f"No data for {state}")

# generate_network("Tasmania", "Australia", cf)
# plot_network("Tasmania", "Australia")

# graph = ox.graph_from_xml('OSM-Data/northern_territory.osm')
