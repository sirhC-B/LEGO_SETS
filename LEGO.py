import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Notebook, Treeview

from funktions import *
import sqlite3, create_db


class UserInterface:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('LEGO SETs')

        ############### FRAMES ##############
        self.topTapFrame = Frame(self.root)
        self.topTapFrame.grid(row=0, column=0)

        self.treeFrame = Frame(self.root)
        self.treeFrame.grid(row=1, column=0)

        self.rightFrame = Frame(self.root)
        self.rightFrame.grid(row=1, column=1, sticky=N, pady=5, ipadx=10)

        self.checkFrame = Frame(self.root)
        self.checkFrame.grid(row=2)

        self.footerFrame = Frame(self.root)
        self.footerFrame.grid(row=3)

        ############# HEADLINE ##############
        self.headline = Label(self.topTapFrame, text="HEADLINE")
        self.headline.pack()

        ############ BUTTONS ###########
        self.Button1 = Button(self.rightFrame, text="HINZU", width=18, pady=8, command=self.add_record)
        self.Button1.grid(row=0)

        self.Button2 = Button(self.rightFrame, text="DELETE", width=18, pady=8)
        self.Button2.grid(row=1, pady=5)

        self.Button3 = Button(self.rightFrame, text="DETAILS", width=18, pady=8,
                              command=lambda: [self.open_details(), self.fill_purchase_details(self.selectItem())])
        self.Button3.grid(row=2)

        self.Button4 = Button(self.rightFrame, text="STATISTIC", width=18, pady=8, command=self.open_stats)
        self.Button4.grid(row=3, pady=5)

        self.Button5 = Button(self.rightFrame, text="SET DATABASE", width=18, pady=8, command=self.edit_database)
        self.Button5.grid(row=4)

        ############ TREEVIEW #############
        self.tree = ttk.Treeview(self.treeFrame)
        self.tree.grid(row=0, pady=5, padx=20)

        self.tree['columns'] = ("ID", "NAME", "THEME", "RETAIL", "COST", "RELEASE", "DATE", "DISCOUNT", "IID")

        self.tree.column("#0", width=0, stretch=NO)  # first column
        self.tree.column("ID", anchor=CENTER, width=80, minwidth=25)
        self.tree.column("NAME", anchor=CENTER, width=150, minwidth=25)
        self.tree.column("THEME", anchor=CENTER, width=124, minwidth=25)
        self.tree.column("RETAIL", anchor=CENTER, width=60, minwidth=25)
        self.tree.column("COST", anchor=CENTER, width=60, minwidth=25)
        self.tree.column("RELEASE", anchor=CENTER, width=60, minwidth=25)
        self.tree.column("DATE", anchor=CENTER, width=90, minwidth=25)
        self.tree.column("DISCOUNT", anchor=CENTER, width=90, minwidth=25)
        self.tree.column("IID", anchor=CENTER, width=90, minwidth=25)

        # self.tree.heading("#0", text="")  # first column
        self.tree.heading("ID", text="SET ID")
        self.tree.heading("NAME", text="NAME")
        self.tree.heading("THEME", text="THEME")
        self.tree.heading("RETAIL", text="RETAIL")
        self.tree.heading("COST", text="COST")
        self.tree.heading("RELEASE", text="YEAR")
        self.tree.heading("DATE", text="DATE")
        self.tree.heading("DISCOUNT", text="DISCOUNT")

        ############ FOOTER ############
        self.textInfo = Text(self.footerFrame, height=5, width=77)
        self.textInfo.grid(row=1, padx=20, pady=5)

        dupevar = IntVar()
        dupecheck = Checkbutton(self.checkFrame, text="Duplicates", variable=dupevar)
        dupecheck.grid(row=1, pady=3, sticky=W, padx=15)
        self.datevar = IntVar()
        datecheck = Checkbutton(self.checkFrame, text="Date", variable=self.datevar,
                                command=lambda: self.checkbox_function("DATE"))
        datecheck.grid(row=1, column=2, pady=3, padx=15)
        self.yearvar = IntVar()
        yearcheck = Checkbutton(self.checkFrame, text="Year", variable=self.yearvar,
                                command=lambda: self.checkbox_function("RELEASE"))
        yearcheck.grid(row=1, column=3, pady=3, padx=15)
        self.retvar = IntVar()
        retailcheck = Checkbutton(self.checkFrame, text="Retail", variable=self.retvar,
                                  command=lambda: self.checkbox_function("RETAIL"))
        retailcheck.grid(row=1, column=4, pady=3, padx=15)
        self.discvar = IntVar()
        disccheck = Checkbutton(self.checkFrame, text="Discount", variable=self.discvar,
                                command=lambda: self.checkbox_function("DISCOUNT"))
        disccheck.grid(row=1, column=5, pady=3, padx=15)

        self.columnlist = ["ID", "NAME", "THEME", "COST"]
        self.tree["displaycolumns"] = self.columnlist
        self.fill_purchase_table()
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
            if self.shopVar.get() == 'Neuen Shop anlegen':
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
                          command=lambda: [self.fill_legoData(sucheEntry.get(), 1), sucheEntry.delete(0, END)])
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
        self.themeChoices = [' ', 'Neues Thema anlegen']
        for index in get_theme_list():
            self.themeChoices.append(index)
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
        self.shopChoices = [' ', 'Neuen Shop anlegen']
        for index in get_shop_list():
            self.shopChoices.append(index)
        self.shopVar = StringVar()
        self.shopVar.set(self.shopChoices[0])
        shopBox = OptionMenu(portfolioData, self.shopVar, *self.shopChoices)
        shopBox.config(width=16, borderwidth=1)
        shopBox.grid(row=4, column=1, padx=6)
        self.shopVar.trace("w", callback_shop)
        ############################
        amountLabel = Label(portfolioData, text="AMOUNT")
        amountLabel.grid(row=5, column=1, sticky=W, padx=6)
        amountBox = Spinbox(portfolioData, from_=1, to=25, width=18)
        amountBox.grid(row=6, column=1, padx=7)
        avePriceLabel = Label(portfolioData, text="AVE PRICE")
        avePriceLabel.grid(row=7, column=0, sticky=W, padx=6)
        avePriceBox = Entry(portfolioData)
        avePriceBox.grid(row=8, column=0, padx=6)

        ############## FOOTER ################
        takeSetBut = Button(footerFrame, text="Apply",
                            command=lambda: [self.fill_messagebox(add_purchase_to_db(costbox.get(), dateBox.get(),
                                                                                     self.shopVar.get(),
                                                                                     amountBox.get(),
                                                                                     self.setIDbox.get(),
                                                                                     self.setRetailBox.get())),
                                             self.fill_purchase_table()])
        takeSetBut.grid(padx=5, row=0, column=0, pady=6)
        goBackBut = Button(footerFrame, text="Return")
        goBackBut.grid(padx=5, row=0, column=1, pady=6)

    def open_stats(self):
        statsTopWin = Toplevel(self.root)
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

    def edit_database(self):

        def update_tables():
            self.fill_set_table()
            self.fill_theme_table()
            self.fill_shop_table()

        topWinDatabase = Toplevel()
        topWinDatabase.title("DATABASE SETTINGS")
        tabControl = Notebook(topWinDatabase)

        ########### FRAMES ################

        setTab = Frame(tabControl)
        themeTab = Frame(tabControl)
        shopTab = Frame(tabControl)
        # SETs TAB
        tableFrame = Frame(setTab)
        tableFrame.grid(row=1, column=0)
        buttonFrame = Frame(setTab)
        buttonFrame.grid(row=1, column=1)
        footerFrame = Frame(setTab)
        footerFrame.grid(row=2)
        # Theme TAB
        tableFrameTh = Frame(themeTab)
        tableFrameTh.grid(row=1, column=0)
        buttonFrameTh = Frame(themeTab, width=60)
        buttonFrameTh.grid(row=1, column=1)
        # Shop Tab
        tableFrameSh = Frame(shopTab)
        tableFrameSh.grid(row=1, column=0)
        buttonFrameSh = Frame(shopTab)
        buttonFrameSh.grid(row=1, column=1)
        ########## TAB CONTROLL ###########

        tabControl.add(setTab, text='SETs DB')
        tabControl.add(themeTab, text='Theme DB')
        tabControl.add(shopTab, text='Shop DB')
        tabControl.pack(expand=1, fill='both')

        ########### SETs TABLE ############

        self.setTree = Treeview(tableFrame)
        self.setTree.pack()
        self.setTree['columns'] = ("ID", "NAME", "THEME", "RETAIL", "RELEASE")
        self.setTree.column("#0", width=0, stretch=NO)  # first column
        self.setTree.column("ID", anchor=CENTER, width=80, minwidth=25)
        self.setTree.column("NAME", anchor=CENTER, width=125, minwidth=25)
        self.setTree.column("THEME", anchor=CENTER, width=124, minwidth=25)
        self.setTree.column("RETAIL", anchor=CENTER, width=60, minwidth=25)
        self.setTree.column("RELEASE", anchor=CENTER, width=80, minwidth=25)

        self.setTree.heading("ID", text="SET ID")
        self.setTree.heading("NAME", text="NAME")
        self.setTree.heading("THEME", text="THEME")
        self.setTree.heading("RETAIL", text="RETAIL")
        self.setTree.heading("RELEASE", text="RELEASE")

        ######### THEME TABLE #############

        self.themeTree = Treeview(tableFrameTh)
        self.themeTree.pack()
        self.themeTree['columns'] = ("NAME", "SUBTHEME")
        self.themeTree.column("#0", width=0, stretch=NO)  # first column
        self.themeTree.column("NAME", anchor=CENTER, width=175, minwidth=25)
        self.themeTree.column("SUBTHEME", anchor=CENTER, width=175, minwidth=25)

        self.themeTree.heading("NAME", text="NAME")
        self.themeTree.heading("SUBTHEME", text="SUB THEME")

        ######### SHOP TABLE #############

        self.shopTree = Treeview(tableFrameSh)
        self.shopTree.pack()
        self.shopTree['columns'] = ("NAME", "URL")
        self.shopTree.column("#0", width=0, stretch=NO)  # first column
        self.shopTree.column("NAME", anchor=CENTER, width=120, minwidth=25)
        self.shopTree.column("URL", anchor=CENTER, width=230, minwidth=25)
        self.shopTree.heading("NAME", text="NAME")
        self.shopTree.heading("URL", text="URL")

        ######### ADD MENUE ###########
        def add_window():
            self.entryFrame = Frame(setTab)
            self.entryFrame.grid(row=1, column=1)
            menueFrame = Frame(self.entryFrame)
            menueFrame.grid(row=0, columnspan=2)
            ######### SEARCH #########
            sucheLabel1 = Label(menueFrame, text="Suche:")
            sucheLabel1.grid(row=0, column=0, sticky=W, padx=6)
            sucheEntry = Entry(menueFrame)
            sucheEntry.grid(row=0, column=1, padx=6)
            sucheBut = Button(menueFrame, text="go", height=1,
                              command=lambda: [self.fill_legoData(sucheEntry.get(), 2), sucheEntry.delete(0, END)])
            sucheBut.grid(row=0, column=2)

            ######### LEGO DATA ###########
            self.setIDlabel = Label(self.entryFrame, text="SET ID")
            self.setIDlabel.grid(row=1, column=0, sticky=W, padx=6)
            self.setIDbox1 = Entry(self.entryFrame)
            self.setIDbox1.grid(row=2, column=0, padx=6)
            self.setNameLabel = Label(self.entryFrame, text="SETNAME")
            self.setNameLabel.grid(row=1, column=1, sticky=W, padx=6)
            self.setNameBox1 = Entry(self.entryFrame)
            self.setNameBox1.grid(row=2, column=1, padx=6)
            self.retailLabel = Label(self.entryFrame, text="RETAIL PRICE")
            self.retailLabel.grid(row=3, column=0, sticky=W, padx=6)
            self.setRetailBox1 = Entry(self.entryFrame)
            self.setRetailBox1.grid(row=4, column=0, padx=6)
            ########### THEME ############
            self.themeLabel = Label(self.entryFrame, text="THEME")
            self.themeLabel.grid(row=3, column=1, sticky=W, padx=6)
            self.themeBox1 = Entry(self.entryFrame)
            self.themeBox1.grid(row=4, column=1, padx=6)
            ###############################
            self.releaseLabel = Label(self.entryFrame, text="RELEASE")
            self.releaseLabel.grid(row=5, column=0, sticky=W, padx=6)
            self.releaseBox1 = Entry(self.entryFrame)
            self.releaseBox1.grid(row=6, column=0, padx=6)
            self.subThemeLabel = Label(self.entryFrame, text="SUBTHEME")
            self.subThemeLabel.grid(row=5, column=1, sticky=W, padx=6)
            self.subThemeBox1 = Entry(self.entryFrame)
            self.subThemeBox1.grid(row=6, column=1, padx=6)

            bframe = Frame(self.entryFrame)
            bframe.grid(row=7, columnspan=2)
            addButton = Button(bframe, text="Add",
                               command=lambda: [self.fill_messagebox(
                                   add_set_to_DB(self.setIDbox1.get(), self.setNameBox1.get(), self.setRetailBox1.get(),
                                                 self.themeBox1.get(), self.releaseBox1.get(), self.subThemeBox1.get()
                                                 )), self.clear_boxes(2), update_tables()
                               ])

            addButton.grid(column=0, pady=5, row=0)
            closeButton = Button(bframe, text="Close", command=lambda: [self.entryFrame.destroy()])
            closeButton.grid(column=1, padx=5, row=0)

        def add_window_th():
            add_thFrame = Frame(themeTab)
            add_thFrame.grid(row=1, column=1)
            nameLabel = Label(add_thFrame, text="NAME")
            nameLabel.grid(row=0, column=0, sticky=W, pady=5, padx=25)
            nameBox = Entry(add_thFrame)
            nameBox.grid(row=1, column=0, padx=25)
            subLabel = Label(add_thFrame, text="SUB THEME")
            subLabel.grid(row=2, column=0, pady=5, sticky=W, padx=25)
            subBox = Entry(add_thFrame)
            subBox.grid(row=3, column=0, padx=5)
            subButFrame = Frame(add_thFrame)
            subButFrame.grid(row=4)
            addBut = Button(subButFrame, text="Add",
                            command=lambda: [self.fill_messagebox(add_theme_to_DB(nameBox.get(), subBox.get())),
                                             nameBox.delete(0, END), subBox.delete(0, END), update_tables()
                                             ])
            addBut.grid(row=0, column=0, pady=8, padx=5)
            closeBut = Button(subButFrame, text="Close", command=add_thFrame.destroy)
            closeBut.grid(row=0, column=1)

        def add_window_sh():
            add_shFrame = Frame(shopTab)
            add_shFrame.grid(row=1, column=1)
            nameLabel = Label(add_shFrame, text="NAME")
            nameLabel.grid(row=0, column=0, sticky=W, pady=5, padx=25)
            nameBox = Entry(add_shFrame)
            nameBox.grid(row=1, column=0, padx=25)
            urlLabel = Label(add_shFrame, text="URL")
            urlLabel.grid(row=2, column=0, pady=5, sticky=W, padx=25)
            urlBox = Entry(add_shFrame)
            urlBox.grid(row=3, column=0, padx=5)
            subButFrame = Frame(add_shFrame)
            subButFrame.grid(row=4)
            addBut = Button(subButFrame, text="Add", command=lambda: [self.fill_messagebox(add_shop_to_DB(nameBox.get(),
                                                                                                          urlBox.get())),
                                                                      nameBox.delete(0, END), urlBox.delete(0, END),
                                                                      update_tables()
                                                                      ])
            addBut.grid(row=0, column=0, pady=8, padx=5)
            closeBut = Button(subButFrame, text="Close", command=add_shFrame.destroy)
            closeBut.grid(row=0, column=1)

        ######### BUTTONS ##########
        # Sets
        expand_to_addBut = Button(buttonFrame, text="ADD SET", width=15, command=add_window)
        expand_to_addBut.grid(row=0, pady=5, padx=10)
        remove_setBut = Button(buttonFrame, text="REMOVE SET", width=15, command=add_window)
        remove_setBut.grid(row=1, padx=10)
        # Themes
        expand_to_add_ThBut = Button(buttonFrameTh, text="ADD THEME", width=15, command=add_window_th)
        expand_to_add_ThBut.grid(row=0, pady=5, padx=15)
        remove_thBut = Button(buttonFrameTh, text="REMOVE THEME", width=15)
        remove_thBut.grid(row=1, padx=15)
        # Shop
        expand_to_add_shBut = Button(buttonFrameSh, text="ADD SHOP", width=15, command=add_window_sh)
        expand_to_add_shBut.grid(row=0, pady=5, padx=15)
        remove_shBut = Button(buttonFrameSh, text="REMOVE SHOP", width=15)
        remove_shBut.grid(row=1, padx=15)

        update_tables()

    def add_theme(self):
        newThemeTopWin = Toplevel()
        newThemeTopWin.title("New Theme")
        nameLabel = Label(newThemeTopWin, text="Name")
        nameLabel.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        nameBox = Entry(newThemeTopWin)
        nameBox.grid(row=1, column=0, padx=5)
        subLabel = Label(newThemeTopWin, text="Sub Theme")
        subLabel.grid(row=0, column=1, pady=5, sticky=W, padx=5)
        options = ['', '2', '3']
        var = StringVar()
        var.set(options[0])
        subThemes = OptionMenu(newThemeTopWin, var, *options)
        subThemes.grid(row=1, column=1, padx=5)
        subThemes.config(width=16, borderwidth=1)
        addBut = Button(newThemeTopWin, text="Add",
                        command=lambda: [self.fill_messagebox(add_theme_to_DB(nameBox.get(), var.get())),
                                         self.themeVar.set(nameBox.get()),
                                         nameBox.delete(0, END),
                                         newThemeTopWin.destroy()])
        addBut.grid(row=3, columnspan=2, pady=8)

    def add_shop(self):
        newShopTopWin = Toplevel()
        newShopTopWin.title("New Shop")
        nameLabel = Label(newShopTopWin, text="Name")
        nameLabel.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        nameBox = Entry(newShopTopWin)
        nameBox.grid(row=1, column=0, padx=5)
        urlLabel = Label(newShopTopWin, text="URL")
        urlLabel.grid(row=0, column=1, pady=5, sticky=W, padx=5)
        urlBox = Entry(newShopTopWin)
        urlBox.grid(row=1, column=1, pady=5, padx=5)
        addBut = Button(newShopTopWin, text="Add",
                        command=lambda: [self.fill_messagebox(add_shop_to_DB(nameBox.get(), urlBox.get())),
                                         self.shopVar.set(nameBox.get()),
                                         nameBox.delete(0, END), urlBox.delete(0, END),
                                         newShopTopWin.destroy()])
        addBut.grid(row=3, columnspan=2, pady=8)

    def fill_legoData(self, setNr, win):  # win ist zum identifizieren in welchem fenster der aufruf stattfindet
        dict = get_details_from_web(setNr)

        if dict is None:
            self.fill_messagebox("Die gesuche SET-Nummer ist nicht vorhanden")

        else:
            if win == 1:  # hizu-fenster
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

            elif win == 2:  # sets database
                self.setNameBox1.delete(0, END)
                self.setNameBox1.insert(END, dict['Name'])
                self.setIDbox1.delete(0, END)
                self.setIDbox1.insert(END, dict['Setnummer'])
                self.setRetailBox1.delete(0, END)
                self.setRetailBox1.insert(END, dict['UVP'])
                self.themeBox1.delete(0, END)
                self.themeBox1.insert(END, dict['Thema'])
                self.releaseBox1.delete(0, END)
                self.releaseBox1.insert(END, dict['Erscheinungsjahr'])

            elif win == 3:  # details
                self.setNameBox.delete(0, END)
                self.setNameBox.insert(END, dict['Name'])
                self.setIDbox.delete(0, END)
                self.setIDbox.insert(END, dict['Setnummer'])
                self.setRetailBox.delete(0, END)
                self.setRetailBox.insert(END, dict['UVP'])
                self.themeBox.delete(0, END)
                self.themeBox.insert(END, dict['Thema'])
                self.releaseBox.delete(0, END)
                self.releaseBox.insert(END, dict['Erscheinungsjahr'])

    def fill_purchase_details(self, values):
        self.fill_legoData(values[0], 3)
        self.clear_boxes(3)
        list = search_for_purchase(values[8])
        for data in list:
            self.costbox.insert(END, str(data[1]) + " €")
            self.dateBox.insert(END, data[2])
            self.discountBox.insert(END, str(data[3]) + " %")
            self.shopBox.insert(END, data[6])
            self.amountBox.insert(END, data[4])
        print(search_for_purchase(values[8]))

    def fill_messagebox(self, message):
        self.textInfo.insert(END, message + "\n")

    def clear_boxes(self, win):
        if win == 2:
            self.setIDbox1.delete(0, END)
            self.setNameBox1.delete(0, END)
            self.setRetailBox1.delete(0, END)
            self.themeBox1.delete(0, END)
            self.releaseBox1.delete(0, END)
            self.subThemeBox1.delete(0, END)
        elif win == 3:
            self.costbox.delete(0, END)
            self.dateBox.delete(0, END)
            self.discountBox.delete(0, END)
            self.discount1Box.delete(0, END)
            self.shopBox.delete(0, END)
            self.amountBox.delete(0, END)
            self.avePriceBox.delete(0, END)

    def fill_set_table(self):
        self.setTree.delete(*self.setTree.get_children())
        list = get_set_records()
        for data in list:
            self.setTree.insert('', 'end', values=(data[0], data[1], data[2], data[3] + " €", data[4]))

    def fill_theme_table(self):
        self.themeTree.delete(*self.themeTree.get_children())
        list = get_theme_records()
        for data in list:
            self.themeTree.insert('', 'end', values=(data[0], data[1]))

    def fill_shop_table(self):
        self.shopTree.delete(*self.shopTree.get_children())
        list = get_shop_records()
        for data in list:
            self.shopTree.insert('', 'end', values=(data[0], data[1]))

    def fill_purchase_table(self):
        self.tree.delete(*self.tree.get_children())
        list = get_purchase_records()
        for data in list:
            self.tree.insert('', 'end',
                             values=(
                                 data[4], data[6], data[7], str(data[8]) + "€", str(data[0]) + "€", data[9], data[1],
                                 str(data[10]) + "%", data[11]))

    def checkbox_function(self, var):
        if var not in self.columnlist:
            self.columnlist.append(var)
            self.tree["displaycolumns"] = self.columnlist

        elif var in self.columnlist:
            self.columnlist.remove(var)
            self.tree["displaycolumns"] = self.columnlist

    def selectItem(self):
        curItem = self.tree.focus()
        print(self.tree.item(curItem)['values'])
        return self.tree.item(curItem)['values']


if __name__ == '__main__':
    db = sqlite3.connect('lego_db')
    create_db.create_table(db)
    gui = UserInterface()
