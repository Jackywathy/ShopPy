from AppBase import *
from Logger import *

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