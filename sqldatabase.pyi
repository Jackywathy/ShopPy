import sqlite3
from typing import *
NoneInt = Optional[int]
NoneStr = Optional[str]

class SQLDatabase:
    openDataBases = [] # type: List[type(sqlite3.connect('1'))]
    def __init__(self, databaseName: str):...
    def getIsbn(self, isbn: str) -> NoneStr:...
    def set_qty(self, isbn: str, front: NoneInt=None, back: NoneInt=None) -> None:...
    def getBasicID(self, number: str) -> NoneStr:...