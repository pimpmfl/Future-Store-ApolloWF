import redis
import os
import random
from redis.commands.json.path import Path

ec2_ip = "18.209.102.135"
supermarket_items = [
    "Bread",
    "Milk",
    "Eggs",
    "Cheese",
    "Butter",
    "Yogurt",
    "Fresh fruits",
    "Fresh vegetables",
    "Chicken",
    "Beef",
    "Pork",
    "Fish",
    "Shrimp",
    "Pasta",
    "Rice",
    "Cereal",
    "Oatmeal",
    "Snack bars",
    "Chips",
    "Soda",
    "Juice",
    "Water",
    "Coffee",
    "Tea",
    "Sugar",
    "Flour",
    "Spices",
    "Canned soup",
    "Canned vegetables",
    "Canned beans",
    "Tomato sauce",
    "Frozen pizza",
    "Ice cream",
    "Frozen vegetables",
    "Frozen fruits",
    "Bakery items",
    "Cookies",
    "Crackers",
    "Candy",
    "Condiments",
    "Salad dressing",
    "Mayonnaise",
    "Ketchup",
    "Mustard",
    "Pickles",
    "Cooking oil",
    "Vinegar",
    "Honey",
    "Peanut butter",
    "Jelly",
    "Baking powder",
    "Baking soda",
    "Chocolate",
    "Nuts",
    "Dried fruits",
    "Yeast",
    "Dish soap",
    "Laundry detergent",
    "Toilet paper",
    "Paper towels",
    "Facial tissues",
    "Cleaning supplies",
    "Shampoo",
    "Conditioner",
    "Soap",
    "Toothpaste",
    "Toothbrush",
    "Deodorant",
    "Feminine hygiene products",
    "Baby diapers",
    "Baby food",
    "Pet food",
    "Cat litter",
    "Trash bags",
    "Aluminum foil",
    "Plastic wrap",
    "Storage containers",
    "Light bulbs",
    "Batteries",
    "Magazines",
    "Newspapers",
    "Greeting cards",
    "Gift wrap",
    "Seasonal decorations",
    "Planting soil",
    "Seeds",
    "Insect repellent",
    "Sunscreen",
    "First aid supplies",
    "Medications",
    "Vitamins",
    "Office supplies",
    "Cookware",
    "Dinnerware",
    "Utensils",
    "Small appliances",
    "Electronics",
    "Clothing",
    "Footwear",
]

r = redis.Redis(
    host=ec2_ip, port=6379,
    username="default",
    password="password",
    decode_responses=True
)

active_customers = 10


def create_customer(name: str) -> dict:
    return {
        name: {
            "active_orders": {},
            "past_orders": {}

        }
    }


def create_random_order(orders: dict):
    number_of_items = random.choice([1, 2, 3, 4, 5])
    for i in range(number_of_items):
        item = random.choice(supermarket_items)
        if item in orders.keys():
            orders[item] = orders[item] + 1
        else:
            orders[item] = 1


path = "./faces"
dirs = os.listdir(path)
customers = []

for customer_name in dirs:
    customers.append(create_customer(customer_name))

# Create random past orders for every customer
for customer in customers:
    for key in customer.keys():
        create_random_order(customer[key]["past_orders"])

# Create random active orders for a select amount of customers
active_customers = random.sample(customers, active_customers)
for customer in active_customers:
    for key in customer.keys():
        create_random_order(customer[key]["active_orders"])

print("Creating entries")
for customer in customers:
    for key in customer.keys():
        name = key
        orders = customer[key]
        print("Creating entry for: ", name, "\n")
        r.json().set(name, Path.root_path(), orders, decode_keys=True)

print("Getting orders\n")
for customer in customers:
    for key in customer.keys():
        name = key
        res = r.json().get(name)
        print("Orders for ", name)
        print(res, "\n")
