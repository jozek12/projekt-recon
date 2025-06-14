from db_scripts import connection
import random
conn = connection.get_connection("recon.db")
c = conn.cursor()
c.execute("DELETE FROM Users_ratings")
conn.commit()
c.execute("""
SELECT user_id, genre_id, status FROM Users_preferences
""")
max_user_id = 0
how_much_users = 6000
user_prefs_raw = c.fetchall()
user_prefs = {}
for user_id, genre_id, status in user_prefs_raw:
    if user_id not in user_prefs:
        user_prefs[user_id] = {'liked': set(), 'disliked': set()}
    user_prefs[user_id][status].add(genre_id)
    if (user_id > max_user_id):
        max_user_id = user_id
all_movies_id = [row[0] for row in c.execute("SELECT movies_id FROM movies_genres").fetchall()]
c.execute("""
SELECT movies_id, genre_id FROM movies_genres
""")
movie_genres_raw = c.fetchall()
movie_genres = {}
for movies_id, genre_id in movie_genres_raw:
    if movies_id not in movie_genres:
        movie_genres[movies_id] = {genre_id}
    else:
        movie_genres[movies_id].add(genre_id)

ratings = []
used_users = set()
for user_counter in range(how_much_users):

    while True:
        user = random.randint(1,max_user_id)
        if user not in used_users:
            
            liked = user_prefs[user]["liked"]
            disliked = user_prefs[user]["disliked"]

            how_much_ratings = random.randint(1,50)

            used_movies = set()
            
            for rating_counter in range(how_much_ratings):
                while True:
                    movie = random.choice(all_movies_id)
                    if movie not in used_movies and movie :
                        genres = movie_genres[movie]
                        count_liked = (len(liked.intersection(genres)))
                        count_disliked = (len(disliked.intersection(genres)))
                        difference_status = count_liked - count_disliked
                        difference_status = max(-8, min(8, difference_status))

                        value = 1+((difference_status+8)*(100-1))/(16)
                        standard_deviation = 12 #change deviation when nessessary

                        random_value = int(random.gauss(value,standard_deviation))
                        random_value = max(1,min(100,random_value))

                        ratings.append((user,movie,random_value))
                        used_movies.add(movie)
                        break
            used_users.add(user)
            break
c.executemany("""INSERT OR REPLACE INTO Users_ratings VALUES(?,?,?)
""",(ratings))
conn.commit()
conn.close()