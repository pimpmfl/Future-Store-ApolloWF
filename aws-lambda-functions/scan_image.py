import boto3

# This function takes the bytes string of an image and runs it through Amazon Rekognition to check if there are any faces present
# Returns a response in JSON
def lambda_handler(event, context):
    # Setup
    image = event['img']
    region = 'us-east-1'
    service = 'rekognition'
    # Running this on your local machine will require additional parameters for the AWS credentials
    rekognition = boto3.client(service, region)

    # Run the image through Amazon Rekognition
    response = rekognition.detect_faces(
        Image={'Bytes': image},
        Attributes=['ALL']
    )

    # Each face found in the picture has a separate attribute called FaceDetails
    if response['FaceDetails']:
        return {
            'faces_in_image': len(response['FaceDetails']),
            'image': event['img']
        }
    else:
        return {
            'faces_in_image': 0,
            'image': event['img']
        }

# Simulate event locally    
#if __name__ == '__main__':
#    with open('/home/ubuntu/Al_Davis_0001.jpg', 'rb') as image_file:
#        image_data = image_file.read()
#    
#    test_event = {
#        'img': image_data
#    }
#    response = lambda_handler(test_event, None)
#    print(response)
    