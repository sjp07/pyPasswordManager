import sqlite3 as sq

db = 'secure.db'


def connect():
    # used to connect to the secure.db database
    conn = sq.connect(db)

    # defined a cursor to retrieve one data/tuple at
    # a time
    c = conn.cursor()

    # execute will execute the entire sql command as
    # it is
    c.execute("""
				CREATE TABLE IF NOT EXISTS data (
					site text,
					user text,
					password text primary key

				)			
	""")

    # to commit the sql command, it will commit the
    # current transaction or
    conn.commit()
    conn.close()


def enter(site, user, pas):
    conn = sq.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES(?,?,?)", (site, user, pas))
    conn.commit()
    conn.close()


def show():
    conn = sq.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM data")

    # this will store all the data from the table to
    # the variable i in the form of 2d list
    i = c.fetchall()
    conn.commit()
    conn.close()
    return i


def Del(password):
    conn = sq.connect(db)
    c = conn.cursor()
    c.execute("DELETE FROM data WHERE password=(?)", (password,))
    conn.commit()
    conn.close()


def edit(site, user, password):
    conn = sq.connect(db)
    c = conn.cursor()
    c.execute("UPDATE data SET site=?, user=(?) WHERE password=(?) ",
              (site, user, password))
    conn.commit()
    conn.close()


def check():
    # this function will check whether the database
    # is empty or not
    if len(show()) == 0:
        return False
    else:
        return True


# calling the connect function to create a table and
# database if it doesn't exists
connect()
