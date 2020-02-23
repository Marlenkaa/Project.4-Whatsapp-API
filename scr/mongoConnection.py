from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/apichat")

# Reading database collections
users = client.get_default_database()['users']
chats = client.get_default_database()['chats']
conversations = client.get_default_database()['conversations']