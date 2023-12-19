import redis
import random
import json
from redis.commands.json.path import Path

"This function checks weather the user has an active order"
"Returns various information related to the customer, can be adapted as needed"

# Change IP as needed
EC2_IP = "18.209.102.135"

r = redis.Redis(
    host=EC2_IP, port=6379,
    username="default",
    password="password",
    decode_responses=True
)


def has_active_order(customer: dict):
    return len(customer["active_orders"].keys()) > 0


def lambda_handler(event, context):
    customer_name = event["customer_name"]
    customer = r.json().get(customer_name)

    return {
        "customer_name": customer_name,
        "has_order": has_active_order(customer),
        'order': customer["active_orders"],
        'orderState': 'readyForPickup'
    }


"Uncomment for testing"
# lambda_event = {
#    "customer_name": "Leon S. Kennedy"
# }

# print(lambda_handler(lambda_event, None))
