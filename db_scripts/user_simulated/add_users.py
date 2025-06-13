from db_scripts import connection
from random_username.generate import generate_username

conn = connection.get_connection("recon.db")
c = conn.cursor()
how_much = 20
for _ in range(how_much):
    username = generate_username(1)
    c.execute("INSERT INTO Users (name) VALUES (?)", (username))
conn.commit()
conn.close()