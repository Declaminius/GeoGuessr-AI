import os
os.environ['USE_PYGEOS'] = '0'
from osmnx.utils_geo import sample_points
from osmnx import load_graphml
from config import states_dict
import csv
import requests
import warnings
import pandas as pd
import numpy as np

class StreetViewImagesForState:
  api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
  streetview_api = 'https://maps.googleapis.com/maps/api/streetview'
  metadata_api = 'https://maps.googleapis.com/maps/api/streetview/metadata'


  def __init__(self, state, country):
    self.state = state
    self.country = country
    self.imagepath = f"images/{country}/{state}"
    self.graph_file = f"street_networks/{country}/{state}.graphml"
    self.network = load_graphml(self.graph_file)
    self.csv_fieldnames = ["i", "lat", "lng"]
    self.init_coordinates_csv()
  
  def init_coordinates_csv(self):
    filepath = os.path.join(self.imagepath, "coordinates.csv")
    if not os.path.isfile(filepath):
      if not os.path.exists(self.imagepath):
        os.makedirs(self.imagepath)
      with open (filepath, "w") as file:
        writer = csv.DictWriter(file, fieldnames = self.csv_fieldnames)
        writer.writeheader() 
      self.current_id = 0
    else:
      with open (filepath, "r") as file:
        last_line = file.readlines()[-1].split(",")
        self.current_id = int(last_line[0]) + 1
  
  def generate_points(self, n):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      return sample_points(self.network, n)
  
  def save_image(self, response):
    if response.status_code == 200:
      if not os.path.exists(self.imagepath):
        os.makedirs(self.imagepath)
      with open(os.path.join(self.imagepath, f'{self.current_id}.jpg'), "wb") as file:
        file.write(response.content)
        self.current_id += 1
    else:
      print(response.json())
      print(f"ERROR in {self.state} at {self.current_id}")

  def save_coordinates(self, coordinates):  
      coordinates_filename = os.path.join(self.imagepath, 'coordinates.csv')
      coordinates["i"] = self.current_id
      with open(coordinates_filename, "a", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames = self.csv_fieldnames)
        if not os.path.isfile(coordinates_filename):
          writer.writeheader() 
        writer.writerow(coordinates)

  def request_image(self, location):
    location = f"{location.y},{location.x}"
    params = {
            'size': '640x640', # max 640x640 pixels
            'location': location,
            'source': 'outdoor',
            'radius': 100,
            'return_error_code': 'true',
            'key': self.api_key,
          }

    # Check first, if an image is available at the given location (metadata-API calls are free)
    metadata = requests.get(self.metadata_api, params).json()

    # If an image is available, save it and its coordinates in the respective folder
    if metadata['status'] == 'OK':
      coordinates = metadata['location']
      image = requests.get(self.streetview_api, params)
      response = (coordinates, image)
      return response
    else:
      return None

def generate_images(country, number_of_total_locations, proportional_to_network_size = True):
  # Make number of locations roughly proportional to the size of the street networks in the respective states
  num_of_images_per_state = {}
  total_number_of_edges = 0
  edges_dict = {}
  for state in states_dict[country]:
    with open(f"street_networks/{country}/{state}.csv", "r") as file:
      if proportional_to_network_size:
        edges_dict[state] = np.sqrt(int(file.readlines()[-1].split(",")[1]))
      else:
        edges_dict[state] = 1
      total_number_of_edges += edges_dict[state]

  # Request images for each state
  for state in states_dict[country]:
    number_of_locations_state = int(number_of_total_locations*edges_dict[state]/total_number_of_edges)
    streetview_images = StreetViewImagesForState(state, country)
    points = streetview_images.generate_points(number_of_locations_state)
    num_images_before = streetview_images.current_id
    for location in points:
      response = streetview_images.request_image(location)
      if response:
        streetview_images.save_coordinates(response[0])
        streetview_images.save_image(response[1])
    num_images_after = streetview_images.current_id
    num_of_images_per_state[state] = num_images_after
    print(f"{num_images_after - num_images_before} images of {number_of_locations_state} locations found in {state}. In total now {num_images_after} images in {state}.")
  print(num_of_images_per_state)
  total_num_of_images = sum(num_of_images_per_state.values())
  print(f"Total number of images: {total_num_of_images}")


def remove_duplicates(country):
  number_of_removed_images = 0
  for state in states_dict[country]:
    df = pd.read_csv(f"images/{country}/{state}/coordinates.csv")
    duplicates = df.duplicated(subset = ["lat", "lng"])
    duplicated_rows = df[duplicates]
    for index in duplicated_rows["i"]:
      filepath = f"images/{country}/{state}/{index}.jpg"
      if os.path.isfile(filepath):
        os.remove(filepath)
        number_of_removed_images += 1
  print(f"{number_of_removed_images} images removed in {country}.")

if __name__ == '__main__':
  generate_images("New Zealand", 2000, True)