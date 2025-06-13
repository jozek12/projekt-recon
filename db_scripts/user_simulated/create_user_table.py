from db_scripts import connection

conn = connection.get_connection("recon.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            name TEXT
    );
""")
c.execute("""CREATE TABLE IF NOT EXISTS Users_ratings (
            user_id INTEGER,
            movie_id INTEGER,
            rating INTEGER CHECK(rating BETWEEN 1 AND 100),
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
""")
c.execute("""CREATE TABLE IF NOT EXISTS Users_preferences(
            user_id integer,
            genre_id integer,
            status text,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (genre_id) REFERENCES genres_list(genre_id)
    );
          """)
conn.commit()
conn.close()