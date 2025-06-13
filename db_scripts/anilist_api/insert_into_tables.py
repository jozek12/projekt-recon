from db_scripts import connection
def insert_into(data):
    conn = connection.get_connection('recon.db')
    c = conn.cursor()
    c.execute("""INSERT INTO movies 
              (movie_id, averageScore, seasonYear, description)
              VALUES(?,?,?,?);
        """,(data['id'],data['averageScore'],data['seasonYear'],data['description']))
    c.executemany("""INSERT OR IGNORE INTO genres_list (name)
              VALUES(?)
        """,((genre,) for genre in data['genres']))
    c.execute("""INSERT INTO movies_translations 
              VALUES(?,?,?)
        """,(data['id'],data['title']['english'],'en'))
    c.execute("""INSERT INTO movies_translations 
              VALUES(?,?,?)
        """,(data['id'],data['title']['native'],'jp'))
    c.execute("""INSERT INTO movies_translations 
              VALUES(?,?,?)
        """,(data['id'],data['title']['romaji'],'ro'))
    movie_id = data["id"]
    genre_names = data["genres"]
    for genre_name in genre_names:
        c.execute("SELECT genre_id FROM genres_list WHERE name = ?", (genre_name,))
        result = c.fetchone()
        c.execute(
                "INSERT INTO movies_genres (movies_id, genre_id) VALUES (?, ?)",
                (movie_id, result)
            )
    conn.close()