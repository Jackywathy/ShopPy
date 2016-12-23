from AppBase import *


class QueryPage(MyBarcodePage):
    def set_info(self, infoTuple):
        print(infoTuple, type(infoTuple))
        if infoTuple is None:
            for i in self.vars:
                i.set("None")
        else:
            if self.containsId(infoTuple): # if it contains an id!
                id = infoTuple[7]
                infoTuple = infoTuple[:7]

            for var, data in zip(self.vars, infoTuple):
                var.set(data)
            self.priceVar.set("$"+self.priceVar.get())

    def SwitchTo(self):
        self.barcodeEntry.focus_set()

    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)
        tkinter.Label(self, text="Barcode").grid(row=0, column=0, columnspan=8)
        entriesFrame = tkinter.Frame(self)
        barcodeEntry = tkinter.Entry(entriesFrame, font=("Courier", 20), justify='center')
        barcodeEntry.bind("<Return>", self.queryAndSelect)
        barcodeEntry.pack(side=LEFT)
        self.barcodeEntry = barcodeEntry
        entriesFrame.grid(row=1,column=0,columnspan=8,pady=(0,35))
        ShowBox = tkinter.Frame(self)
        self.ShowBoxText = tkinter.StringVar()
        ShowBoxLabel = tkinter.Label(ShowBox,  font=("Helvetica", 16), justify='center', textvariable=self.ShowBoxText)
        ShowBoxLabel.pack(pady=(20,30))
        ShowBox.grid(row=2, column=1, columnspan=6)
        # begin the dataFrame
        dataFrame = tkinter.Frame(self,borderwidth=10, highlightbackground='black')
        self.ItemNameVar, self.ISBNVar, self.authorVar = tkinter.StringVar(),tkinter.StringVar(), tkinter.StringVar()
        self.frontVar, self.backVar,self.priceVar = tkinter.StringVar(), tkinter.StringVar(), tkinter.StringVar()


        tkinter.Label(dataFrame, text="Item Name", font = (None,18)).pack()
        tkinter.Label(dataFrame, textvariable=self.ItemNameVar, font=(None,30),wraplength=600, width=40, height=3).pack()

        tkinter.Label(dataFrame, text="RRP", font=(None,18)).pack()
        tkinter.Label(dataFrame, textvariable=self.priceVar, font=(None,25)).pack()



        authorGrid = tkinter.Frame(dataFrame)
        labels = [('Author(s)', 'ISBN'),
                  ('Front QTY', 'Back QTY')]
        labelVars = [(self.authorVar, self.ISBNVar),
                     (self.frontVar, self.backVar)]
        for iter,zipedDoubleRow in enumerate(zip(labels,labelVars)):
            doubleRow, Vars = zipedDoubleRow
            tkinter.Label(authorGrid, text=doubleRow[0], **self.queryDescriptor).grid(**self.padStick,row=iter*2,column=0,padx=(0,100))
            tkinter.Label(authorGrid, textvariable=Vars[0], **self.queryData).grid(**self.padStick,row=iter*2+1, column=0,padx=(0,100))

            tkinter.Label(authorGrid, text=doubleRow[1], **self.queryDescriptor).grid(**self.padStick,row=iter*2,column=2,padx=(100,0))
            tkinter.Label(authorGrid, textvariable=Vars[1], **self.queryData).grid(**self.padStick,row=iter*2+1, column=2,padx=(100,0))


        ImageLabel = tkinter.Label(authorGrid, relief=SUNKEN, anchor=CENTER, Image=None, width=300, height=300)
        self.ImageHolder = ImageHolderUpdater(ImageLabel)


        self.vars = [self.ItemNameVar, self.authorVar, self.ISBNVar, self.frontVar, self.backVar, self.priceVar, self.ImageHolder]
        ImageLabel.grid(rowspan=4, row=0, column=1)

        authorGrid.pack()



        dataFrame.grid(row=2, column=0, columnspan=8, padx=(10,10), pady=(10,10), sticky=N+S+E+W)

        self.set_info(None)