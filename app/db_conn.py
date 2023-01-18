import redis as redis
from pymongo import mongo_client
import pymongo
from config import settings

client = mongo_client.MongoClient(
    settings.DATABASE_URL)

try:
    conn = client.server_info()
    print('Connected to DB')
except Exception as e:
    # fatal error
    print("Unable to connect" + str(e))

# Redis for user action Cache as you requested
try:
    Red = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    print('Connected to RDB')
except Exception as e:
    print("Unable to connect (RDB)" + str(e))

db = client[settings.MONGO_INITDB_DATABASE]

# User collection in MongoDB
User = db.users
User.create_index([("email", pymongo.ASCENDING)], unique=True)
Post = db.posts
User.create_index([("user_id", pymongo.ASCENDING)], unique=False)

