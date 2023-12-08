import json

def lambda_handler(event, context):
    # TODO check if user has an open order and return order details
    return {
        'orderId': 1,
        'orderState': 'readyForPickup'
    }
