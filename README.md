# Future-Store-AWS-StepFunctions

## About
This project focuses on creating an **AWS Step Functions** workflow that triggers AWS Lambda functions to identify customers in a store, register new ones, notify the storage about an open order of a customer when he/she enters the store and also send push notifications to customers in the store about all promotions/offers.

The pictures of the customers entering the store are run through Amazon Rekognition.  

## Tech Stack
- [AWS](https://aws.amazon.com/)
    - [AWS Step Functions](https://aws.amazon.com/step-functions/)
    - [ASL](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html)
    - [S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
    - [Rekognition](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html)
- [Python](https://www.python.org/)
- [Redis](https://redis.io/)



## Setup:

### EC2:
- Add an inbound TCP rule on port 6379 (RedisPort)
- Don't forget to update the IAM role of the instance to LabRole  
- Optionally you can create an elastic IP for your instance

---   

### Redis
- Install [Redis](https://redis.io/docs/install/install-redis/install-redis-from-source/)
- Install the [RedisJSON](https://github.com/RedisJSON/RedisJSON/) Module
- update the path of the RedisJSON module in start_server.sh

### Lambda Functions:
For Lambda functions use Python 3.12 runtime(x86_64)
#### Add layers to functions  
redis_layer:
- init_collection.py
- map_face_to_user.py
- has_order.py
- notify_storage.py
- notify_relevant_offers.py

#### Replace connection data
Replace the EC2 address in the code of the above functions with the public DNS of your elastic IP or use the private IP of your EC2 instance  
Don't forget to update the database password/port aswell

---  

### VPC:
Create a VPC for your EC2 Instance

#### Set VPC for Lambda Functions
All functions that access the database must be run inside a VPC (select the same as EC2)  
For Security Roles it is important to create a new default role:  
- VpcEndpointLambdaSecurityGroup
- Inbound: None
- Outbound:
    - Protocoll: All
    - Ports: All
    - Destination: 0.0.0.0/0

Additionally the functions that use Rekognition (init_collection, map_faces_to_users, register_user) requires an additional SecurityGroup otherwise the Rekognition API cannot be accessed:
- Inbound:
    - Protocoll: All
    - Ports: All
    - Destination: 0.0.0.0/0


#### Endpoints
Create VPC endpoints with default SecurityGroup
- Create a VPC endpoint for S3 (com.amazonaws.us-east-1.s3)(Gateway)
- Create a VPC endpoint for Rekognition(rekognition.us-east-1.amazonaws.com)

---   

---   
