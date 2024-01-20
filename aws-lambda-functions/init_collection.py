import boto3
import redis
# IMPORTANT: This function takes a long time to build the initial indecies. 
# Set timeout for first run to 60+ seconds and reduce afterwards

ec2IP = 'ec2-44-206-127-26.compute-1.amazonaws.com'

def create_face_collection(rekognition, collection_id):
    existing_collections = rekognition.list_collections(
        MaxResults=5).get('CollectionIds')
    if ((existing_collections is None) or (collection_id not in existing_collections)):
        rekognition.create_collection(CollectionId=collection_id)
        return True
    else:
        return False

def index_faces(rekognition, collection_id, image, key):
    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {
            'Bucket': image.bucket_name,
            'Name': image.key
        }},
        ExternalImageId=key
    )
    return response['FaceRecords']

def index_collection(redis, bucket, rekognition, collection_id):
    print('indexing')
    for username in redis.keys():
        # connect to s3 and recieve the images for each user
        folder_path = 'faces/' + username
        images_of_user = bucket.objects.filter(Prefix=folder_path)
        for user_image in images_of_user:
            index_faces(rekognition, collection_id, user_image, username)

def lambda_handler(event, context):
    # Rekogition
    region = 'us-east-1'
    service = 'rekognition'
    rekognition = boto3.client(service, region)
    collection_id = 'currentUsersInDatabase'

    # S3
    bucket_name = 'automatedstore'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # Redis
    r = redis.Redis(
        host=ec2IP, port=6379,
        username="default",
        password="Mkmkl0loopo",
        decode_responses=True,
    )

    # rekognition.delete_collection(CollectionId=collection_id)
    # raise Exception('deleted collection')
    
    if create_face_collection(rekognition, collection_id):
        index_collection(r, bucket, rekognition, collection_id)

    return event


