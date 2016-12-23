from AppBase import *

class InsertPage(MyBarcodePage):
    def SwitchTo(self):
        ...

    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)

        self.label = tkinter.Label(self, text="hi")
        self.label.pack()