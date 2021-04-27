import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from funktions import *


class UserInterface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('LEGO SETs')
        self.root.geometry('900x400')

        ############### FRAMES ##############
        self.topTapFrame = Frame(self.root, borderwidth=1)
        self.topTapFrame.grid(row=0, column=0)

        self.treeFrame = Frame(self.root)
        self.treeFrame.grid(row=1, column=0)

        self.rightFrame = Frame(self.root)
        self.rightFrame.grid(row=1, column=1, sticky=N, pady=20)

        self.footerFrame = Frame(self.root)
        self.footerFrame.grid(row=2, pady=5)

        ############# HEADLINE ##############
        self.headline = Label(self.topTapFrame, text="HEADLINE")
        self.headline.pack()

        ############ BUTTONS ###########
        self.testButton = Button(self.rightFrame, text="HINZU", width=18, pady=8, command=self.add_record)
        self.testButton.grid(row=0)

        self.testButton = Button(self.rightFrame, text="DELETE", width=18, pady=8)
        self.testButton.grid(row=1, pady=5)

        self.testButton = Button(self.rightFrame, text="DETAILS", width=18, pady=8, command=self.open_details)
        self.testButton.grid(row=2)

        self.testButton = Button(self.rightFrame, text="STATISTIC", width=18, pady=8, command=self.open_stats)
        self.testButton.grid(row=3, pady=5)

        ############ TREEVIEW #############
        self.tree = ttk.Treeview(self.treeFrame)
        self.tree.pack(pady=20, padx=20)

        self.tree['columns'] = ("ID", "NAME", "THEME", "RETAIL", "COST", "RELEASE", "DATE")

        self.tree.column("#0", width=0, stretch=NO)  # first column
        self.tree.column("ID", anchor=CENTER, width=120, minwidth=25)
        self.tree.column("NAME", anchor=CENTER, width=80, minwidth=25)
        self.tree.column("THEME", anchor=CENTER, width=124, minwidth=25)
        self.tree.column("RETAIL", anchor=CENTER, width=60, minwidth=25)
        self.tree.column("COST", anchor=CENTER, width=60, minwidth=25)
        self.tree.column("RELEASE", anchor=CENTER, width=80, minwidth=25)
        self.tree.column("DATE", anchor=CENTER, width=90, minwidth=25)

        # self.tree.heading("#0", text="")  # first column
        self.tree.heading("ID", text="SET ID")
        self.tree.heading("NAME", text="NAME")
        self.tree.heading("THEME", text="THEME")
        self.tree.heading("RETAIL", text="RETAIL")
        self.tree.heading("COST", text="COST")
        self.tree.heading("RELEASE", text="RELEASE")
        self.tree.heading("DATE", text="DATE")

        ############ FOOTER ############
        self.textInfo = Text(self.footerFrame, height=5, width=77)
        self.textInfo.pack(padx=20)

        self.root.mainloop()

    def open_details(self):
        self.topWinDetails = Toplevel()
        self.topWinDetails.title("SET DETAILS")

        ########### FRAMES #############
        self.headFrame = Frame(self.topWinDetails)
        self.headFrame.grid(row=0, columnspan=2, pady=10)
        self.legoData = LabelFrame(self.topWinDetails, text="LEGO DATA", borderwidth=2)
        self.legoData.grid(row=1, column=0, padx=5, ipady=5)
        self.portfolioData = LabelFrame(self.topWinDetails, text="PORTFOLIO DATA", borderwidth=2)
        self.portfolioData.grid(row=1, column=1, padx=5, ipady=5)
        self.footerFrame = Frame(self.topWinDetails)
        self.footerFrame.grid(row=2, column=0, columnspan=2, padx=5)

        ######### TOP LINE ############
        self.topLabel = Label(self.headFrame, text="SETNAME ODER BILD")
        self.topLabel.grid()

        ######### LEGO DATA ###########
        # self.headlineLego = Label(self.legoData, text="LEGO DATA")
        # self.headlineLego.grid(row=0, column=0)
        self.setIDlabel = Label(self.legoData, text="SET ID")
        self.setIDlabel.grid(row=1, column=0, sticky=W, padx=6)
        self.setIDbox = Entry(self.legoData)
        self.setIDbox.grid(row=2, column=0, padx=6)
        self.setNameLabel = Label(self.legoData, text="SETNAME")
        self.setNameLabel.grid(row=1, column=1, sticky=W, padx=6)
        self.setNameBox = Entry(self.legoData)
        self.setNameBox.grid(row=2, column=1, padx=6)
        self.retailLabel = Label(self.legoData, text="RETAIL PRICE")
        self.retailLabel.grid(row=3, column=0, sticky=W, padx=6)
        self.setRetailBox = Entry(self.legoData)
        self.setRetailBox.grid(row=4, column=0, padx=6)
        self.themeLabel = Label(self.legoData, text="THEME")
        self.themeLabel.grid(row=3, column=1, sticky=W, padx=6)
        self.themeBox = Entry(self.legoData)
        self.themeBox.grid(row=4, column=1, padx=6)
        self.releaseLabel = Label(self.legoData, text="RELEASE")
        self.releaseLabel.grid(row=5, column=0, sticky=W, padx=6)
        self.releaseBox = Entry(self.legoData)
        self.releaseBox.grid(row=6, column=0, padx=6)
        self.subThemeLabel = Label(self.legoData, text="SUBTHEME")
        self.subThemeLabel.grid(row=5, column=1, sticky=W, padx=6)
        self.subThemeBox = Entry(self.legoData)
        self.subThemeBox.grid(row=6, column=1, padx=6)
        self.eolLabel = Label(self.legoData, text="EOL")
        self.eolLabel.grid(row=7, column=0, sticky=W, padx=6)
        self.eolBox = Entry(self.legoData)
        self.eolBox.grid(row=8, column=0, padx=6)

        ######### PORTFOLIO DATA ###########
        # self.headlinePort = Label(self.portfolioData, text="PORTFOLIO DATA")
        # self.headlinePort.grid(row=0, column=0)
        self.costlabel = Label(self.portfolioData, text="COST")
        self.costlabel.grid(row=1, column=0, sticky=W, padx=6)
        self.costbox = Entry(self.portfolioData)
        self.costbox.grid(row=2, column=0)
        self.dateLabel = Label(self.portfolioData, text="PURCHASE DATE")
        self.dateLabel.grid(row=1, column=1, sticky=W, padx=6)
        self.dateBox = Entry(self.portfolioData)
        self.dateBox.grid(row=2, column=1, padx=6)
        self.discountLabel = Label(self.portfolioData, text="DISCOUNT")
        self.discountLabel.grid(row=3, column=0, sticky=W, padx=6)
        self.discountBox = Entry(self.portfolioData)
        self.discountBox.grid(row=4, column=0, padx=6)
        self.discount1Label = Label(self.portfolioData, text="DISCOUNT")
        self.discount1Label.grid(row=5, column=0, sticky=W, padx=6)
        self.discount1Box = Entry(self.portfolioData)
        self.discount1Box.grid(row=6, column=0, padx=6)
        self.shopLabel = Label(self.portfolioData, text="SHOP")
        self.shopLabel.grid(row=3, column=1, sticky=W, padx=6)
        self.shopBox = Entry(self.portfolioData)
        self.shopBox.grid(row=4, column=1, padx=6)
        self.amountLabel = Label(self.portfolioData, text="AMOUNT")
        self.amountLabel.grid(row=5, column=1, sticky=W, padx=6)
        self.amountBox = Entry(self.portfolioData)
        self.amountBox.grid(row=6, column=1, padx=6)
        self.avePriceLabel = Label(self.portfolioData, text="AVE PRICE")
        self.avePriceLabel.grid(row=7, column=0, sticky=W, padx=6)
        self.avePriceBox = Entry(self.portfolioData)
        self.avePriceBox.grid(row=8, column=0, padx=6)

        ########## BUTTONS ############
        self.editBut = Button(self.footerFrame, text="EDIT")
        self.editBut.grid(row=0, column=0, pady=10, padx=6)
        self.backBut = Button(self.footerFrame, text="GO BACK")
        self.backBut.grid(row=0, column=1, pady=10, padx=6)

    def add_record(self):
        addRecTopWin = Toplevel()
        addRecTopWin.title("ADD RECORD")

        def callback_theme(*args):
            if self.themeVar.get() == 'Neues Thema anlegen':
                self.add_theme()

        def callback_shop(*args):
            if var1.get() == 'Neuen Shop anlegen':
                self.add_shop()

        ########### FRAMES #############
        sucheLabel = LabelFrame(addRecTopWin, text="Suche (SET ID)")
        sucheLabel.grid(row=0, padx=10, ipady=5, pady=10, sticky=W)
        legoData = LabelFrame(addRecTopWin, text="LEGO DATA")
        legoData.grid(row=1, column=0, ipady=5, padx=5, ipadx=3)
        portfolioData = LabelFrame(addRecTopWin, text="PURCHASE DATA")
        portfolioData.grid(row=1, column=1, ipady=5, padx=5, ipadx=3)
        footerFrame = Frame(addRecTopWin)
        footerFrame.grid(columnspan=2, row=2)

        ########### SEARCH #############
        sucheEntry = Entry(sucheLabel)
        sucheEntry.grid(row=0, column=0, padx=6)
        sucheBut = Button(sucheLabel, text="go", height=1,
                          command=lambda: [self.fill_legoData(sucheEntry.get()), sucheEntry.delete(0, END)])
        sucheBut.grid(row=0, column=1, padx=6)

        ######### LEGO DATA ###########
        # headlineLego = Label(legoData, text="LEGO DATA")
        # headlineLego.grid(row=0, column=0)
        self.setIDlabel = Label(legoData, text="SET ID")
        self.setIDlabel.grid(row=1, column=0, sticky=W, padx=6)
        self.setIDbox = Entry(legoData)
        self.setIDbox.grid(row=2, column=0, padx=6)
        self.setNameLabel = Label(legoData, text="SETNAME")
        self.setNameLabel.grid(row=1, column=1, sticky=W, padx=6)
        self.setNameBox = Entry(legoData)
        self.setNameBox.grid(row=2, column=1, padx=6)
        self.retailLabel = Label(legoData, text="RETAIL PRICE")
        self.retailLabel.grid(row=3, column=0, sticky=W, padx=6)
        self.setRetailBox = Entry(legoData)
        self.setRetailBox.grid(row=4, column=0, padx=6)
        ########### THEME ############
        self.themeLabel = Label(legoData, text="THEME")
        self.themeLabel.grid(row=3, column=1, sticky=W, padx=6)
        self.themeChoices = ['a', 'b', 'Neues Thema anlegen']
        self.themeVar = StringVar()
        self.themeVar.set(self.themeChoices[0])
        self.themeBox = OptionMenu(legoData, self.themeVar, *self.themeChoices)
        self.themeBox.config(width=16, borderwidth=1)
        self.themeBox.grid(row=4, column=1, padx=6)
        self.themeVar.trace("w", callback_theme)
        ###############################
        self.releaseLabel = Label(legoData, text="RELEASE")
        self.releaseLabel.grid(row=5, column=0, sticky=W, padx=6)
        self.releaseBox = Entry(legoData)
        self.releaseBox.grid(row=6, column=0, padx=6)
        self.subThemeLabel = Label(legoData, text="SUBTHEME")
        self.subThemeLabel.grid(row=5, column=1, sticky=W, padx=6)
        self.subThemeBox = Entry(legoData)
        self.subThemeBox.grid(row=6, column=1, padx=6)
        self.eolLabel = Label(legoData, text="EOL")
        self.eolLabel.grid(row=7, column=0, sticky=W, padx=6)
        self.eolBox = Entry(legoData)
        self.eolBox.grid(row=8, column=0, padx=6)

        ######### PURCHASE DATA ###########
        costlabel = Label(portfolioData, text="COST")
        costlabel.grid(row=1, column=0, sticky=W, padx=6)
        costbox = Entry(portfolioData)
        costbox.grid(row=2, column=0)
        dateLabel = Label(portfolioData, text="PURCHASE DATE")
        dateLabel.grid(row=1, column=1, sticky=W, padx=6)
        dateBox = Entry(portfolioData)
        dateBox.grid(row=2, column=1, padx=6)
        discountLabel = Label(portfolioData, text="DISCOUNT")
        discountLabel.grid(row=3, column=0, sticky=W, padx=6)
        discountBox = Entry(portfolioData)
        discountBox.grid(row=4, column=0, padx=6)
        discount1Label = Label(portfolioData, text="DISCOUNT")
        discount1Label.grid(row=5, column=0, sticky=W, padx=6)
        discount1Box = Entry(portfolioData)
        discount1Box.grid(row=6, column=0, padx=6)
        ######### SHOP ############
        shopLabel = Label(portfolioData, text="SHOP")
        shopLabel.grid(row=3, column=1, sticky=W, padx=6)
        choices1 = ['a', 'b', 'Neuen Shop anlegen']
        var1 = StringVar()
        var1.set(choices1[0])
        shopBox = OptionMenu(portfolioData, var1, *choices1)
        shopBox.config(width=16, borderwidth=1)
        shopBox.grid(row=4, column=1, padx=6)
        var1.trace("w", callback_shop)
        ############################
        amountLabel = Label(portfolioData, text="AMOUNT")
        amountLabel.grid(row=5, column=1, sticky=W, padx=6)
        amountBox = Spinbox(portfolioData, from_=0, to=25, width=18)
        amountBox.grid(row=6, column=1, padx=7)
        avePriceLabel = Label(portfolioData, text="AVE PRICE")
        avePriceLabel.grid(row=7, column=0, sticky=W, padx=6)
        avePriceBox = Entry(portfolioData)
        avePriceBox.grid(row=8, column=0, padx=6)

        ############## FOOTER ################
        takeSetBut = Button(footerFrame, text="Apply")
        takeSetBut.grid(padx=5, row=0, column=0, pady=6)
        goBackBut = Button(footerFrame, text="Return")
        goBackBut.grid(padx=5, row=0, column=1, pady=6)

    def open_stats(self):
        statsTopWin = Toplevel()
        statsTopWin.title("Statistics")

        ########### FRAMES ############
        topFrame = Frame(statsTopWin)
        topFrame.grid(row=0)
        mainFrame = Frame(statsTopWin)
        mainFrame.grid(row=2)

        ########## DROPDOWN ##########
        dropText = StringVar()
        dropText.set("General")
        options = {'General', 'Themes', 'Worth'}
        drop = OptionMenu(topFrame, dropText, *options)
        drop.config(borderwidth=1)
        drop.pack()

        ########### GRAPH ############
        spaceHolder = Label(mainFrame, text="HIER WERDEN SPAETER DIE STATS GEZEIGT")
        spaceHolder.pack(padx=20, pady=100)

    def add_theme(self):
        newThemeTopWin = Toplevel()
        newThemeTopWin.title("New Theme")
        nameLabel = Label(newThemeTopWin, text="Name")
        nameLabel.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        nameBox = Entry(newThemeTopWin)
        nameBox.grid(row=1, column=0, padx=5)
        subLabel = Label(newThemeTopWin, text="Sub Theme")
        subLabel.grid(row=0, column=1, pady=5, sticky=W, padx=5)
        options = ['Test', '2', '3']
        var = StringVar()
        var.set(options[0])
        subThemes = OptionMenu(newThemeTopWin, var, *options)
        subThemes.grid(row=1, column=1, padx=5)
        subThemes.config(width=16, borderwidth=1)
        addBut = Button(newThemeTopWin, text="Add")
        addBut.grid(row=3, columnspan=2, pady=8)

    def add_shop(self):
        newShopTopWin = Toplevel()
        newShopTopWin.title("New Shop")
        nameLabel = Label(newShopTopWin, text="Name")
        nameLabel.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        nameBox = Entry(newShopTopWin)
        nameBox.grid(row=1, column=0, padx=5)
        urlLabel = Label(newShopTopWin, text="Sub Theme")
        urlLabel.grid(row=0, column=1, pady=5, sticky=W, padx=5)
        urlBox = Entry(newShopTopWin)
        urlBox.grid(row=1, column=1, pady=5, padx=5)
        addBut = Button(newShopTopWin, text="Add")
        addBut.grid(row=3, columnspan=2, pady=8)

    def fill_legoData(self, setNr):
        dict = get_details_from_web(setNr)
        if dict is None:
            rootWin=Tk()
            rootWin.withdraw()
            messagebox.showerror("Fehler", "Die gesuche SET-Nummer ist nicht vorhanden",parent=rootWin)
            rootWin.destroy()
        else:
            self.setNameBox.delete(0, END)
            self.setNameBox.insert(END, dict['Name'])
            self.setIDbox.delete(0, END)
            self.setIDbox.insert(END, dict['Setnummer'])
            self.setRetailBox.delete(0, END)
            self.setRetailBox.insert(END, dict['UVP'])
            self.themeVar.set(dict['Thema'])
            self.themeChoices[0] = dict['Thema']
            self.releaseBox.delete(0, END)
            self.releaseBox.insert(END, dict['Erscheinungsjahr'])


if __name__ == '__main__':
    gui = UserInterface()
