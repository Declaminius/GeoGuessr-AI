import osmnx as ox
import csv

# ox.settings.timeout = 600
# ox.overpass_settings = "[out:json][timeout:{600}]"

class StreetNetwork:

    def __init__(self, state, country, filepath = None, savefile = None):
        self.filepath = filepath
        self.state = state
        self.country = country
        self.savefile = None

    def plot_network(self):
        if self.savefile is not None:
            G = ox.load_graphml(self.savefile)
            ox.plot_graph(G)
        else:
            raise Exception("Graph not yet generated")
    
    def generate_network(self, filter):
        if self.filepath is None:
            self.generate_network_overpass(filter)
        else:
            self.generate_network_osm()

    def generate_network_overpass(self, filter):
        if self.state == "Vienna":
            location = {'city': self.state, 'country': self.country}
        else:
            location = {'state': self.state, 'country': self.country}
        self.savefile = f"networks/{self.country}/{self.state}.graphml"

        G = ox.graph_from_place(location, network_type="drive", custom_filter = filter)
        # G = ox.project_graph(G)

        self.save_stats(G)
        ox.save_graphml(G, self.savefile)

    def generate_network_osm(self):
        self.savefile = f"networks/{self.country}/{self.state}.graphml"

        G = ox.graph_from_xml(self.filepath)
        # G = ox.project_graph(G)
        self.save_stats(G)
        ox.save_graphml(G, self.savefile)

    def save_stats(self, graph):
        savefile = f"networks/{self.country}/{self.state}.csv"
        try:
            stats = ox.basic_stats(graph, clean_int_tol=15)
        except Exception as e:
            print(e)
            stats = {"n": len(graph.nodes), "m": len(graph.edges)}

        with open(savefile, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames= stats.keys())
            writer.writeheader()
            writer.writerow(stats)


states_dict = {"Austria": ["Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg", "Vienna"],\
                "Australia": ["Australian Capital Territory", "Tasmania", "Northern Territory", "Western Australia", "South Australia", "Queensland", "Victoria", "New South Wales"],\
                "New Zealand": ["West Coast", "Marlborough", "Gisborne", "Nelson", "Tasman", "Southland", "Taranaki", "Hawke's Bay", "Northland", "Otago", "Manawatū-Whanganui", "Bay of Plenty", "Waikato", "Wellington", "Canterbury", "Auckland"]}
cf = '["highway"~"motorway|trunk|primary|secondary"]'

for state in states_dict["Austria"]:
    print(state)
    street_network = StreetNetwork(state = state, country = "Austria")
    street_network.generate_network(filter = cf)
    # street_network.plot_network()

