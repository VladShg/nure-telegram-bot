import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

def create_users():
    with conn:
        c.execute("""CREATE TABLE users(
                id INTEGER  NOT NULL,
                name VARCHAR(50) NOT NULL,
                short_subj INTEGER NOT NULL,
                short_teacher INTEGER NOT NULL,
                faculty_name VARCHAR(50) NOT NULL,
                group_name VARCHAR(50) NOT NULL,
                group_id INTEGER NOT NULL,
                last_update TIMESTAMP,
                updates INTEGER NOT NULL,
                grp_state INTEGER NOT NULL,
                notify INTEGER NOT NULL,
                time_state INTEGER NOT NULL,
                pair_state INTEGER
            )""")

def drop_users():
    with conn:
        c.execute("DROP TABLE users")

def create_cache():
    with conn:
        c.execute("""CREATE TABLE cache(
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                events JSON NOT NULL,
                teachers JSON,
                subjects JSON,
                types JSON,
                url TEXT NOT NULL
            )""")

def drop_cache():
    with conn:
        c.execute("DROP TABLE cache")