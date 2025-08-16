from pymongo.mongo_client import MongoClient

uri="mongodb://localhost:27017/"
client=MongoClient(uri)
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    raise e