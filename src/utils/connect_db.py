import psycopg2

from src.config import DB_URI

con = psycopg2.connect(DB_URI)
cursor_obj = con.cursor()