from sqldatabase import *
from Logger import *
from tkinter.constants import *
from collections import defaultdict
from constants import *
import tkinter.ttk as ttk

class MyTreeView:
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
        self.treeView = treeView # type: ttk.Treeview
        self.isbnToNode = {} # isbn: tuple([0] is the reference to treeView, [1] is the name of book)
        self.isbnToFront = defaultdict(int)
        self.isbnToBack = defaultdict(int)

        self.master_database = database

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
            LOG("Adding line:", line, "to tree")
            self.addAmountToTree(*line)

    def UpdateDataBase(self, isbn):
        """Updates the isbn given from internal dictionary to the sqldatabase"""
        self.dataBase.updateItem(isbn, 'front', self.isbnToFront[isbn])
        self.dataBase.updateItem(isbn, 'back', self.isbnToBack[isbn])

    def addAmountToTree(self, isbn, front=0,back=0):
        LOG("Adding %d to front and %d to back, itemNo: %s" % (front,back, isbn))
        self.isbnToFront[isbn] += front
        self.isbnToBack[isbn] += back
        LOG("All ISBN's: front %s, back %s" % (self.isbnToFront, self.isbnToBack))
        if isbn not in self.isbnToNode:
            realName = self.master_database.getName(isbn)
            LOG("New Node, ISBN: %s, Name: %s" % (isbn, realName))
            self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
            self.UpdateDataBase(isbn)

        else:
            # [0] is the reference to treeView, [1] is the name.
            LOG("Updating line", self.treeView.item(self.isbnToNode[isbn][0]), "to", {'name':self.isbnToNode[isbn][1], 'isbn':isbn, 'front':self.isbnToFront[isbn], 'back':self.isbnToBack[isbn]})
            self.treeView.set(self.isbnToNode[isbn][0], column='#4', value=self.isbnToBack[isbn])
            self.treeView.set(self.isbnToNode[isbn][0], column='#3', value=self.isbnToFront[isbn])
            self.UpdateDataBase(isbn)

    def setItemInTree(self, isbn, front=None, back=None):
        """sets the isbn front to front and isbn back to back"""
        if front is not None:
            self.isbnToFront[isbn] = front
            if isbn not in self.isbnToNode:
                realName = self.master_database.getName(isbn)
                self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
            else:
                self.treeView.set(self.isbnToNode[isbn][0], column='#3', value=self.isbnToFront[isbn])


        if back is not None:
            self.isbnToBack[isbn] = back
            if isbn not in self.isbnToNode:
                realName = self.master_database.getName(isbn)
                self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
            else:
                self.treeView.set(self.isbnToNode[isbn][0], column='#4', value=self.isbnToBack[isbn])

        self.UpdateDataBase(isbn)

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

    def deleteItem(self, isbn):
        # treeview, databae, dictionarys
        self.treeView.delete(self.isbnToNode[isbn][0])
        self.dataBase.deleteISBN(isbn)
        del self.isbnToBack[isbn]
        del self.isbnToFront[isbn]
        del self.isbnToNode[isbn]

    def __iter__(self):
        return iter(self.dataBase.getAllStock())







