import ssl

import motor.motor_asyncio

MONGODB_URL = "mongodb+srv://dasein:788556@chat.govob.mongodb.net/chat?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL, ssl_cert_reqs=ssl.CERT_NONE)
db = client['chat']

SALT = b'$2b$12$7J78V4g/gse4Kr7B2PrdyO'

TOKEN_KEY = 'e&q$bte6o+7i#oo=*_d=!l2#-e&&c=gq9uetrdb08m2r@z9nek'
