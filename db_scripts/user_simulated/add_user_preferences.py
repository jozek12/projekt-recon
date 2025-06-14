from db_scripts import connection
from random import randint
conn = connection.get_connection("recon.db")
how_much_dislike = 4 
how_much_like = 4
c = conn.cursor()
c.execute("DELETE FROM Users_preferences")
conn.commit()
max_genre_id = c.execute("""SELECT MAX(genre_id) FROM genres_list""").fetchone()[0]
max_user_id = c.execute("""SELECT MAX(user_id) FROM Users""").fetchone()[0]
for user in range(max_user_id):
    used_genres = set()
    for user_genre_number in range(1, (how_much_like + how_much_dislike)+1):
        while True:
            random = randint(1, max_genre_id)
            if random not in used_genres:
                used_genres.add(random)
                break
        if user_genre_number < how_much_like+1:
            c.execute("""INSERT OR REPLACE INTO Users_preferences VALUES (?,?,?)""", (user+1, random, "liked"))
        else:
            c.execute("""INSERT OR REPLACE INTO Users_preferences VALUES (?,?,?)""", (user+1, random, "disliked"))
conn.commit()
conn.close()