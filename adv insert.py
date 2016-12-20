import sqlite3

conn = sqlite3.connect("stock_data.db")
c = conn.cursor()


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
