import sqlite3
import config
import datetime

conn = sqlite3.connect('user.db')

c = conn.cursor()

#c.execute("SELECT * FROM users WHERE id = :id", {'id': config.MY_ID})
#obj = c.fetchone()
#num = obj[7] + 1

c.execute("""CREATE TABLE users (
    id integer,
    name string,
    short_subj integer,
    short_teacher integer,
    faculty_name string,
    group_name string,
    group_id integer,
    last_update string,
    updates integer,
    grp_state integer
    )""")


conn.commit()
conn.close()