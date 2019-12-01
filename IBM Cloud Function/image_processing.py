
import ibm_boto3
from ibm_botocore.client import Config
import uuid
from time import time
from PIL import Image, ImageFilter


cos_credentials = {
  "apikey": "api_key",
  "endpoints": "end_point",
  "iam_apikey_description": "Auto-generated for key ",
  "iam_apikey_name": "name",
  "iam_role_crn": "xxxxx",
  "iam_serviceid_crn": "xxx",
  "resource_instance_id": "xxxx"
}



s3_client = ibm_boto3.client('s3', ibm_api_key_id=cos_credentials['apikey'])
FILE_NAME_INDEX = 2

TMP = "/tmp/"





def flip(image, file_name):
    path_list = []
    path = TMP + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)
    path_list.append(path)

    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)
    path_list.append(path)

    return path_list


def rotate(image, file_name):
    path_list = []
    path = TMP + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    img.save(path)
    path_list.append(path)

    path = TMP + "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    img.save(path)
    path_list.append(path)

    path = TMP + "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    img.save(path)
    path_list.append(path)

    return path_list


def filter(image, file_name):
    path_list = []
    path = TMP + "blur-" + file_name
    img = image.filter(ImageFilter.BLUR)
    img.save(path)
    path_list.append(path)

    path = TMP + "contour-" + file_name
    img = image.filter(ImageFilter.CONTOUR)
    img.save(path)
    path_list.append(path)

    path = TMP + "sharpen-" + file_name
    img = image.filter(ImageFilter.SHARPEN)
    img.save(path)
    path_list.append(path)

    return path_list


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    img = image.convert('L')
    img.save(path)
    return [path]


def resize(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((128, 128))
    image.save(path)
    return [path]


def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += ops.flip(image, file_name)
        path_list += ops.rotate(image, file_name)
        path_list += ops.filter(image, file_name)
        path_list += ops.gray_scale(image, file_name)
        path_list += ops.resize(image, file_name)

    latency = time() - start
  
    return latency, path_list


def main(event):
    print("inside main")
    input_bucket = event['input_bucket']
    object_key = event['object_key']
    output_bucket = event['output_bucket']
    

    download_path = '/tmp/{}{}'.format(uuid.uuid4(), object_key)
    
    
    try:
        s3_client.download_file(input_bucket, object_key, download_path)
    except Exception as e:
        print(Exception, e)
   
   
    latency, path_list = image_processing(object_key, download_path)

    for upload_path in path_list:
        s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_NAME_INDEX])

    return {"latency": latency,
            "path_list": path_list }
