from tkinter import *
import sqlite3
import tkinter.messagebox

conn = sqlite3.connect(
    'C:/Users/aseth/OneDrive/Desktop/POS Software/Database/store.db')
c = conn.cursor()

result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]


class Database1:
    def __init__(self, master, *args, **kwargs):

        self.master = master

        self.all_win = Frame(master, width=1366, height=768, bg='grey')
        self.all_win.pack()

        self.heading = Label(master, text='Add Products', font=(
            'arial 30 bold'), fg='white', bg='grey')
        self.heading.place(x=400, y=0)

        # Labels for the Database Addition window
        self.name_label = Label(
            master, text='Product Name:', bg='grey', fg='white', font=('arial 18 bold'))
        self.name_label.place(x=40, y=70)

        self.stock_label = Label(master, text='Stocks: ',
                                 font=('arial 18 bold'), fg='white', bg='grey')
        self.stock_label.place(x=40, y=120)

        self.cp_label = Label(master, text='Cost Price: ',
                              bg='grey', fg='white', font=('arial 18 bold'))
        self.cp_label.place(x=40, y=170)

        self.sp_label = Label(master, bg='grey', fg='white', text='Selling Price: ',
                              font=('arial 18 bold'))
        self.sp_label.place(x=40, y=220)

        self.vendor_label = Label(
            master, text='Vendor Name: ', bg='grey', fg='white', font=('arial 18 bold'))
        self.vendor_label.place(x=40, y=270)

        self.vendor_phoneno_label = Label(
            master, text='Vendor Phone No: ', bg='grey', fg='white', font=('arial 18 bold'))
        self.vendor_phoneno_label.place(x=40, y=320)

        self.id_label = Label(
            master, text='ID: ', bg='grey', fg='white', font=('arial 18 bold'))
        self.id_label.place(x=40, y=370)

        # Entries for the Labels
        self.name_entry = Entry(master, width=25,
                                font=('arial 15 bold'), bg='lightblue')
        self.name_entry.place(x=350, y=70)

        self.stocks_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.stocks_entry.place(x=350, y=120)

        self.cp_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.cp_entry.place(x=350, y=170)

        self.sp_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.sp_entry.place(x=350, y=220)

        self.vendor_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.vendor_entry.place(x=350, y=270)

        self.vendor_phoneno_entry = Entry(
            master, width=25, font=('arial 15 bold'), bg='lightblue')
        self.vendor_phoneno_entry.place(x=350, y=320)

        self.id_entry = Entry(
            master, width=25, font=('arial 15 bold'), bg='lightblue')
        self.id_entry.place(x=350, y=370)

        # Button to Add to the Database
        self.btnAdd = Button(master, text='Add To Database',
                             width=25, height=2, bg='steelblue', fg='black', command=self.get_Items)
        self.btnAdd.place(x=500, y=420)

        self.btnClearAll = Button(master, text='Clear All Fields',
                                  width=18, height=2, bg='lightgreen', fg='black', command=self.clear)
        self.btnClearAll.place(x=350, y=420)

        # TextBox for Logs
        self.textBox1 = Text(master, width=75, height=20, bg='lightblue')
        self.textBox1.place(x=670, y=70)
        self.textBox1.insert(END, "ID has reached up to " + str(id))

        self.master.bind('<Return>', self.get_Items)
        self.master.bind('<Up>', self.clear)

    def get_Items(self, *args, **kwargs):
        # recieving information from the entries
        self.name = self.name_entry.get()
        self.stock = self.stocks_entry.get()
        self.cp = self.cp_entry.get()
        self.sp = self.sp_entry.get()
        self.vendor = self.vendor_entry.get()
        self.vendor_phoneno = self.vendor_phoneno_entry.get()

        # Dynamic Entries
        self.totalcp = float(self.cp) * float(self.stock)
        self.totalsp = float(self.sp) * float(self.stock)
        self.assumed_profit = float(self.totalsp - self.totalcp)

        if self.name == '' or self.stock == '' or self.cp == '' or self.sp == '':
            tkinter.messagebox.showinfo('Error', 'please fill all the entries')
        else:
            sql = "INSERT INTO Inventory (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno) VALUES(?,?,?,?,?,?,?,?,?)"
            c.execute(sql, (self.name, self.stock, self.cp, self.sp, self.totalcp,
                            self.totalsp, self.assumed_profit, self.vendor, self.vendor_phoneno))
            conn.commit()

            # Textbox Message
            self.textBox1.insert(END, "\n\nInserted " +
                                 str(self.name) + " into the Database with code  " + str(self.id_entry.get()))
            tkinter.messagebox.showinfo(
                'Success', 'Sucessfully Added To The Database')

    def clear(self, *args, **kwargs):
        self.name_entry.delete(0, END)
        self.stocks_entry.delete(0, END)
        self.cp_entry.delete(0, END)
        self.sp_entry.delete(0, END)
        self.vendor_entry.delete(0, END)
        self.vendor_phoneno_entry.delete(0, END)
        self.id_entry.delete(0, END)


root = Tk()
b = Database1(root)

root.geometry('1366x768+0+0')
root.title('Add to the Database')
root.mainloop()
