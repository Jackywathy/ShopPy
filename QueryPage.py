from AppBase import *


class QueryPage(MyBarcodePage):
    def set_info(self, infoTuple):
        LOG("Setting info for", infoTuple)
        if infoTuple is None:
            LOG("InfoTuple is None")
            for i in self.vars:
                i.set("None")
        else:
            if self.containsId(infoTuple): # if it contains an id!
                id = infoTuple[7]
                LOG("InforTuple contains ID!", id)
                infoTuple = infoTuple[:7]

            for var, data in zip(self.vars, infoTuple):
                var.set(data)
            self.priceVar.set("$"+self.priceVar.get())

    def SwitchTo(self):
        self.barcodeEntry.focus_set()

    def __init__(self, parent, database, MainApp):
        super().__init__(parent, database, MainApp)
        # barcode label
        tkinter.Label(self, text="Barcode").pack()
        # barcode Entry
        self.barcodeEntry = tkinter.Entry(self, font=("Courier", 20), justify='center')
        self.barcodeEntry.bind("<Return>", self.queryAndSelect)
        self.barcodeEntry.pack()
        # item name
        self.ShowBoxText = tkinter.StringVar()
        ShowBoxLabel = tkinter.Label(self,  font=("Helvetica", 16), justify='center', textvariable=self.ShowBoxText)
        ShowBoxLabel.pack()

        # begin the dataFrame
        dataFrame = tkinter.Frame(self,borderwidth=10, highlightbackground='black')


        self.ItemNameVar, self.ISBNVar, self.authorVar = tkinter.StringVar(),tkinter.StringVar(), tkinter.StringVar()
        self.frontVar, self.backVar,self.priceVar = tkinter.StringVar(), tkinter.StringVar(), tkinter.StringVar()


        tkinter.Label(dataFrame, text="Item Name", font = (None,18)).pack()
        tkinter.Label(dataFrame, textvariable=self.ItemNameVar, font=(None,30), wraplength=600, width=40, height=3).pack()

        tkinter.Label(dataFrame, text="RRP", font=(None,18)).pack()
        tkinter.Label(dataFrame, textvariable=self.priceVar, font=(None,25)).pack()



        authorGrid = tkinter.Frame(dataFrame)
        labels = [('Author(s)', 'ISBN'),
                  ('Front QTY', 'Back QTY')]
        labelVars = [(self.authorVar, self.ISBNVar),
                     (self.frontVar, self.backVar)]
        for iter,zipedDoubleRow in enumerate(zip(labels,labelVars)):
            doubleRow, Vars = zipedDoubleRow
            leftFrame  = tkinter.Frame(authorGrid)
            rightFrame = tkinter.Frame(authorGrid)

            # left
            tkinter.Label(leftFrame, text=doubleRow[0], **self.queryDescriptor).pack()
            tkinter.Label(leftFrame, textvariable=Vars[0], **self.queryData).pack()

            # right
            tkinter.Label(rightFrame, text=doubleRow[1], **self.queryDescriptor).pack()
            tkinter.Label(rightFrame, textvariable=Vars[1], **self.queryData).pack()
            print(doubleRow[1])
    
            leftFrame.grid(**self.padStick,row=iter   , column=0, padx=(0,100))
            rightFrame.grid(**self.padStick,row=iter, column=2, padx=(100,0))


        ImageLabel = tkinter.Label(authorGrid, relief=SUNKEN, anchor=CENTER, Image=None, width=300, height=300)
        self.ImageHolder = ImageHolderUpdater(ImageLabel)


        self.vars = [self.ItemNameVar, self.authorVar, self.ISBNVar, self.frontVar, self.backVar, self.priceVar, self.ImageHolder]
        ImageLabel.grid(rowspan=4, row=0, column=1)

        authorGrid.pack()



        dataFrame.pack(padx=(10,10), pady=(10,10))
        # TODO REMOVE
        self.set_info(None)