from db_scripts import connection
import random
conn = connection.get_connection("recon.db")
c = conn.cursor()

# Fetch user preferences
c.execute("""
SELECT user_id, genre_id, status FROM Users_preferences
""")
user_prefs_raw = c.fetchall()

# Organize user preferences into a dictionary
user_prefs = {}
for user_id, genre_id, status in user_prefs_raw:
    user_prefs.setdefault(user_id, {'liked': set(), 'disliked': set()})
    user_prefs[user_id][status].add(genre_id)

# Fetch all movies and their genres
c.execute("""
SELECT movies_id, genre_id FROM movies_genres
""")
movie_genres_raw = c.fetchall()

# Organize movie genres
movie_genres = {}
for movie_id, genre_id in movie_genres_raw:
    movie_genres.setdefault(movie_id, set()).add(genre_id)

# Clear existing ratings (optional)
# c.execute("DELETE FROM Users_ratings")

# Generate ratings
for user_id, prefs in user_prefs.items():
    for movie_id, genres in movie_genres.items():
        liked_overlap = len(genres & prefs['liked'])
        disliked_overlap = len(genres & prefs['disliked'])

        if liked_overlap > disliked_overlap:
            rating = random.randint(70, 100)
        elif disliked_overlap > liked_overlap:
            rating = random.randint(1, 40)
        else:
            rating = random.randint(41, 69)

        # Insert into Users_ratings
        c.execute("""
        INSERT OR REPLACE INTO Users_ratings (user_id, movie_id, rating)
        VALUES (?, ?, ?)
        """, (user_id, movie_id, rating))

conn.commit()
conn.close()