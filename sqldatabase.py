import sqlite3


class SQLDatabase:
    openDataBases = []
    def __init__(self, databaseName):
        self.connection = sqlite3.connect(databaseName)
        self.c = self.connection.cursor()
        self.openDataBases.append(self.connection)

    def getIsbn(self, isbn):
        basic = self.c.execute("SELECT * FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        excel = self.c.execute("SELECT * FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        basicId = self.c.execute("SELECT * FROM basic WHERE id=(?) LIMIT 1", (isbn,)).fetchone()
        return basic if basic is not None else excel if excel is not None else basicId

    def getBasicID(self, number):
        return self.c.execute("""SELECT * FROM basic WHERE id=(?) LIMIT 1""", (number,)).fetchone()



    def set_qty(self, isbn, front=None, back=None):
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
        basic = self.c.execute("SELECT title FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        excel = self.c.execute("SELECT title FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        basicId = self.c.execute("SELECT title FROM basic WHERE id=(?) LIMIT 1", (isbn,)).fetchone()
        return basic if basic is not None else excel if excel is not None else basicId

    def __del__(self):
        self.connection.close()

    def close(self):
        self.__del__()

    def execute(self, string):
        """Allows unsanitized sql code to run!!! please have mercy on our souls and dont do |DROP TABLE excel"""
        assert "drop" not in string.lower()
        assert string is not 'dangerous!!!'
        self.c.execute(string)
