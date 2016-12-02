import sqlite3
import re
conn = sqlite3.connect('basicSkills.db')
c = conn.cursor()
try:
    c.execute("""ALTER TABLE excel ADD ID""")
except:
    print('table exists')
    pass

basic1 = re.compile(r'\(.*[0-9]+.*\)')
basic2 = re.compile(r'#.+?$')

numberRE = re.compile(r'[0-9]+[A|B]?\)')
rows = c.execute("""SELECT title, isbn, id FROM basic""")
changes = []

for line in rows:

    # define id, title, isbn
    title, isbn, id = line
    if id is not None:
        continue

    number = (basic1.findall(line[0]))

    if not number:
        # use regex 2
        number = basic2.findall(line[0])
        if not number:
            print(title,isbn)
            id = input("Enter BASIC ID, Enter to cancel: ")
            if not title:
                continue
        else:
            id = number[0].lstrip("#")


    else:
        # it is good! use regex 1 (Name No.Number)
        number = number[0] # first element is ppropert
        id = numberRE.search(number).group(0)[:-1]

    changes.append((id, isbn))

for i in changes:
    c.execute("""UPDATE excel SET ID=(?) WHERE isbn=(?)""", (i))
    print("setting", i[0], "to", i[1])
conn.commit()






