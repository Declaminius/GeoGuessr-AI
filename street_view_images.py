import osmnx as ox
import os

api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

site_api='https://maps.googleapis.com/maps/api/streetview'
site_metadata='https://maps.googleapis.com/maps/api/streetview/metadata'

states_dict = {"Austria": ["Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg"],\
                "Australia": ["Australian Capital Territory", "Tasmania", "Northern Territory", "Western Australia", "South Australia", "Queensland", "Victoria", "New South Wales"]}

def request_images(points, imagepath):
  for (i,loc) in enumerate(points):
    coords = str(loc.y) + "," + str(loc.x)
    print(coords)

    params = {
            'size': '640x640', # max 640x640 pixels
            'location': coords,
            'return_error_code': 'true',
            'key': api_key
          }
    response = requests.get(site_api, params)
    if response.status_code == 200:
      with open(os.path.join(imagepath, f'{state},{country}_{i}.jpg'), "wb") as file:
        file.write(response.content)
      
      with open(os.path.join(imagepath, 'coords.csv', "wb") as file:
        

    print(response.status_code)

for country in states_dict.keys():
  for state in states_dict[country]:
    filepath = f"networks/{country}/{state}.graphml"
    imagepath = f"images/{country}/{state}"

    G = ox.load_graphml(filepath)
    points = ox.utils_geo.sample_points(G, 5)
    request_images(points, imagepath)


# https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key=YOUR_API_KEY&signature=YOUR_SIGNATURE

# metadata_links = [site_metadata + '?' + urlencode(p) for p in params]
# metadata = [requests.get(url, stream=True).json() for url in metadata_links]

# metadata_response = requests.get(site_metadata, params)
# print(metadata_response)
# response = requests.get(site_api, params)

# with open(os.path.join(download_folder, f'street_view.jpg'), "wb") as file:
#   file.write(response.content)

# Create a results object
# results = Results(params)

# # Preview results
# results.preview()

# # Download images to directory 'downloads'
# results.download_links('Machine Learning Algorithms/Projekt/images')

# # Save links
# results.save_links('links.txt')

# # Save metadata
# results.save_metadata('metadata.json')