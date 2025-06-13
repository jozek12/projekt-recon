from connection import get_connection

def insert_into(data):
    conn = get_connection('recon.db')
    c = conn.cursor()

    movie_id = data["id"]
    genre_names = data["genres"]

    for genre_name in genre_names:
        c.execute("SELECT genre_id FROM genres_list WHERE name = ?", (genre_name,))
        result = c.fetchone()
        c.execute(
                "INSERT INTO movies_genres (movies_id, genre_id) VALUES (?, ?)",
                (movie_id, result)
            )
    conn.commit()
    conn.close()