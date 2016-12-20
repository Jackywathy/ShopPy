import tkinter
from tkinter import ttk
import appdirs
from enum import Enum
from tkinter.constants import *
import tkinter.messagebox
from io import BytesIO
from PIL import Image, ImageTk
import base64
import sqlite3
from collections import defaultdict

appname = "Product Checker"
appauthor = "Jackywathy24"
import os
directory = appdirs.user_data_dir(appname,appauthor)
if not os.path.exists(directory):
    os.mkdir(directory)

print(directory)

class MyAppPage(tkinter.Frame):
    def __init__(self, parent, database, MainApp):
        """
        :type database: SQLDatabase
        :type MainApp: Application
        """

        super().__init__(parent)
        self.database = database
        self.MainApp = MainApp
    def SwitchTo(self):
        raise NotImplementedError

class MyBarcodePage(MyAppPage):
    courier = {
        "font": ("courier", 20)
    }
    queryDescriptor = {
        'font': (None,12),
    }
    queryData = {
        'relief':SUNKEN,
        'font': (None,20),
        'height':2,
        'wraplength':220,
        'width':20
    }
    padStick = {
        'pady':(20,0),
        'sticky':W+E
    }
    superSticky = {
        'sticky':"nsew"
    }

    def queryAndSelect(self, event):
        ret = self.queryDataBase(event)
        self.selectAll(event)
        return ret

    def queryDataBase(self, event):
        ret = False
        if self.MainApp.checkSpecialBarcodes(event.widget.get()):
            pass
        else:
            barcode = event.widget.get()
            barcode_data = self.database.get_item(barcode)
            # get data in excel&basic isbn's
            if barcode_data is None:
                # get data from basic #123's
                barcode_data = self.database.get_basic_number(barcode)
                if barcode_data is not None:
                    self.set_info(barcode_data)
                    ret = True
                else:
                    self.set_info(None)
            else:
                self.set_info(barcode_data)
                ret = True
        return ret

    def set_info(self, info):
        raise NotImplementedError

    @staticmethod
    def selectAll(event):
        event.widget.selection_range(0,END)

    @staticmethod
    def upToThree(event, length=3):
        input = event.widget.get()
        if len(input) > length:
            event.widget.delete(0,END)
            event.widget.insert(0, input[:length])
    @staticmethod
    def containsId(infoTuple):
        if len(infoTuple) == 8:
            return True
        elif len(infoTuple) == 7:
            return False
        else:
            raise Exception(str(infoTuple))

class InsertPage(MyAppPage):
    def SwitchTo(self):
        ...

    def __init__(self, parent, database, MainApp):
        """
        :type database: SQLDatabase
        :type MainApp: Application
        """
        super().__init__(parent, database, MainApp)

        self.label = tkinter.Label(self, text="hi")
        self.label.pack()

class ImageHolderUpdater:
    @property
    def Image(self):
        return self._image
    @Image.setter
    def Image(self, newimage):
        if newimage is None or newimage.lower() == 'none':
            self._image = errorImage
        else:
            self.decoded = Image.open(BytesIO(base64.b64decode(newimage)))
            #self.decoded.show()
            self._image = ImageTk.PhotoImage(self.decoded) # keeping eine reference!
        self.Display.configure(image=self._image)

    def __init__(self, Label, Image=""):
        """
        :type Label: tkinter.Label
        :param data:
        :return:
        """
        self.Display = Label
        self._image = tkinter.PhotoImage(data=Image)

    def set(self, data):
        self.Image = data

class QueryPage(MyBarcodePage):
    def set_info(self, infoTuple):
        if infoTuple is None:
            for i in self.vars:
                i.set("None")
        else:
            if self.containsId(infoTuple): # if it contains an id!
                id = infoTuple[7]
                infoTuple = infoTuple[:7]

                print(id)
            for var, data in zip(self.vars, infoTuple):
                var.set(data)
            self.priceVar.set("$"+self.priceVar.get())

    def SwitchTo(self):
        self.barcodeEntry.focus_set()

    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)
        tkinter.Label(self, text="Barcode").grid(row=0, column=0, columnspan=8)
        entriesFrame = tkinter.Frame(self)
        barcodeEntry = tkinter.Entry(entriesFrame, font=("Courier", 20), justify='center')
        barcodeEntry.bind("<Return>", self.queryAndSelect)
        barcodeEntry.pack(side=LEFT)
        self.barcodeEntry = barcodeEntry
        entriesFrame.grid(row=1,column=0,columnspan=8,pady=(0,35))
        ShowBox = tkinter.Frame(self)
        self.ShowBoxText = tkinter.StringVar()
        ShowBoxLabel = tkinter.Label(ShowBox,  font=("Helvetica", 16), justify='center', textvariable=self.ShowBoxText)
        ShowBoxLabel.pack(pady=(20,30))
        ShowBox.grid(row=2, column=1, columnspan=6)
        # begin the dataFrame
        dataFrame = tkinter.Frame(self,borderwidth=10, highlightbackground='black')
        self.ItemNameVar, self.ISBNVar, self.authorVar = tkinter.StringVar(),tkinter.StringVar(), tkinter.StringVar()
        self.frontVar, self.backVar,self.priceVar = tkinter.StringVar(), tkinter.StringVar(), tkinter.StringVar()


        tkinter.Label(dataFrame, text="Item Name", font = (None,18)).pack()
        tkinter.Label(dataFrame, textvariable=self.ItemNameVar, font=(None,30),wraplength=600, width=40, height=3).pack()

        tkinter.Label(dataFrame, text="RRP", font=(None,18)).pack()
        tkinter.Label(dataFrame, textvariable=self.priceVar, font=(None,25)).pack()



        authorGrid = tkinter.Frame(dataFrame)
        labels = [('Author(s)', 'ISBN'),
                  ('Front QTY', 'Back QTY')]
        labelVars = [(self.authorVar, self.ISBNVar),
                     (self.frontVar, self.backVar)]
        for iter,zipedDoubleRow in enumerate(zip(labels,labelVars)):
            doubleRow, Vars = zipedDoubleRow
            tkinter.Label(authorGrid, text=doubleRow[0], **self.queryDescriptor).grid(**self.padStick,row=iter*2,column=0,padx=(0,100))
            tkinter.Label(authorGrid, textvariable=Vars[0], **self.queryData).grid(**self.padStick,row=iter*2+1, column=0,padx=(0,100))

            tkinter.Label(authorGrid, text=doubleRow[1], **self.queryDescriptor).grid(**self.padStick,row=iter*2,column=2,padx=(100,0))
            tkinter.Label(authorGrid, textvariable=Vars[1], **self.queryData).grid(**self.padStick,row=iter*2+1, column=2,padx=(100,0))


        ImageLabel = tkinter.Label(authorGrid, image=errorImage, width=250,height=300)
        self.ImageHolder = ImageHolderUpdater(ImageLabel)
        self.vars = [self.ItemNameVar, self.authorVar, self.ISBNVar, self.frontVar, self.backVar, self.priceVar, self.ImageHolder]
        ImageLabel.grid(rowspan=4, row=0, column=1)

        authorGrid.pack()



        dataFrame.grid(row=2, column=0, columnspan=8, padx=(10,10), pady=(10,10), sticky=N+S+E+W)

        self.set_info(None)

class SQLDatabase:
    def __init__(self, databaseName):
        self.connection = sqlite3.connect(databaseName)
        self.c = self.connection.cursor()

    def get_item(self, isbn):
        excelResponse = self.c.execute("""SELECT * FROM excel WHERE isbn=(?) LIMIT 1""", (isbn,)).fetchone()
        return excelResponse if excelResponse is not None else self.c.execute("""SELECT * FROM basic WHERE isbn=(?) LIMIT 1""", (isbn,)).fetchone()

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

    def get_basic_number(self, number):
        return self.c.execute("""SELECT * FROM basic WHERE id=(?) LIMIT 1""", (number,)).fetchone()

    def __del__(self):
        self.connection.close()

    def close(self):
        self.__del__()

    def execute(self, string):
        """Allows unsanitized sql code to run!!! please have mercy on our souls and dont do |DROP TABLE excel"""
        assert string is not 'dangerous!!!'
        self.c.execute(string)

    def getName(self, isbn):
        basic = self.c.execute("SELECT title FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        excel = self.c.execute("SELECT title FROM basic WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        basicId = self.c.execute("SELECT title FROM basic WHERE id=(?) LIMIT 1", (isbn,)).fetchone()
        return basic if basic is not None else excel if excel is not None else basicId

class EmptyVar:
    def set(self, item):
        pass

class MyTreeView():
    def __init__(self,treeView, database):
        """
        :type treeView: ttk.TreeView
        :return:
        """
        treeView.heading("#1", text="Name")
        treeView.heading('#2', text='ISBN')
        treeView.heading("#3", text='F')
        treeView.heading("#4", text="B")

        treeView.column("#1", width=200)
        treeView.column('#2', width = 70)
        treeView.column("#3", width=40)
        treeView.column("#4", width=40)
        self.treeView = treeView
        self.isbnToNode = {}
        self.isbnToFront = defaultdict(int)
        self.isbnToBack = defaultdict(int)

        self.realData = database

        self.dataBase = SQLDatabase("stockTemp.db")
        try:
            self.dataBase.execute("""CREATE TABLE stock
                                    (ISBN text, front integer, back integer)""")
        except:
            pass



    def addAmountToTree(self, isbn, front=0,back=0):
        self.isbnToFront[isbn] += front
        self.isbnToBack[isbn] += back
        if isbn not in self.isbnToNode:
            realName = self.realData.getName(isbn)
            self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)
        else:
            # [0] is the reference to treeView, [1] is the name.
            self.treeView.set(self.isbnToNode[isbn][0], value=(self.isbnToNode[isbn][1], isbn, self.isbnToFront[isbn], self.isbnToBack[isbn]))


class StockPage(MyBarcodePage):
    def SwitchTo(self):
        self.barcodeEntry.focus_set()

    def set_info(self, infoTuple):
        if infoTuple is None:
            for i in [self.nameVar, self.authorVar, self.priceVar, self.frontVar, self.backVar, self.totalVar,self.pictureVar]:
                print(type(i))
                i.set(None)

        else:
            if self.containsId(infoTuple):
                id = infoTuple[7]
                infoTuple = infoTuple[:7]
            for var,item in zip(self.vars,infoTuple):
                var.set(item)

            self.totalVar.set(int(self.backVar.get() if self.backVar.get().lower() != 'none' else 0) + int(self.frontVar.get() if self.frontVar.get().lower() != 'none' else 0))

    def createTempDatabase(self, name="inprogress.db"):
        self.inprogress = SQLDatabase(name)

    def queryAndSelect(self, event):
        valid = super().queryAndSelect(event)
        # Also set the extra entry to right amount
        if valid:
            self.myTree.addAmountToTree(event.widget.get(),1,1)


    def __init__(self,parent, database, MainApp):
        super().__init__(parent, database, MainApp)

        tkinter.Label(self, text="Barcode").pack()

        topFrame = tkinter.Frame(self)
        barcodeEntry = tkinter.Entry(topFrame, font=("Courier", 20), justify='center')
        barcodeEntry.bind("<Return>", self.queryAndSelect)
        barcodeEntry.pack(side=LEFT)
        self.barcodeEntry = barcodeEntry

        self.numberOfItemEntry = tkinter.Entry(topFrame, width=3, justify='center', **self.courier)
        self.numberOfItemEntry.pack(side=LEFT)
        topFrame.pack()


        # DATA
        mainFrame = tkinter.Frame(self)

        # left Data
        # variables of the lables that change
        self.nameVar = tkinter.StringVar()
        self.authorVar = tkinter.StringVar()
        self.priceVar = tkinter.StringVar()
        self.frontVar = tkinter.StringVar()
        self.backVar = tkinter.StringVar()
        self.totalVar = tkinter.StringVar()


        # end vars
        leftFrame = tkinter.Frame(mainFrame)
        # itemName
        tkinter.Label(leftFrame,text="Name", **self.queryDescriptor).pack()
        tkinter.Label(leftFrame,textvariable=self.nameVar,width=40,wraplength=400, height=3,relief=SUNKEN, font=(None,20)).pack()
        # authorName
        tkinter.Label(leftFrame,text="Author(s)", **self.queryDescriptor).pack()
        tkinter.Label(leftFrame,textvariable=self.authorVar, **self.queryData).pack()
        # picture and text
        pictureTextFrame = tkinter.Frame(leftFrame)

        pictureLabel = tkinter.Label(pictureTextFrame,relief=SUNKEN)
        self.pictureVar = ImageHolderUpdater(pictureLabel)
        # title, author, isbn, front, back, price, image
        self.vars = [self.nameVar, self.authorVar, EmptyVar(), self.frontVar, self.backVar, self.priceVar, self.pictureVar]

        self.set_info(None)


        pictureLabel.grid(row=0,rowspan=4, column=0, columnspan=2,padx=20,pady=20)
        # make pack all the boxes in correct location
        self.makeBoxedVars(pictureTextFrame)
        pictureTextFrame.pack()


        # right treeview with prev.
        rightFrame = tkinter.Frame(mainFrame)
        self.myTree = MyTreeView(ttk.Treeview(rightFrame, columns=("name", 'isbn','f','b'),show='headings'),self.database)
        self.myTree.treeView.pack(fill=BOTH, expand=True)
        # make the tree



        leftFrame.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        rightFrame.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        mainFrame.pack()




    def makeBoxedVars(self, pictureTextFrame):
        for iter,var_name in enumerate(zip([self.priceVar, self.frontVar, self.backVar,self.totalVar],["Price", "Front", "Back", "Total"])):
            var, name = var_name
            # price, front, back, total
            priceFrame = tkinter.Frame(pictureTextFrame)
            tkinter.Label(priceFrame,text=name, **self.queryDescriptor).pack()
            tkinter.Label(priceFrame,textvariable=var, **self.queryData).pack()
            priceFrame.grid(row=iter,column=2)










import sys
class Application:

    SpecialBarcodes = {
        "?":"query"
    }

    def checkSpecialBarcodes(self, text):
        if text in Application.SpecialBarcodes:
            if Application.SpecialBarcodes[text] == 'query':
                self.pages['query'].SwitchTo()

    def destroySelf(self, event):
        self.root.quit()
        sys.exit()

    def __init__(self):
        self.database = SQLDatabase("database.db")
        self.root = tkinter.Tk()
        global errorImage
        errorImage = ImageTk.PhotoImage(Image.open("errorcross.png"))


        #self.root.attributes("-fullscreen", True)


        self.root.bind("<Alt-F4>", lambda x: self.destroySelf(x))

        self.notebook = ttk.Notebook(self.root)

        self.pages = {
            "query":QueryPage(self.notebook, self.database, self),
            "insert":InsertPage(self.notebook, self.database, self),
            "stock":StockPage(self.notebook, self.database, self)
        }


        self.notebook.add(self.pages['query'], text='Query')
        self.notebook.add(self.pages['insert'], text='Insert')
        self.notebook.add(self.pages['stock'], text='Stock')
        self.notebook.pack(pady=20,padx=20)

        self.notebook.bind("<<NotebookTabChanged>>", self.chooseNoteBookTarget)
        import traceback
        def show_error(*args):
            err = traceback.format_exception(*args)
            print(''.join(err))
            tkinter.messagebox.showerror('Exception',err)


        self.root.report_callback_exception = show_error



        self.root.mainloop()

    def chooseNoteBookTarget(self, event):
        tab = event.widget.select()
        if tab == str(self.pages['query']):
            self.pages['query'].SwitchTo()
        elif tab == str(self.pages['insert']):
            self.pages['insert'].SwitchTo()
        elif tab == str(self.pages['stock']):
            self.pages['stock'].SwitchTo()

app = Application()

'''

import GoogleScraper
config = {
    'keyword': 'beautiful landscape', # :D hehe have fun my dear friends
    'search_engines': ['google'],
    'search_type': 'image',
    'scrape_method': 'selenium',
    'do_caching': True,
}
search = GoogleScraper.scrape_with_config(config)
image_urls = []
import google
for serp in search.serps:
    image_urls.extend(
        [link.link for link in serp.links]
    )
    '''