import sqlite3
db = 'db/api.db'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(str(e))

    return conn

def create_table():
    sql1 = '''
    CREATE TABLE "tvshows" (
	"imdb"	TEXT NOT NULL,
	"season"	INTEGER NOT NULL,
	"episode"	INTEGER NOT NULL,
	"stream"	TEXT NOT NULL
    );
    '''
    sql2 = '''
    CREATE TABLE "movies" (
    "imdb"	TEXT NOT NULL,
	"stream"	TEXT NOT NULL
    );        
    '''
    conn = create_connection(db)
    cursor = conn.cursor()
    cursor.execute(sql1)
    cursor.execute(sql2)
    conn.close()

def insert_movie(name,stream):
    sql = "INSERT INTO movies (imdb, stream) VALUES ('{0}', '{1}')".format(str(name),str(stream))
    conn = create_connection(db)
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        print('dados inseridos')
    else:
        print('Falha')

def insert_tvshow(name,season,episode,stream):
    sql = "INSERT INTO tvshows (imdb, season, episode, stream) VALUES ('{0}', '{1}', '{2}', '{3}')".format(str(name),int(season),int(episode),str(stream))
    conn = create_connection(db)
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        print('dados inseridos')
    else:
        print('Falha')

def show_movie():
    sql = "SELECT * FROM movies"
    conn = create_connection(db)
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    else:
        rows = ''
    return rows

def show_tvshow():
    sql = "SELECT * FROM tvshows"
    conn = create_connection(db)
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    else:
        rows = ''
    return rows

#linha = show_tvshow()
#print(linha)
#print(linha)
#insert_data('teste')
#create_table()
#for imdb, season, episode, url in linha:
#print(imdb)



