import cloudinary.api
import json

def convert_decimalcoords(dms):

  degrees, minutes, seconds = dms.split(', ')
  degrees = convert_fraction(degrees)
  minutes = convert_fraction(minutes)
  seconds = convert_fraction(seconds)
  decimal_coords = degrees + (minutes / 60) + (seconds / 3600)
  return decimal_coords

def convert_fraction(input):

  input_num, input_denom = input.split('/')
  input = float(input_num) / float(input_denom)
  return input

def image_data(resource):

  url = resource['url']
  # public_id = resource['public_id']

  # resource_details = cloudinary.api.resource(public_id, exif=True)
  # embedded_data = resource_details.get('exif', {})
  # latitude_ref = embedded_data.get('GPSLatitudeRef')
  # latitude = convert_decimalcoords(embedded_data.get('GPSLatitude'))
  # if (latitude_ref == 'S'):
  #   latitude = -latitude

  # longitude_ref = embedded_data.get('GPSLongitudeRef')
  # longitude = convert_decimalcoords(embedded_data.get('GPSLongitude'))
  # if (longitude_ref == 'W'):
  #   longitude = -longitude

  # return url, latitude, longitude

  custom_metadata = resource.get('context', {}).get('custom', {})
  latitude = float(custom_metadata.get('Latitude'))
  longitude = float(custom_metadata.get('Longitude'))
  return url, latitude, longitude

  #for resource in resources.get('resources', []):
    
    
    #f.write(f"{latitude}\n{longitude}\n")


  # with open('picturedata.txt', 'w') as f:
      
  # print("TigerSpot's image data saved to picturedata.txt")
