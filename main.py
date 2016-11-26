from tkinter import *
import appdirs
from enum import Enum

appname = "Product Checker"
appauthor = "Jackywathy24"
appdirs.user_data_dir(appname,appauthor)








picturePath = ...


class Product:
    def __init__(self, price, barcodenum, path=None):
        ...

class MyAppPage(Frame):
    def __init__(self, parent, database, MainApp):
        super().__init__(parent)
        self.database = database
        self.MainApp = MainApp
    def SwitchTo(self):
        for page in self.MainApp.pages.values():
            page.pack_forget()




class InsertPage(MyAppPage):
    def SwitchTo(self):
        super().SwitchTo()
        self.pack()

    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)

        self.label = Label(self, text="hi")
        self.label.pack()


class QueryPage(MyAppPage):
    def SwitchTo(self):
        super().SwitchTo()
        self.pack()
        self.barcodeEntry.focus_set()

    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)

        def queryDataBase(event, self):
            if not MainApp.checkSpecialBarcodes(event):
                print(event.widget.get())
                event.widget.doDelete = True
            else:
                barcode = event.widget.get()
                if barcode in self.database:
                    currentProduct = self.database[barcode]

        def checkDelete(event):
            if event.widget.doDelete:
                event.widget.doDelete = False
                event.widget.delete(0, END)

        x = Label(self)
        x.grid(row=0, column=0, columnspan=8)

        barcodeEntry = Entry(self, font=("Courier", 20), justify='center')
        barcodeEntry.doDelete = False
        barcodeEntry.bind("<Return>", lambda ev: ev, self)
        barcodeEntry.bind("<Key>", checkDelete)
        barcodeEntry.grid(row=1, column=3, columnspan=4, padx=(35,35), pady=(0,35))
        self.barcodeEntry = barcodeEntry
        ShowBox = Frame(self)
        self.ShowBoxText = StringVar()
        self.ShowBoxText.set("name")
        ShowBoxLabel = Label(ShowBox,  font=("Helvetica", 16), justify='center', textvariable=self.ShowBoxText)
        ShowBoxLabel.pack(pady=(20,30))

        ShowBox.grid(row=2, column=1, columnspan=6)


import sys

class Application:
    SpecialBarcodes = {
        "?":"query"
    }

    def checkSpecialBarcodes(self, event):
        text = event.widget.get()
        if text in Application.SpecialBarcodes:
            if Application.SpecialBarcodes[text] == 'query':
                self.pages['query'].SwitchTo()

    def destroySelf(self, event):
        self.root.quit()
        sys.exit()

    def __init__(self):
        self.database = {}  # type: {}[str: Product]
        self.root = Tk()
        #self.root.attributes("-fullscreen", True)


        self.root.bind("<Alt-F4>", lambda x: self.destroySelf(x))

        self.pages = {
            "query":QueryPage(self.root, self.database, self),
            "insert":InsertPage(self.root, self.database, self)
        }

        self.pages['query'].SwitchTo()
        #self.pages['insert'].SwitchTo()





        self.root.mainloop()



app = Application()


