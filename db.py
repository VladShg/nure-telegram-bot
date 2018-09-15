import psycopg2
import os

def ex():

    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    c = conn.cursor()

    # c.execute("DROP TABLE users")
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

    conn.commit()
    conn.close()

    print("inside ex function")
