from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi # Import this package

# Create the CA certificate variable
ca = certifi.where()

# PLEASE REPLACE THE PASSWORD BELOW WITH YOUR NEW ONE
uri = "mongodb+srv://neerajb0408_db_user:<password>@cluster0.ksl73ak.mongodb.net/?appName=Cluster0"

# Add tlsCAFile=ca to the MongoClient
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)