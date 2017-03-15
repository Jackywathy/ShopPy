import tkinter
from tkinter.constants import *
import tkinter.ttk as ttk
from Logger import *
import base64
from io import BytesIO
from PIL import Image, ImageTk

class ImageHolderUpdater:
    errorImage = None
    @property
    def Image(self):
        return self._image
    @Image.setter
    def Image(self, newimage):
        if newimage is None or newimage.lower() == 'none':
            self._image = self.errorImage
        else:
            decoded = Image.open(BytesIO(base64.b64decode(newimage)))
            self._image = ImageTk.PhotoImage(decoded) # keeping eine reference!
        self.Display.configure(image=self._image)

    def __init__(self, Label, image=""):
        self.Display = Label
        self._image = tkinter.PhotoImage(data=image)

    def set(self, data):
        self.Image = data

class MyBarcodePage(tkinter.Frame):
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
    def SwitchTo(self):
        """Set focus on parts on this page when the page is switched to"""
        raise NotImplementedError

    def queryAndSelect(self, event):
        barcode = event.widget.get()
        ret = self.queryDataBase(barcode)
        self.selectAll(event)
        return ret,barcode

    def queryDataBase(self, barcode):
        """Queries the database for the specified string"""
        ret = False
        if self.MainApp.checkSpecialBarcodes(barcode):
            pass
        else:
            ISBN = self.database.getData(barcode)
            # get data in excel&basic&basicID's isbn's
            self.set_info(ISBN)
            LOG("Barcode data is",RemoveImage(ISBN), type(ISBN))
            ret = True if ISBN is not None else False
        LOG("RET is", ret)
        return ret

    def set_info(self, info):
        """Sets the info of the labels that need to be updated"""
        raise NotImplementedError

    @staticmethod
    def selectAll(event):
        """Selects all of the given widgets entry"""
        event.widget.selection_range(0,END)

    @staticmethod
    def containsId(infoTuple):
        """Returns true if provided infoTuple contains ID, e.g. has 8th element"""
        if len(infoTuple) == 8:
            return True
        elif len(infoTuple) == 7:
            return False
        else:
            LOG("ERROR@Resolving containsID", str(infoTuple), str(len(infoTuple)))
            raise Exception

    def __init__(self, parent, database, MainApp):
        super().__init__(parent)
        self.database = database #type: SQLDatabase
        self.MainApp = MainApp

class EmptyVar:
    def set(self, item):
        pass
