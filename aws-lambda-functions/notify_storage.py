import json

def lambda_handler(event, context):
    # TODO get orderId as input and send notification to storage to fulfill it
    # update order status in database
    return {
        'notificationSent': True
    }
