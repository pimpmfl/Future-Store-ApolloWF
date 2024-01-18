import redis, json,boto3, base64
ec2IP = '44.206.127.26'

def create_new_user(face):
    #Redis
    r = redis.Redis(
        host=ec2IP, port=6379,
        username="default",
        password="Mkmkl0loopo",
        decode_responses=True,
    )
    new_customer_id = 'TMP_' + str(len(r.keys()))
    r.json().set(new_customer_id, '.', {'active_orders':{}, 'past_orders':{}})
    image_key = f'faces/{new_customer_id}/{new_customer_id}_0001.jpg'
    s3image = upload_image_to_s3(key, face)
    index_faces(s3image, new_customer_id)
    return new_customer_id



def upload_image_to_s3(key, image_bytes):
    #S3
    bucket_name = 'automatedstore'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    bucket.put_object(Key=key, Body=image_bytes)
    return bucket.Object(key)

def index_faces(image, key):
    #Rekogition
    region = 'us-east-1'
    service = 'rekognition'
    rekognition = boto3.client(service, region)
    collection_id='currentUsersInDatabase'


    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {
            'Bucket' : image.bucket_name,
            'Name': image.key
        }},
        ExternalImageId=key
    )
    return response['FaceRecords']


def lambda_handler(event, context):
    face64 = event.get('face')
    if face64 is None: 
        return {
            'error': "No image has been provided."
        }
    face = base64.b64decode(face64)
    new_customer_id= create_new_user(face)
    return {
        'customer_name': new_customer_id,
    }
