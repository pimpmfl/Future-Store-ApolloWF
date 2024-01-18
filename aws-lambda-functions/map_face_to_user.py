import json, redis, boto3, base64, os
# IMPORTANT: This function takes a long time to build the initial indecies. Set timeout for first run to 60+ seconds and reduce afterwards
ec2IP = 'ec2-44-206-127-26.compute-1.amazonaws.com'

def create_face_collection(rekognition, collection_id):
    existing_collections=rekognition.list_collections(MaxResults=5).get('CollectionIds')

    if ((existing_collections is None) or (collection_id not in existing_collections)):
        rekognition.create_collection(CollectionId=collection_id)
        return True
    else:
        return False

def index_faces(rekognition, collection_id, image, key):
    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {
            'Bucket' : image.bucket_name,
            'Name': image.key
        }},
        ExternalImageId=key
    )
    return response['FaceRecords']

def search_faces_by_image(rekognition, collection_id, image_bytes):
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes}
    )
    return response['FaceMatches']

def index_collection(redis, bucket, rekognition, collection_id):
    print('indexing')
    for username in redis.keys():
        #connect to s3 and recieve the images for each user
        folder_path = 'faces/' + username
        images_of_user = bucket.objects.filter(Prefix=folder_path)
        for user_image in images_of_user:
            index_faces(rekognition,collection_id, user_image, username)
        
def lambda_handler(event, context):
    face64 = event.get('face')
    if face64 is None: 
        return {
            'error': "No image has been provided."
        }
    face = base64.b64decode(face64)
    print('start')
    #S3
    bucket_name = 'automatedstore'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    #Rekogition
    region = 'us-east-1'
    service = 'rekognition'
    rekognition = boto3.client(service, region)
    collection_id='currentUsersInDatabase'
    
    #Redis
    r = redis.Redis(
        host=ec2IP, port=6379,
        username="default",
        password="Mkmkl0loopo",
        decode_responses=True,
    )


#    rekognition.delete_collection(CollectionId=collection_id)
#    return{'msg':'deleted collection'}
    if create_face_collection(rekognition, collection_id):
        index_collection(r, bucket, rekognition, collection_id)


    highest_confidence:float = 0
    best_match:str = '-1'

    search_results = search_faces_by_image(rekognition, collection_id, face)
    for match in search_results:
        similarity = match.get('Similarity')
        if similarity > 80 and similarity > highest_confidence:
            highest_confidence=similarity
            best_match = match.get('Face')['ExternalImageId']
            
    if (best_match != '-1') and (best_match not in r.keys()):
        print(f'user {best_match} not present in database. deleting matched image from collection')
        face_ids = []
        faces = rekognition.list_faces(CollectionId=collection_id)['Faces']
        for face in faces:
            if face.get('ExternalImageId') == best_match:
                face_ids.append(face['FaceId'])
        
        rekognition.delete_faces(CollectionId=collection_id, FaceIds=face_ids)
        best_match='-1'

    print('Best match:', best_match)
    return {
        'customer_name': best_match,
        'face': face64
    }


# # Simulate locally
# if __name__ == '__main__':
#     with open('response_detect_face.json', 'r') as test_event_data:
#         json_string = test_event_data.read()
#         face = json.loads(json_string)
#         response = lambda_handler(face,None)
#         with open('response_map_face_to_user.json', 'w') as f:
#             json.dump(response, f)