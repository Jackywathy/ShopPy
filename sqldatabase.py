import sqlite3
import constants

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
        assert table in constants.K_TABLES
        assert criteria in constants.K_COLUMNS
        # stop them cheeky sql injections :D (hopefully)

        if not self.c.execute("SELECT 1 FROM %s WHERE isbn=? LIMIT 1" % table, (isbn,)).fetchone():
            # it doesnt exist, cerate new record
            self.c.execute("INSERT INTO %s (isbn, %s) VALUES (?, ?)" % (table, criteria), (isbn, newItem))
        else:
            self.c.execute("UPDATE %s SET %s=? WHERE isbn=?" % (table, criteria), (newItem, isbn))


    def deleteISBN(self, isbn):
        self.c.execute("DELETE FROM stock WHERE isbn=?", (isbn,))

    def getTable(self, isbn):
        basic = self.c.execute("SELECT title FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        excel = self.c.execute("SELECT title FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        basicId = self.c.execute("SELECT title FROM basic WHERE id=(?) LIMIT 1", (isbn,)).fetchone()
        sap = self.c.execute("SELECT title FROM sap   WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        return 'basic' if basic else 'excel' if excel else 'basic' if basicId else sap

