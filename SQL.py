import sqlite3
import openpyxl
def create_database(conn):
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE excel
                 (title text, authors text, isbn text, front_qty integer, back_qty, price integer, image text)''')
    except:
        pass

free_keywords = {"FREE"}

def notNone(iterable):
    for i in iterable:
        if i is None:
            return False
    return True

def read_excel(filepath, conn, debug=0):
    """
    reads from excel essential books
    :param filepath: excel path
    :param conn: sqlite3.connection
    :param debug: 0=None (default), 1=Show servere warnings (duplicates), 2=Show changes and insertions, 3=Show skips
    :return:
    """
    #print("WARNING! ENSURE NO HARMFUL DATA IS IN THE EXCEL DOC! A BACKUP WILL BE SAVED&ONLY PRESS ENTER IF YOU KNOW WAT YOUR DOING!!!")

    #input()
    c = conn.cursor()
    wb = openpyxl.load_workbook(filepath)
    ws = next(iter(wb))
    seen = set()
    for row in ws:

        rowlist = tuple(x.value if (iter != 2 and x.value not in free_keywords) else str(x.value) if x.value not in free_keywords else 0.0 for iter,x in enumerate(row[1:5]))  #title,author,isbn,rrpt
        title,author,isbn,rrp = rowlist # title, author, isbn, rrp
        # filter out already seen isbn's
        if isbn in seen:
            if debug >= 1 and notNone(rowlist):
                print('duplicate isbn', rowlist)
            continue
        seen.add(isbn)

        # from excel doc, the proper value
        if notNone(rowlist) and not rowlist[0].lower().startswith('title'): # all title,author,isbn and rrp
            #print(rowlist[3], type(rowlist[3]))

            c.execute("SELECT title,authors,isbn,price FROM excel WHERE isbn=(?) LIMIT 1", (isbn,))
            fetch = c.fetchone()

            if fetch:
                # if the record is already in database
                if not fetch == rowlist:
                    # if the record is not the same
                    if debug >= 2:
                        print("converting", fetch, 'to', rowlist)
                    c.execute("""UPDATE excel SET
                              title=(?),
                              authors=(?),
                              price=(?)
                              WHERE isbn=(?);""", (title,author,rrp,isbn))

                else:
                    # the record is the same as required
                    if debug >= 3:
                        print("The item is already correct!", fetch)
            else:
                # the record is not in database, insert with INSERT INTO
                c.execute("""INSERT INTO excel
                    (title, authors, isbn, price, front_qty, back_qty) VALUES
                    (?,?,?,?,0,0)""", rowlist)
                if debug >= 2:
                    print("INSERTING", rowlist, "INTO DATABASE")







conn = sqlite3.connect('database.db')
create_database(conn)
read_excel('seed.xlsx', conn, debug=1)
conn.commit()
conn.close()

