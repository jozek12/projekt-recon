from db_scripts import connection
from random import randint
conn = connection.get_connection("recon.db")
c = conn.cursor()
max_genre_id = c.execute("""SELECT MAX(genre_id) FROM genres_list""").fetchone()[0]
max_user_id = c.execute("""SELECT MAX(user_id) FROM Users""").fetchone()[0]
for user in range(max_user_id):
    used_genres = set()
    for user_genre_number in range(1, 4):
        while True:
            random = randint(1, max_genre_id)
            if random not in used_genres:
                used_genres.add(random)
                break
        if user_genre_number < 3:
            c.execute("""INSERT INTO Users_preferences VALUES (?,?,?)""", (user+1, random, "liked"))
        else:
            c.execute("""INSERT INTO Users_preferences VALUES (?,?,?)""", (user+1, random, "disliked"))
conn.commit()
conn.close()