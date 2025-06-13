from db_scripts import connection
conn = connection.get_connection("recon.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS movies  (
          movie_id integer PRIMARY KEY,
          averageScore integer,
          seasonYear integer,
          description text
          );
""")
c.execute("""CREATE TABLE IF NOT EXISTS genres_list(
          genre_id integer PRIMARY KEY,
          name text UNIQUE
          );
""")
c.execute("""CREATE TABLE IF NOT EXISTS movies_genres(
          movies_id integer,
          genre_id integer,
          PRIMARY KEY(movies_id,genre_id)
          );
""")
c.execute("""CREATE TABLE IF NOT EXISTS movies_translations(
          movie_id integer,
          title text,
          language text,
          FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
          );
""")
conn.close()