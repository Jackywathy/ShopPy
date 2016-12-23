from typing import *
from collections import defaultdict
from sqldatabase import *
import tkinter.ttk as ttk

class MyTreeView:
    def __init__(self, treeView: ttk.Treeview, database: SQLDatabase):...
    def addAmountToTree(self, isbn:str, front:int = 0, back: int = 0):...
