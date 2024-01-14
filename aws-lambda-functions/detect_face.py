import json, base64
from PIL import Image
from io import BytesIO
def lambda_handler(event, context):
    faces_in_image = event.get('faces_in_image')
    print(event.keys())
    image = event.get('image')
    if image is None: 
        return {
            'error': "No image has been provided."
        }

    image_data = base64.b64decode(image)
    image_decoded = Image.open(BytesIO(image_data))
    if faces_in_image == 0:
        return {
            'face_images': []
        }
    
    face_details = event.get('FaceDetails')
    if face_details is None:
        return {
            'error': "No faces detected in the provided image."
        }

    # Split the image into multiple ones with faces
    face_images = []
    for face_detail in face_details:
        # Extract bounding box information for each face
        bounding_box = face_detail['BoundingBox']
        left = int(image_decoded.width * bounding_box['Left'])
        top = int(image_decoded.height * bounding_box['Top'])
        width = int(image_decoded.width * bounding_box['Width'])
        height = int(image_decoded.height * bounding_box['Height'])

        # Crop the face from the original image
        face_image = image_decoded.crop((left, top, left + width, top + height))
        bytes = BytesIO()
        face_image.save(bytes, 'jpeg')
        im_bytes = bytes.getvalue()
        
        #store the face as base64 string
        face_images.append({'face': base64.b64encode(im_bytes).decode('utf-8')})

    # Now face_images contains individual face images
    return {
        'faces': face_images 
    }

# if __name__ == '__main__':
#     with open('test_event.json', 'r') as test_event_data:
#         json_string = test_event_data.read()
#         test_event = json.loads(json_string)
#         response = lambda_handler(test_event,None)
#         print(response)
#         with open('response_detect_face.json', 'w') as f:
#             json.dump(response, f)