import os
from dotenv import load_dotenv

load_dotenv()

BASE_URI = os.getenv('ZALANDO_BASE_URI')
AUTH_URI = os.getenv('ZALANDO_AUTH_URI')
CLIENT_ID = os.getenv('ZALANDO_CLIENT_ID')
CLIENT_SECRET = os.getenv('ZALANDO_CLIENT_SECRET')
ORDER_URI = os.getenv('ZALANDO_ORDER_API')
MERCHANT_ID = os.getenv('ZALANDO_MERCHANT_ID')