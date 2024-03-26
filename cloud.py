import cloudinary.api
import json

cloudinary.config(
  cloud_name = 'dmiaxw4rr', 
  api_key = '678414952824331', 
  api_secret = 'wt-aWFLd0n-CelO5kN8h1NCYFzY'
)

# The name of the folder you want to list resources from
folder_name = 'TigerSpot'

# Fetch the resources
resources = cloudinary.api.resources(
    type = 'upload',
    prefix = folder_name,  # List resources under this folder
    max_results = 500  # Adjust based on your needs, max is 500 per call
)

# Extracting URLs and saving them to a file
with open('url.txt', 'w') as f:
    for resource in resources.get('resources', []):
        f.write(resource['url'] + '\n')  # Write each URL to the file

print("URLs saved to url.txt")
