import redis
import json

EC2_IP = ""
port = 6379

r = redis.Redis(
    host=EC2_IP, port=port,
    password="password",
    decode_responses=True
)

# This function takes customer_name and order as input from has_order
# It updates the customer's order in the database and then returns a response in JSON format
def lambda_handler(event, context):
    customer_name = event["customer_name"]
    if customer_name is None:
        return {
            'notification_sent': False,
            'error': 'No customer name provided.'
        }
    
    # Get data from Redis using customer_name as key
    data = r.json().get(customer_name)

    # Check if active_orders and past_orders exist
    if 'past_orders' not in data:
        data['past_orders'] = {}
    
    if 'active_orders' not in data:
        return {
            'notification_sent': False,
            'error': 'Customer has no active_orders column.'
        }
    
    # Move everything from active_orders to past_orders
    for item, quantity in data['active_orders'].items():
        data['past_orders'][item] = quantity

    # Remove everything from active_orders and update customer's orders in database
    data['active_orders'] = {}
    r.json().set(customer_name, '.', data)
    notification_message = f"Customer {customer_name} has entered the store and has the following order {event['order']}."
    
    return {
        'notification_sent': True,
        'notification_msg': notification_message,
        'customer_name': customer_name,
        'order': event['order']
    }

# Simulate event to test the code
#if __name__ == '__main__':
#    test_event = {
#        "customer_name": "Jill Valentine",
#        "order": {
#            "Samurai Edge": 1,
#        }
#    }
#    result = lambda_handler(test_event, None)
#    print(result)
