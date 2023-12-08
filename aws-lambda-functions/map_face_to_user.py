import json

def lambda_handler(event, context):
    # TODO input is a base64 encoded image string containing a single face
    # check if face can be mapped to somebody in the database and return customerId, else -1
    return {
        'customerId': -1
    }
