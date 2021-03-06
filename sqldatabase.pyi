import sqlite3
from BaseTyping import *

class SQLDatabase:
    openDataBases = [] # type: List[type(sqlite3.connect('1'))]
    def __init__(self, databaseName: str):...
    def getData(self, isbn: str) -> Optional[str]:...
    def getISBN(self, IDorISBN: str) -> Optional[str]:...
    def set_qty(self, isbn: str, front: Optional[int]=None, back: Optional[int]=None) -> None:...
    def getName(self, isbn: str):...
    def __del__(self) -> None:...
    def close(self) -> None:...
    def createTableISBN_FRONT_BACK(self) -> None:...