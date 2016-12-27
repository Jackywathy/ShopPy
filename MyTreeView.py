from sqldatabase import *
from Logger import *
from tkinter.constants import *
from collections import defaultdict
from constants import *


class MyTreeView():
    def __init__(self, treeView, database):
        LOG("Creating TreeView")
        treeView.heading("#1", text="Name")
        treeView.heading('#2', text='ISBN')
        treeView.heading("#3", text='F')
        treeView.heading("#4", text="B")

        treeView.column("#1", width=450)
        treeView.column('#2', width=100)
        treeView.column("#3", width=50, anchor=CENTER)
        treeView.column("#4", width=50, anchor=CENTER)
        self.treeView = treeView
        self.isbnToNode = {}
        self.isbnToFront = defaultdict(int)
        self.isbnToBack = defaultdict(int)

        self.mainDataBase = database

        self.dataBase = SQLDatabase("stockTemp.db")

        try:
            self.dataBase.createTableISBN_FRONT_BACK()
        except sqlite3.OperationalError:
            # table already exists
            pass
        # import the database
        self.ImportDataBase()

    def ImportDataBase(self):
        for line in self.dataBase.getAllStock():
            print(line)
            self.addAmountToTree(*line)

    def updateDataBase(self, isbn):
        self.dataBase.updateItem(isbn, 'front', self.isbnToFront[isbn])
        self.dataBase.updateItem(isbn, 'back', self.isbnToBack[isbn])

    def addAmountToTree(self, isbn, front=0,back=0):
        LOG("Adding %d to front and %d to back, itemNo: %s" % (front,back, isbn))
        self.isbnToFront[isbn] += front
        self.isbnToBack[isbn] += back
        LOG("All ISBN's: front %s, back %s" % (self.isbnToFront, self.isbnToBack))
        if isbn not in self.isbnToNode:
            realName = self.mainDataBase.getName(isbn)
            LOG("New Node, ISBN: %s, Name: %s" % (isbn, realName))
            self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
            self.updateDataBase(isbn)

        else:
            # [0] is the reference to treeView, [1] is the name.
            LOG("Updating Line:")
            LOG(self.treeView.item(self.isbnToNode[isbn][0]))
            LOG("TO")
            LOG({'name':self.isbnToNode[isbn][1], 'isbn':isbn, 'front':self.isbnToFront[isbn], 'back':self.isbnToBack[isbn]})
            self.treeView.set(self.isbnToNode[isbn][0], column='#4', value=self.isbnToBack[isbn])
            self.treeView.set(self.isbnToNode[isbn][0], column='#3', value=self.isbnToFront[isbn])
            self.updateDataBase(isbn)

    def setItemInTree(self, isbn, front=None, back=None):
        if front is not None:
            self.isbnToFront[isbn] = front
            if isbn not in self.isbnToNode:
                realName = self.mainDataBase.getName(isbn)
                self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
            else:
                self.treeView.set(self.isbnToNode[isbn][0], column='#3', value=self.isbnToFront[isbn])

        if back is not None:
            if isbn not in self.isbnToNode:
                realName = self.mainDataBase.getName(isbn)
                self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
            else:
                self.treeView.set(self.isbnToNode[isbn][0], column='#4', value=self.isbnToBack[isbn])

    def selectISBN(self, ISBN):
        self.treeView.selection_set(self.isbnToNode[ISBN][0])

    def resetISBN(self):
        for i in self.treeView.selection():
            barcode = str(self.treeView.item(i)['values'][K_BARCODE_INDEX])
            # delete the thing in the treeview
            self.treeView.delete(i)
            # delete out of all dicts
            print(self.isbnToBack)
            del self.isbnToBack[barcode]
            del self.isbnToNode[barcode]
            del self.isbnToFront[barcode]
            # delete from database
            self.dataBase.deleteISBN(barcode)




