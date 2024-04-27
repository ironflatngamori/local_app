import sqlite3
from config import __DB_FILE__


conn = sqlite3.connect(__DB_FILE__)
cursor = conn.cursor()