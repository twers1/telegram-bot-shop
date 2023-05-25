import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
# admin_id = int(os.getenv("ADMIN_ID"))
admin_id = os.getenv("ADMIN_ID")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
host = os.getenv('HOST')
DB_URI = os.getenv('DB_URI')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
