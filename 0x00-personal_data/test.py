import mysql.connector
import os

# db_connector = mysql.connector.connect(
# host="localhost",
# # database=os.getenv('PERSONAL_DATA_DB_NAME', 'holberton'),
# user="root",
# password="")

# cursor = db_connector.cursor()
# cursor.execute("SELECT COUNT(*) FROM users;")
# print(cursor.fetchone()[0])
# cursor.close()

paswd_to_hash = base64.b64encode(hashlib.sha256(
        password.encode()
        ).digest())
name = "olakunle"
print(name.encode())