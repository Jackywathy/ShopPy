from AppBase import *
from Logger import *
from collections import defaultdict
from sqldatabase import *

class MyTreeView():
    def __init__(self, treeView, database):
        LOG("Creating TreeView")
        treeView.heading("#1", text="Name")
        treeView.heading('#2', text='ISBN')
        treeView.heading("#3", text='F')
        treeView.heading("#4", text="B")

        self.col1 = treeView.column("#1", width= 300)
        self.col2 = treeView.column('#2', width = 70)
        self.col3 = treeView.column("#3", width=40)
        self.col4 = treeView.column("#4", width=40)
        self.treeView = treeView
        self.isbnToNode = {}
        self.isbnToFront = defaultdict(int)
        self.isbnToBack = defaultdict(int)
        self.allCols = self.col1, self.col2, self.col3, self.col4

        self.realData = database

        self.dataBase = SQLDatabase("stockTemp.db")

        try:
            self.dataBase.execute("""CREATE TABLE stock
                                    (ISBN text, front integer, back integer)""")
        except:
            pass


    def addAmountToTree(self, isbn, front=0,back=0):
        LOG("Adding %d to front and %d to back, itemNo: %s" % (front,back, isbn))
        self.isbnToFront[isbn] += front
        self.isbnToBack[isbn] += back
        LOG("All ISBN's: front %s, back %s" % (self.isbnToFront, self.isbnToBack))
        if isbn not in self.isbnToNode:
            realName = self.realData.getName(isbn)[0]
            LOG("New Node, ISBN: %s, Name: %s" % (isbn, realName))
            self.isbnToNode[isbn] = (self.treeView.insert("",0,values=(realName, isbn, self.isbnToFront[isbn], self.isbnToBack[isbn])), realName)

        else:
            # [0] is the reference to treeView, [1] is the name.
            LOG("Updating Line:")
            LOG(self.treeView.item(self.isbnToNode[isbn][0]))
            LOG("TO")
            LOG({'name':self.isbnToNode[isbn][1], 'isbn':isbn, 'front':self.isbnToFront[isbn], 'back':self.isbnToBack[isbn]})
            self.treeView.set(self.isbnToNode[isbn][0], column='#4', value=self.isbnToBack[isbn])
            self.treeView.set(self.isbnToNode[isbn][0], column='#3', value=self.isbnToFront[isbn])

class StockPage(MyBarcodePage):
    def SwitchTo(self):
        self.barcodeEntry.focus_set()

    def set_info(self, infoTuple):
        if infoTuple is None:
            for i in [self.nameVar, self.authorVar, self.priceVar, self.frontVar, self.backVar, self.totalVar,self.pictureVar]:
                i.set(None)

        else:
            if self.containsId(infoTuple):
                id = infoTuple[7]
                infoTuple = infoTuple[:7]
            for var,item in zip(self.vars,infoTuple):
                var.set(item)

            self.totalVar.set(int(self.backVar.get() if self.backVar.get().lower() != 'none' else 0) + int(self.frontVar.get() if self.frontVar.get().lower() != 'none' else 0))

    def createTempDatabase(self, name="inprogress.db"):
        self.inprogress = SQLDatabase(name)

    def queryAndSelect(self, event):
        valid = super().queryAndSelect(event)
        # Also set the extra entry to right amount

        if valid:
            self.myTree.addAmountToTree(event.widget.get(),1)


    def __init__(self,parent, database, MainApp):
        super().__init__(parent, database, MainApp)

        tkinter.Label(self, text="Barcode").pack()

        topFrame = tkinter.Frame(self)
        barcodeEntry = tkinter.Entry(topFrame, font=("Courier", 20), justify='center')
        barcodeEntry.bind("<Return>", self.queryAndSelect)
        barcodeEntry.pack(side=LEFT)
        self.barcodeEntry = barcodeEntry

        self.numberOfItemEntry = tkinter.Entry(topFrame, width=3, justify='center', **self.courier)
        self.numberOfItemEntry.pack(side=LEFT)
        topFrame.pack()


        # DATA
        mainFrame = tkinter.Frame(self)

        # left Data
        # variables of the lables that change
        self.nameVar = tkinter.StringVar()
        self.authorVar = tkinter.StringVar()
        self.priceVar = tkinter.StringVar()
        self.frontVar = tkinter.StringVar()
        self.backVar = tkinter.StringVar()
        self.totalVar = tkinter.StringVar()


        # end vars
        leftFrame = tkinter.Frame(mainFrame)
        # itemName
        tkinter.Label(leftFrame,text="Name", **self.queryDescriptor).pack()
        tkinter.Label(leftFrame,textvariable=self.nameVar,width=40,wraplength=400, height=3,relief=SUNKEN, font=(None,20)).pack()
        # authorName
        tkinter.Label(leftFrame,text="Author(s)", **self.queryDescriptor).pack()
        tkinter.Label(leftFrame,textvariable=self.authorVar, **self.queryData).pack()
        # picture and text
        pictureTextFrame = tkinter.Frame(leftFrame)

        pictureLabel = tkinter.Label(pictureTextFrame,relief=SUNKEN)
        self.pictureVar = ImageHolderUpdater(pictureLabel)
        # title, author, isbn, front, back, price, image
        self.vars = [self.nameVar, self.authorVar, EmptyVar(), self.frontVar, self.backVar, self.priceVar, self.pictureVar]

        self.set_info(None)


        pictureLabel.grid(row=0,rowspan=4, column=0, columnspan=2,padx=20,pady=20)
        # make pack all the boxes in correct location
        self.makeBoxedVars(pictureTextFrame)
        pictureTextFrame.pack()


        # right treeview with prev.
        rightFrame = tkinter.Frame(mainFrame)
        self.myTree = MyTreeView(ttk.Treeview(rightFrame, columns=("name", 'isbn','f','b'),show='headings'),self.database)
        self.myTree.treeView.pack(fill=BOTH, expand=True)
        # make the tree
        tkinter.Button(rightFrame, text='eyy',command=lambda :print(self.myTree.treeView.item(self.myTree.treeView.selection()))).pack()




        leftFrame.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        rightFrame.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        mainFrame.pack()




    def makeBoxedVars(self, pictureTextFrame):
        for iter,var_name in enumerate(zip([self.priceVar, self.frontVar, self.backVar,self.totalVar],["Price", "Front", "Back", "Total"])):
            var, name = var_name
            # price, front, back, total
            priceFrame = tkinter.Frame(pictureTextFrame)
            tkinter.Label(priceFrame,text=name, **self.queryDescriptor).pack()
            tkinter.Label(priceFrame,textvariable=var, **self.queryData).pack()
            priceFrame.grid(row=iter,column=2)
