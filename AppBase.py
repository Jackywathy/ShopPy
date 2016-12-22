import tkinter
from tkinter import ttk as ttk
from tkinter.constants import *
from Logger import *
import base64
from io import BytesIO
from PIL import Image, ImageTk


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
            self.decoded = Image.open(BytesIO(base64.b64decode(newimage)))
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
            barcode_data = self.database.getIsbn(barcode)
            # get data in excel&basic&basicID's isbn's
            self.set_info(barcode_data)
            LOG("Barcode data is",barcode_data, type(barcode_data))
            ret = True if barcode_data is not None else False
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
            LOG("ERROR@Resolving containsID", str(infoTuple), str(len(infoTuple)))
            raise Exception

class EmptyVar:
    def set(self, item):
        pass
