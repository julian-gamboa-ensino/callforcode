from coordinates.converter import convert_degrees_to_decimal
from google.cloud import vision
import piexif
import os, io

def execute(filename, img_file_path, company):
  
    try:
        exif_dict = piexif.load(img_file_path)
        
        # Extract thumbnail and save it, if exists
        
        thumbnail = exif_dict.pop('thumbnail')
        """
        if thumbnail is not None:
            with open('thumbnail.jpg', 'wb') as f:
                f.write(thumbnail)
        """
        # Iterate through all the other ifd names and print them
        #print(f'Metadata for {image_name}:')
        for ifd in exif_dict:
            #print(f'{ifd}:')
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                tag_value = exif_dict[ifd][tag]
                #print(tag_name, ' => ', type(tag_value))
                if 'GPSLongitude' in tag_name:
                    longitude = tag_value                
                elif 'GPSLatitude' in tag_name:
                    latitude = tag_value
                
                if 'GPSLongitudeRef' in tag_name:
                    longitude_ref = str(tag_value).split("'")[1]
                elif 'GPSLatitudeRef' in tag_name:
                    latitude_ref = str(tag_value).split("'")[1]
                    
        lat_degrees = latitude[0][0] / latitude[0][1]
        lat_minutes = latitude[1][0] / latitude[1][1]
        lat_seconds = latitude[2][0] / latitude[2][1]
        
        lon_degrees = longitude[0][0] / longitude[0][1]
        lon_minutes = longitude[1][0] / longitude[1][1]
        lon_seconds = longitude[2][0] / longitude[2][1]
        
        latitude = convert_degrees_to_decimal(lat_degrees, lat_minutes, lat_seconds)
        latitude = latitude if latitude_ref == 'N' else latitude * (-1)
        
        longitude = convert_degrees_to_decimal(lon_degrees, lon_minutes, lon_seconds)
        longitude = longitude if longitude_ref == 'E' else longitude * (-1)
    
    except:
        latitude = None
        longitude = None
    
    try:      
        # Instantiates a client
        config_file_path = os.path.join('config', 'vision_credentials.json')
        client = vision.ImageAnnotatorClient.from_service_account_json(
            config_file_path)

        # Loads the image into memory
        with io.open(img_file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        #print('Labels:')
        label_list = []
        for label in labels:
            if label.score > 0.7:
                if ('water' in label.description.lower()) or ('waste' in label.description.lower()) \
                    or ('bottle' in label.description.lower()) or ('plastic' in label.description.lower()) \
                        or ('pollution' in label.description.lower()):
                    
                    label_list.append(label.description)
    except:
        label_list = [] 
                   
    return {
        'latitude': latitude,
        'longitude': longitude,
        'labels': label_list,
        'filename': filename,
        'company': company
    }