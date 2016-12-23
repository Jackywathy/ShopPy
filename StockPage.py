from AppBase import *
from MyTreeView import *

class StockPage(MyBarcodePage):
    def SwitchTo(self):
        """Set focus on parts on this page when the page is switched to"""
        self.barcodeEntry.focus_set()

    def set_info(self, infoTuple):
        """Sets the info of the variables on this page using a 7-8 length infoTuple"""
        LOG("SETTING vars to", infoTuple)
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

    def updateNoEntry(self, ISBN):
        currB = self.button_select.get()
        if currB == K_FRONT:
            self.myTree.addAmountToTree(ISBN, front=1)
            self.numberOfItemEntry.delete(0, END)
            self.numberOfItemEntry.insert(0,self.myTree.isbnToFront[ISBN])
        elif currB == K_BACK:
            self.myTree.addAmountToTree(ISBN, back=1)
            self.numberOfItemEntry.delete(0, END)
            self.numberOfItemEntry.insert(0,self.myTree.isbnToBack[ISBN])
        else:
            raise Exception




    def queryAndSelect(self, event):
        valid = super().queryAndSelect(event)
        # Also set the extra entry to right amount
        if valid[0]:
            ISBN = self.database.getISBN(valid[1])
            self.updateNoEntry(ISBN)
            # update the entry
            self.myTree.selectISBN(ISBN)

        return valid

    def setTreeViewFromNumberEntry(self, event):
        if self.button_select.get() == K_FRONT:
            self.myTree.setItemInTree(self.database.getISBN(self.barcodeEntry.get()), front=self.numberOfItemEntry.get())
        elif self.button_select.get() == K_BACK:
            self.myTree.setItemInTree(self.database.getISBN(self.barcodeEntry.get()), back=self.numberOfItemEntry.get())
        else:
            raise Exception
    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)

        tkinter.Label(self, text="Barcode").pack()

        topFrame = tkinter.Frame(self)
        barcodeEntry = tkinter.Entry(topFrame, font=("Courier", 20), justify='center')
        barcodeEntry.bind("<Return>", self.queryAndSelect)
        barcodeEntry.pack(side=LEFT)
        self.barcodeEntry = barcodeEntry

        self.numberOfItemEntry = tkinter.Entry(topFrame, width=3, justify='center', **self.courier)
        self.numberOfItemEntry.pack(side=LEFT)
        self.numberOfItemEntry.bind("<Return>", self.setTreeViewFromNumberEntry)


        self.button_select = tkinter.StringVar()

        self.F_Button = tkinter.Radiobutton(topFrame, text="Front", value=K_FRONT, variable=self.button_select) # type: tkinter.Radiobutton
        self.B_Button = tkinter.Radiobutton(topFrame, text="Back", value=K_BACK, variable=self.button_select)   # type: tkinter.Radiobutton
        self.F_Button.select()
        self.F_Button.pack(side=LEFT); self.B_Button.pack(side=LEFT)

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

        pictureLabel = tkinter.Label(pictureTextFrame,relief=SUNKEN, anchor=CENTER, width=300, height=300, image=None)
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
        tkinter.Button(rightFrame, text='Delete',command=self.deleteSelected).pack()




        leftFrame.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        rightFrame.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        mainFrame.pack()

    def deleteSelected(self):
        self.myTree.resetISBN()

    def makeBoxedVars(self, pictureTextFrame):
        for iter,var_name in enumerate(zip([self.priceVar, self.frontVar, self.backVar,self.totalVar],["Price", "Front", "Back", "Total"])):
            var, name = var_name
            # price, front, back, total
            priceFrame = tkinter.Frame(pictureTextFrame)
            tkinter.Label(priceFrame,text=name, **self.queryDescriptor).pack()
            tkinter.Label(priceFrame,textvariable=var, **self.queryData).pack()
            priceFrame.grid(row=iter,column=2)
