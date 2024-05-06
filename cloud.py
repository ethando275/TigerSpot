#-----------------------------------------------------------------------
# cloud.py
#-----------------------------------------------------------------------

import cloudinary.api

#-----------------------------------------------------------------------

# extracts the url, latitude, longitude, and place metadata from
# each image in the cloudinary folder
def image_data(resource):
    url = resource['url']
    custom_metadata = resource.get('context', {}).get('custom', {})
    latitude = float(custom_metadata.get('Latitude'))
    longitude = float(custom_metadata.get('Longitude'))
    place = custom_metadata.get('Place')
    return url, latitude, longitude, place

#-----------------------------------------------------------------------

def main():

    # configures and connects to cloudinary account
    cloudinary.config(
    cloud_name = 'dmiaxw4rr', 
    api_key = '678414952824331', 
    api_secret = 'wt-aWFLd0n-CelO5kN8h1NCYFzY'
    )

    # name of folder to extract resources from
    folder_name = 'TigerSpot/Checked'

    # extracts all resources from folder
    resources = cloudinary.api.resources(
    type = 'upload',
    prefix = folder_name,  
    max_results = 500, 
    context = True
    )
    
    # extracts and writes all image data to picturedata.txt
    with open('picturedata.txt', 'w') as f:
      for resource in resources.get('resources', []):
        url, latitude, longitude, place = image_data(resource)
        f.write(f"{place}\n")
        f.write(f"{latitude}, {longitude}\n")
        f.write(url + '\n\n')

    print("TigerSpot's image data saved to picturedata.txt")

#-----------------------------------------------------------------------

if __name__=="__main__":
  main()

