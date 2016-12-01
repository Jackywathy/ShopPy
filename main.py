import tkinter
from tkinter import ttk
import appdirs
from enum import Enum
from tkinter.constants import *
import tkinter.messagebox

appname = "Product Checker"
appauthor = "Jackywathy24"
import os
os.chdir(appdirs.user_data_dir(appname,appauthor))








picturePath = ...



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
        raise NotImplemented

class MyBarcodePage(MyAppPage):
    def queryDataBase(self, event):
        if self.MainApp.checkSpecialBarcodes(event.widget.get()):
            print(event.widget.get())
            event.widget.doDelete = True
        else:
            barcode = event.widget.get()
            barcode_data = self.database.get_item(barcode)
            if barcode_data is not None:
                print(barcode_data)
                self.set_info(barcode_data)
            else:
                print("NONE")
                self.set_info(None)

    def set_info(self, info):
        raise NotImplemented

    @staticmethod
    def selectAll(event):
        event.widget.selection_range(0,END)



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
        if newimage is None:
            newimage = ""
        print('newimage', newimage)
        self._image = tkinter.PhotoImage(data=newimage)
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
            for i in [self.ItemNameVar, self.ISBNVar, self.authorVar]:
                i.set("None")
            for i in self.frontVar, self.backVar:
                i.set("None")
            self.priceVar.set('None')
        else:
            for var, data in zip([self.ItemNameVar, self.authorVar, self.ISBNVar, self.frontVar, self.backVar, self.priceVar, self.ImageHolder], infoTuple):
                print('setting', var, 'to', data)
                var.set(data)
            self.priceVar.set("$"+self.priceVar.get())

    def SwitchTo(self):
        self.barcodeEntry.focus_set()

    queryDescriptor = {
        'font': (None,12),
    }
    queryData = {
        'font': (None,20),
        'height':2,
        'wraplength':220,
        'width':20
    }
    padStick = {
        'pady':(20,0),
        'sticky':W+E
    }


    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)
        def queryAndSelect(event):
            self.queryDataBase(event)
            self.selectAll(event)

        tkinter.Label(self, text="Barcode").grid(row=0, column=0, columnspan=8)



        barcodeEntry = tkinter.Entry(self, font=("Courier", 20), justify='center')
        barcodeEntry.bind("<Return>", queryAndSelect)
        barcodeEntry.grid(row=1, column=0, columnspan=8, padx=(35,35), pady=(0,35))
        self.barcodeEntry = barcodeEntry
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

            tkinter.Label(authorGrid, text=doubleRow[1], **self.queryDescriptor).grid(**self.padStick,row=iter*2,column=1,padx=(100,0))
            tkinter.Label(authorGrid, textvariable=Vars[1], **self.queryData).grid(**self.padStick,row=iter*2+1, column=1,padx=(100,0))




        authorGrid.pack()

        ImageLabel = tkinter.Label(dataFrame)
        self.ImageHolder = ImageHolderUpdater(ImageLabel)
        ImageLabel.pack(fill=BOTH, expand=1)



        dataFrame.grid(row=2, column=0, columnspan=8, padx=(10,10), pady=(10,10), sticky=N+S+E+W)

        self.set_info(None)
        print("DONES")


import sys
import sqlite3
class SQLDatabase:
    def __init__(self, databaseName):
        self.connection = sqlite3.connect(databaseName)
        self.c = self.connection.cursor()

    def get_item(self, isbn):
        print(type(isbn), print(isbn))
        return self.c.execute("""SELECT * FROM excel WHERE isbn=(?) LIMIT 1""", (isbn,)).fetchone()

    def set_qty(self, isbn, front=None, back=None):
        assert self.c.execute("SELECT 1 FROM excel WHERE isbn=(?) LIMIT 1", (isbn,)).fetchone()
        if front is not None:
            self.c.execute("""UPDATE excel SET
                                  front_qty=(?)
                                  WHERE isbn=(?);""", (front,isbn))
        if back is not None:
            self.c.execute("""UPDATE excel SET
                                  back_qty=(?)
                                  WHERE isbn=(?);""", (back,isbn))



class StockPage(MyAppPage):
    def __init__(self,parent,database,MainApp):
        super().__init__(parent,database,MainApp)
        '''
        setOrAddFrame = tkinter.Frame(self)
        setOrAddLabel = tkinter.Label(setOrAddFrame, text='Set/Increment')
        setOrAddVar = tkinter.StringVar()
        self.setButton = tkinter.Radiobutton(setOrAddFrame, text="Set", variable=setOrAddVar, value='set')
        self.incButton = tkinter.Radiobutton(setOrAddFrame, text="Inc", variable=setOrAddVar,value='inc')
        '''
        barcodeFrame = tkinter.Frame(self)
        barcodeLabel = tkinter.Label(barcodeFrame, text="Barcode")


        entryBarcodeFrame = tkinter.Frame(barcodeFrame)

        # TODO make this work!
        barcodeEntry = tkinter.Entry(entryBarcodeFrame)

        numEntry = tkinter.Entry(entryBarcodeFrame, width=3)

        barcodeEntry.grid(row=0, column=0,columnspan=3)
        numEntry.grid(row=0, column=3, columnspan=1)

        #barcodeEntry.grid(column=0, columnspan=2)
        barcodeLabel.pack()
        entryBarcodeFrame.pack()

        barcodeFrame.pack()







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
        self.notebook.pack()

        self.notebook.bind("<<NotebookTabChanged>>", self.chooseNoteBookTarget)
        import traceback
        def show_error(*args):
            err = traceback.format_exception(*args)
            print(err)
            tkinter.messagebox.showerror('Exception',err)


        self.root.report_callback_exception = show_error



        self.root.mainloop()

    def chooseNoteBookTarget(self, event):
        tab = self.notebook.select()
        if tab == str(self.pages['query']):
            self.pages['query'].SwitchTo()
        elif tab == str(self.pages['insert']):
            self.pages['insert'].SwitchTo()


app = Application()
    #       pass
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