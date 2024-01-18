import redis
import random

"This functions generates a recommend order for a given user based on their previously purchased items"

# Change IP as needed
EC2_IP = "ec2-44-206-127-26.compute-1.amazonaws.com"

r = redis.Redis(
    host=EC2_IP, port=6379,
    username="default",
    password="Mkmkl0loopo",
    decode_responses=True
)


def get_past_orders(customer_name: str):
    customer = r.json().get(customer_name)
    return customer["past_orders"]


def generate_recommended_order(past_orders: dict):
    recommended_order = {}
    number_of_items = random.choice([1, 2, 3, 4, 5])
    past_items = []

    if len(past_orders.keys()) == 0:
        return None

    # Add past items to a list, so its compatible with random.choice
    for item in past_orders.keys():
        past_items.append(item)


    for i in range(number_of_items):
        item = random.choice(past_items)
        if item in recommended_order.keys():
            recommended_order[item] = recommended_order[item] + 1
        else:
            recommended_order[item] = 1

    return recommended_order


def lambda_handler(event, context):
    customer_name = event["customer_name"]
    past_orders = get_past_orders(customer_name)
    recommended_order = generate_recommended_order(past_orders)

    return {
        'successfullyNotified': True,
        "recommended_order": recommended_order
    }


# "Uncomment for testing"
# lambda_event = {
#   "customer_name": "Alicia_Witt",
#   "has_order": False,
#   "order": {},
#   "orderState": "readyForPickup"
# }

# print(lambda_handler(lambda_event, None))
