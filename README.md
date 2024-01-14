# Future-Store-ApolloWF

## About
This project focuses on creating an Apollo workflow that triggers AWS Lambda functions to identify customers in a store, register new ones, notify the storage about an open order of a customer when it enters the store and also send push notifications to customers in the store about all promotions/offers.

The pictures of the customers entering the store are run through Amazon Rekognition.  

## Tech Stack
- [ApolloWF](https://apollowf.github.io/)
- [AFCL](https://dps.uibk.ac.at/projects/afcl/subpages/user-documentation/index.html)
- [AWS](https://aws.amazon.com/)
- [Python](https://www.python.org/)


## Setup:

### EC2:
Add an inbound TCP rule on port 6379 
Don't forget to update the IAM role of the instance to LabRole

### Lambda Functions:
Add layers to functions
Configure correct VPC for functions that need access to the EC2 Cluster and change the EC2-IP in the code to private IPv4 addresses of EC2 instance