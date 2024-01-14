
def lambda_handler(event, context):
    # TODO input is a base64 image string containing a face
    # implement logic to save the new customer in the database and return new customerId
    # also add the new customer to the rekognition collection created in map_face_to_user
    return {
        'customerId': 2
    }
