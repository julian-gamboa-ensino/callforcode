import os
import uuid
import json
import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError
import ibm_s3transfer.manager

def execute(filename, file_path, image_info):
    config_file_path = os.path.join('config', 'ibm_credentials.json')
    with open(config_file_path, 'r') as config:
        ibm_credentials = json.loads(config.read())
    
    cos = ibm_boto3.resource("s3",
        ibm_api_key_id=ibm_credentials['apikey'],
        ibm_service_instance_id=ibm_credentials['resource_instance_id'],
        ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
        config=Config(signature_version="oauth"),
        endpoint_url='https://s3.us-south.cloud-object-storage.appdomain.cloud'
    )
    
    img_bucket_name = 'call-for-code-2021-images'
    data_bucket_name = 'call-for-code-2021-data'
    
    img_filename = image_info['company'] + '_' + filename
    cos.Object(img_bucket_name, img_filename).upload_file(file_path)
    
    data_filename = image_info['company'] + '_' + filename.split('.')[0] + '.json'
    cos.Object(data_bucket_name, data_filename).put(Body=json.dumps(image_info))
    
    return True
