from osmnx.utils_geo import sample_points
from osmnx import load_graphml
import os
import csv
import requests

class StreetViewImages:
  api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
  streetview_api = 'https://maps.googleapis.com/maps/api/streetview'
  metadata_api = 'https://maps.googleapis.com/maps/api/streetview/metadata'

  def __init__(self, state, country):
    self.state = state
    self.country = country
    self.imagepath = f"images/{country}/{state}"
    self.graph_file = f"networks/{country}/{state}.graphml"
    self.network = load_graphml(self.graph_file)
    with open (os.path.join(self.imagepath, "coordinates.csv"), "r") as file:
      last_line = file.readlines()[-1]
      self.current_id = int(last_line[0])
  
  def generate_points(self, n):
    return sample_points(self.network, n)
  
  def save_image(self, response):
    if response.status_code == 200:
      if not os.path.exists(self.imagepath):
        os.makedirs(self.imagepath)
      with open(os.path.join(self.imagepath, f'{self.current_id}.jpg'), "wb") as file:
        file.write(response.content)

  def save_coordinates(self, coordinates):  
      coordinates_filename = os.path.join(self.imagepath, 'coordinates.csv')
      coordinates["i"] = self.current_id
      fieldnames = ["i", "lat", "lng"]
      with open(coordinates_filename, "a", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)
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
      response = requests.get(self.streetview_api, params)
      self.current_id += 1
      self.save_image(response)
      self.save_coordinates(coordinates)

num_of_locations = 100
states_dict = {"Austria": ["Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg", "Vienna"],\
                "Australia": ["Australian Capital Territory", "Tasmania", "Northern Territory", "Western Australia", "South Australia", "Queensland", "Victoria", "New South Wales"],\
                "New Zealand": ["West Coast", "Marlborough", "Gisborne", "Nelson", "Tasman", "Southland", "Taranaki", "Hawke's Bay", "Northland", "Otago", "Manawatū-Whanganui", "Bay of Plenty", "Waikato", "Wellington", "Canterbury", "Auckland"]}

for state in states_dict["Austria"]:
  if state != "Vienna":
    streetview_images = StreetViewImages(state, "Austria")
    points = streetview_images.generate_points(num_of_locations)
    for location in points:
      streetview_images.request_image(location)
    print(streetview_images.current_id)

