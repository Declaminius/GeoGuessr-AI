import csv
import os
# os.environ['USE_PYGEOS'] = '0'
import osmnx as ox
import pyrosm
import numpy as np
from config import states_dict, highway_filter, highway_filter_pyrosm

class StreetNetwork:

    def __init__(self, state, country, filepath = None):
        self.filepath = filepath
        self.state = state
        self.country = country
        self.savefile = f"networks/{self.country}/{self.state}.graphml"
        self.network = None
        self.saved_graph = False

    def load_network(self, file = None):
        if file is not None:
            self.network = ox.load_graphml(file)
        else:
            if self.saved_graph:
                self.network = ox.load_graphml(self.savefile)
            else:
                raise Exception("No savefile specified to load the network from")

    def plot_network(self):
        if self.network is not None:
            ox.plot_graph(self.network)
        else:
            raise Exception("Graph not yet generated")
    
    def generate_network(self, filter = None):
        if self.filepath is None:
            return self.generate_network_overpass(filter)
        else:
            return self.generate_network_osm()

    def generate_network_overpass(self, filter):
        try:
            location = {'state': self.state, 'country': self.country}
            self.network = ox.graph_from_place(location, network_type="drive", custom_filter = filter)
        except:
            location = {'city': self.state, 'country': self.country}
            self.network = ox.graph_from_place(location, network_type="drive", custom_filter = filter)
        self.save_network()         
        
    def generate_network_osm(self):
        self.network = ox.graph_from_xml(self.filepath)
        self.save_network() 

    def generate_network_pyrosm(self):
        osm = pyrosm.OSM(self.filepath)
        nodes, edges = osm.get_network(network_type = "driving", nodes = True)
        self.network = osm.to_graph(nodes, edges, graph_type="networkx", retain_all=True)
        self.save_network() 

    def save_network(self):
        if self.network is not None:
            ox.save_graphml(self.network, self.savefile)
            self.save_stats()
            self.saved_graph = True
        else:
            raise Exception("Network not yet generated.")

    def save_stats(self):
        savefile = f"networks/{self.country}/{self.state}.csv"
        try:
            stats = ox.basic_stats(self.network, clean_int_tol=15)
        except Exception as e:
            print(e)
            stats = {"n": len(self.network.nodes), "m": len(self.network.edges)}

        with open(savefile, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames= stats.keys())
            writer.writeheader()
            writer.writerow(stats)

# for state in states_dict["Austria"]:
#     print(state)
#     street_network = StreetNetwork(state = state, country = "Austria")
#     street_network.generate_network(filter = highway_filter)
#     street_network.plot_network()

# street_network = StreetNetwork(state = "new_south_wales", country = "Australia", filepath = f"OSM-Data/new_south_wales_filtered2.osm")
# street_network.generate_network_osm()
# print(len(street_network.network.nodes), len(street_network.network.edges))
# street_network.plot_network()

# street_network = StreetNetwork(state = "new_south_wales", country = "Australia", filepath = f"OSM-Data/new_south_wales_filtered.osm.pbf")
# street_network.generate_network_pyrosm()
# print(len(street_network.network.nodes), len(street_network.network.edges))
# street_network.plot_network()


for state in states_dict["Australia"]:
    print(state)
    if state == "new_south_wales":
        street_network = StreetNetwork(state = state, country = "Australia")
        street_network.generate_network_overpass(filter = highway_filter)
        print(len(street_network.network.nodes), len(street_network.network.edges))
        street_network.plot_network()
