import openpyxl
import pickle
try:
    database = pickle.load(open("data.pkl", 'rb'))
except:
    raise Exception()
wb = openpyxl.load_workbook('seed.xlsx')
ws = next(iter(wb))
for i in ws:
    if (str(i[3].value)) in database:
        print(i[1].value, i[3].value, i[4].value)
        #print(i[5], type(i[5]), i[5].value, type(i[5].value))
        i[5].value = database[str(i[3].value)]

wb.save("out.xlsx")
