import json

def lambda_handler(event, context):
    # TODO base64 encoded image string
    # run it through Amazon Rekognition
    # return if there are people's faces in the image
    return {
        'presentFaces': True,
        'base64Image': "someString"
    }
