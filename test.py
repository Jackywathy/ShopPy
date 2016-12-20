import tkinter
import tkinter.ttk

root = tkinter.Tk()
treeview = tkinter.ttk.Treeview(root,show='headings',columns=('name','isbn','F'))

x = treeview.insert("",0, text='none',values=('kai','mai','f'))
treeview.insert('',1, values=("jac", '?'))
print(treeview.set(x,value=('louie',)))
treeview.pack()
root.mainloop()
