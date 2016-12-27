import sqlite3


class SQLDatabase:
    openDataBases = []
    def __init__(self, databaseName):
        self.connection = sqlite3.connect(databaseName)
        self.c = self.connection.cursor()
        self.openDataBases.append(self.connection)

    def getData(self, isbn):
        """Gets all data from database: (title, authors, isbn, front_qty, back_qty, price, image, optional[ID])"""
        basic   = self.c.execute("SELECT * FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        excel   = self.c.execute("SELECT * FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        basicId = self.c.execute("SELECT * FROM basic WHERE id=(?)   LIMIT 1", (isbn,)).fetchone()
        sap     = self.c.execute("SELECT * FROM sap   WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        return basic if basic is not None else excel if excel is not None else basicId if basicId is not None else sap

    def getISBN(self, IDorISBN):
        """Returns the ISBN, given ISBN or ID"""
        basic   = self.c.execute("SELECT isbn FROM basic WHERE isbn=(?) LIMIT 1", (IDorISBN,)).fetchone()
        excel   = self.c.execute("SELECT isbn FROM excel WHERE isbn=(?) LIMIT 1", (IDorISBN,)).fetchone()
        basicId = self.c.execute("SELECT isbn FROM basic WHERE id=(?)   LIMIT 1", (IDorISBN,)).fetchone()
        sap     = self.c.execute("SELECT isbn FROM sap   WHERE isbn=(?) LIMIT 1", (IDorISBN,)).fetchone()
        return basic[0] if basic is not None else excel[0] if excel is not None else basicId[0] if basicId is not None else sap[0] if sap is not None else None

    def set_qty(self, isbn, front=None, back=None):
        """Updates the qty of the given ISBN to front or back if supplied"""
        if self.c.execute("SELECT 1 FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone():
            table = 'excel'
        elif self.c.execute("SELECT 1 FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone():
            table = 'basic'
        else:
            raise Exception
        if front is not None:
            self.c.execute("""UPDATE (?) SET
                                  front_qty=(?)
                                  WHERE isbn=(?);""", (table,front,isbn))
        if back is not None:
            self.c.execute("""UPDATE (?) SET
                                  back_qty=(?)
                                  WHERE isbn=(?);""", (table,back,isbn))

    def getName(self, isbn):
        """Returns the title, given isbn or ID"""
        basic   = self.c.execute("SELECT title FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        excel   = self.c.execute("SELECT title FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        basicId = self.c.execute("SELECT title FROM basic WHERE id=(?) LIMIT 1", (isbn,)).fetchone()
        sap     = self.c.execute("SELECT title FROM sap   WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        return basic[0] if basic is not None else excel[0] if excel is not None else basicId[0] if basicId is not None else sap[0] if sap is not None else None

    def __del__(self):
        self.connection.close()

    def close(self):
        self.__del__()

    def createTableISBN_FRONT_BACK(self):
        self.c.execute("""CREATE TABLE stock (ISBN text, front integer, back integer)""")

    def getAllStock(self):
        return self.c.execute("""SELECT * FROM stock""").fetchall()

    def updateItem(self, isbn, criteria, newItem, table='stock'):
        if table == 'stock':
            if not self.c.execute("SELECT 1 FROM stock WHERE isbn=? LIMIT 1", (isbn,)).fetchone():
                # it doesnt exist, cerate new record
                if criteria == 'front':
                    self.c.execute("INSERT INTO stock (isbn, front) VALUES (?, ?)", (isbn, newItem))
                elif criteria == 'back':
                    self.c.execute("INSERT INTO stock (isbn, back) VALUES (?, ?)", (isbn, newItem))
                else:
                    raise Exception
            else:
                if criteria == "front":
                    self.c.execute("UPDATE stock SET front=? WHERE isbn=?", (newItem, isbn))
                elif criteria == 'back':
                    self.c.execute("UPDATE stock SET back=? WHERE isbn=?", (newItem, isbn))
                else:
                    raise Exception
        else:
            raise Exception

    def deleteISBN(self, isbn):
        self.c.execute("DELETE FROM stock WHERE isbn=?", (isbn,))

