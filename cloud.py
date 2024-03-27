import cloudinary.api
import json

cloudinary.config(
  cloud_name = 'dmiaxw4rr', 
  api_key = '678414952824331', 
  api_secret = 'wt-aWFLd0n-CelO5kN8h1NCYFzY'
)

folder_name = 'TigerSpot'

resources = cloudinary.api.resources(
    type = 'upload',
    prefix = folder_name, 
    max_results = 500,
    context = True
)

with open('picturedata.txt', 'w') as f:
    for resource in resources.get('resources', []):
        f.write(resource['url'] + '\n')

        custom_metadata = resource.get('context', {}).get('custom', {})
        latitude = float(custom_metadata.get('Latitude'))
        longitude = float(custom_metadata.get('Longitude'))
        
        f.write(f"{latitude}\n{longitude}\n")
        #print(latitude + longitude)

#print("TigerSpot's image data saved to picturedata.txt")
