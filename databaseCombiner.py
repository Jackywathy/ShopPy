import sqlite3
conn1 = sqlite3.connect('basicSkills.db')
conn2 = sqlite3.connect('excel.db')
out = sqlite3.connect("database.db")
outc = out.cursor()
conn1c = conn1.cursor()
conn2c = conn2.cursor()
outc.execute('''CREATE TABLE excel
(title text, authors text, isbn text, front_qty integer, back_qty, price integer, image text)''')
outc.execute("""CREATE TABLE basic
    (title text, authors text, isbn text, front_qty integer,
    back_qty integer, price integer, image text, id integer)""")
for i in conn1c.execute("SELECT * FROM basic"):
    outc.execute("""INSERT INTO basic
                    (title, authors, isbn, front_qty, back_qty, price, image, id) VALUES
                    (?,?,?,?,?,?,?,?)""", i)
    print(i)
for i in conn2c.execute("SELECT * FROM excel"):
    outc.execute("""INSERT INTO excel
                        (title, authors, isbn, front_qty, back_qty, price, image) VALUES
                        (?,?,?,?,?,?,?)""", i)
out.commit()
