import appdirs
import tkinter.messagebox
import traceback
from constants import *
import sys
import os


from InsertPage import *
from StockPage import *
from QueryPage import *



SetLog("stderr.txt")


appname = "Product Checker"
appauthor = "Jackywathy24"
directory = appdirs.user_data_dir(appname,appauthor)
if not os.path.exists(directory):
    os.makedirs(directory)


class Application:
    SpecialBarcodes = {
        "?":"query"
    }
    def checkSpecialBarcodes(self, text):
        if text in Application.SpecialBarcodes:
            if Application.SpecialBarcodes[text] == 'query':
                self.pages['query'].SwitchTo()
                return True
        return False

    def destroySelf(self, *args):
        self.root.quit()
        sys.exit()

    def __init__(self, fullscreen=False):
        LOG("Starting Application")
        self.database = SQLDatabase("database.db")
        LOG("Database")
        self.root = tkinter.Tk()
        ImageHolderUpdater.errorImage = ImageTk.PhotoImage(Image.open(K_ERRORIMAGE))

        if fullscreen:
            self.root.attributes("-fullscreen", True)
            LOG("Starting in Fullscreen")
        else:
            LOG("Starting in Normal mode")


        LOG("Creating the notebook")
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


        LOG("Binding!")
        self.root.bind("<Alt-F4>", lambda x: self.destroySelf(x))
        self.notebook.bind("<<NotebookTabChanged>>", self.chooseNoteBookTarget)
        def show_error(*args):
            err = traceback.format_exception(*args)
            print(''.join(err))
            tkinter.messagebox.showerror('Exception',err)
        self.root.report_callback_exception = show_error

        LOG("Beginning Loop")
        self.root.mainloop()

    def chooseNoteBookTarget(self, event):
        tab = event.widget.select()
        if tab == str(self.pages['query']):
            self.pages['query'].SwitchTo()
        elif tab == str(self.pages['insert']):
            self.pages['insert'].SwitchTo()
        elif tab == str(self.pages['stock']):
            self.pages['stock'].SwitchTo()

if __name__ == "__main__":
    try:
        app = Application()
    finally:
        for i in SQLDatabase.openDataBases:
            i.commit(); i.close()
        LOG("Exiting!")
        LogExit()
