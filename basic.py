import pickle
from collections import defaultdict
database = defaultdict(int)
#import openpyxl
#from google import *
try:
    with open("data.pkl", 'rb') as f:
        database = pickle.load(f)
except:
    print("A")



x = input("Enter Barcode: ")
prev = None
while x:
    if len(x) <= 2:
        if prev is not None:
            database[prev] += int(x)-1
            assert (int(x)-1)>1
    else:
        database[x] += 1

    prev = x
    pickle.dump(database, open('data.pkl', 'wb'))
    x = input("Enter Barcode or number of prev. Barcode: ")
print(database)
