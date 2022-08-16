import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id = 'AKIAQVWCUMEC62WL74BI',
                        aws_secret_access_key = 'cQTktg2lWsdXcjopXoiu4DkbHbyrtqFADPLUnVRj')

imagePath = "./example1/e10.jpg"
imgNametobeStore = "example1.jpg"

def upload_my_file(bucket, folder, file_to_upload, file_name):

    key = folder+"/"+file_name
    try:
        response = s3_client.upload_file(file_to_upload, bucket, key, ExtraArgs={'ACL':'public-read'})
        file_url = '%s/%s/%s' % (s3_client.meta.endpoint_url, bucket, key)
        
    except ClientError as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False
    return file_url


#Upload file
upload_my_file("videotofotos", "groupImageForAttendance", imagePath, imgNametobeStore )