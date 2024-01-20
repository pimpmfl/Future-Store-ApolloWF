import json
import redis
import boto3
import base64
import os
ec2IP = 'ec2-44-206-127-26.compute-1.amazonaws.com'

def get_best_match(search_results):
    highest_confidence: float = 0
    best_match: str = '-1'

    for match in search_results:
        similarity = match.get('Similarity')
        if similarity > 80 and similarity > highest_confidence:
            highest_confidence = similarity
            best_match = match.get('Face')['ExternalImageId']
            
    return best_match


def remove_face_from_collection(rekognition, collection_id, username):
    face_ids = []
    faces = rekognition.list_faces(CollectionId=collection_id)['Faces']
    for face in faces:
        if face.get('ExternalImageId') == username:
            face_ids.append(face['FaceId'])

    rekognition.delete_faces(CollectionId=collection_id, FaceIds=face_ids)


def search_faces_by_image(rekognition, collection_id, image_bytes):
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes}
    )
    return response['FaceMatches']


def lambda_handler(event, context):
    face64 = event.get('face')
    if face64 is None:
        return {
            'error': "No image has been provided."
        }
    face = base64.b64decode(face64)

    # Rekogition
    region = 'us-east-1'
    service = 'rekognition'
    rekognition = boto3.client(service, region)
    collection_id = 'currentUsersInDatabase'

    # Redis
    r = redis.Redis(
        host=ec2IP, port=6379,
        username="default",
        password="Mkmkl0loopo",
        decode_responses=True,
    )

    search_results = search_faces_by_image(rekognition, collection_id, face)
    best_match = get_best_match(search_results)

    if (best_match != '-1') and (best_match not in r.keys()):
        print(
            f'user {best_match} not present in database. deleting matched image from collection')
        remove_face_from_collection(rekognition, collection_id, best_match)
        best_match = '-1'

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
