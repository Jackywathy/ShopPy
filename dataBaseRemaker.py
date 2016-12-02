import sqlite3
out = sqlite3.connect('out.db')
indb = sqlite3.connect('temp.db')
outc = out.cursor()
indbc = indb.cursor()
try:
    outc.execute("""CREATE TABLE basic
    (title text, authors text, isbn text, front_qty integer,
    back_qty integer, price integer, image text, ID integer)""")
except sqlite3.OperationalError:
    pass
to = 0
for i in indbc.execute("""SELECT * FROM excel"""):
    outc.execute("""INSERT INTO basic
                    (title, authors, isbn, front_qty, back_qty, price, image, ID) VALUES
                    (?,?,?,?,?,?,?,?)""", i)

out.commit()
