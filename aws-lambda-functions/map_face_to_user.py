import json, redis, boto3, base64

ec2IP = '127.0.0.1'

def lambda_handler(event, context):
    face64 = event.get('face')
    if face64 is None: 
        return {
            'error': "No image has been provided."
        }

    face = base64.b64decode(face64)
    region = 'us-east-1'
    service = 'rekognition'
    # Running this on your local machine will require additional parameters for the AWS credentials
    rekognition = boto3.client(service, region)

    bucket_name = 'automatedstore'
    s3 = boto3.client('s3')
   
    r = redis.Redis(
        host=ec2IP, port=6379,
        username="default",
        password="Mkmkl0loopo",
        decode_responses=True
    )

    highest_confidence:float = 0
    best_match:str = '-1'

    print('matching faces...this might take some time')
    for key in r.keys():
        #connect to s3 and recieve the images for each user
        folder_path = 'faces/' + key
        s3_response = s3.list_objects(Bucket=bucket_name, Prefix=folder_path)
        if 'Contents' in s3_response:
            for obj in s3_response['Contents']:
                object_key = obj['Key']
                target_image_bytes=s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read()        

                response = rekognition.compare_faces(
                    SourceImage={'Bytes': face},
                    TargetImage={'Bytes': target_image_bytes},
                    SimilarityThreshold= 80
                )
                matches=response.get('FaceMatches')
                for match in matches:
                    similarity = match.get('Similarity')
                    if similarity > highest_confidence:
                        highest_confidence=similarity
                        best_match = key

    return {
        'customerId': best_match
    }



# #Simulate locally
# if __name__ == '__main__':
#     with open('response_detect_face.json', 'r') as test_event_data:
#         json_string = test_event_data.read()
#         faces = json.loads(json_string).get('faces')
#         test_event = {
#             'faces' : faces,
#             'face': faces[0]
#         }
#         response = lambda_handler(test_event,None)
#         with open('response_map_face_to_user.json', 'w') as f:
#             json.dump(response, f)