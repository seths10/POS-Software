from tkinter import *
import sqlite3
import tkinter.messagebox

conn = sqlite3.connect(
    'C:/Users/aseth/OneDrive/Desktop/POS Software/Database/store.db')
c = conn.cursor()

result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]


class Database:
    def __init__(self, master, *args, **kwargs):

        self.master = master

        self.all_win = Frame(master, width=1366, height=768, bg='grey')
        self.all_win.pack()

        self.heading = Label(master, text='Product Update', font=(
            'arial 30 bold'), fg='white', bg='grey')
        self.heading.place(x=400, y=0)

        # Labels for the Database Update window
        self.id_label = Label(
            master, text=' Enter ID: ', font=('arial 18 bold'),  bg='grey',  fg='white')
        self.id_label.place(x=40, y=70)

        self.name_label = Label(
            master, text='Product Name: ', font=('arial 18 bold'),  bg='grey', fg='white')
        self.name_label.place(x=40, y=120)

        self.stock_label = Label(master, text='Stocks: ',
                                 font=('arial 18 bold'),  bg='grey', fg='white')
        self.stock_label.place(x=40, y=170)

        self.cp_label = Label(master, text='Cost Price: ',
                              font=('arial 18 bold'),  bg='grey', fg='white')
        self.cp_label.place(x=40, y=220)

        self.sp_label = Label(master, text='Selling Price: ',
                              font=('arial 18 bold'),  bg='grey', fg='white')
        self.sp_label.place(x=40, y=270)

        self.totalcp_label = Label(
            master, text='Total Cost Price', font=('arial 18 bold'), bg='grey', fg='white')
        self.totalcp_label.place(x=40, y=320)

        self.totalsp_label = Label(
            master, text='Total Selling Price: ', font=('arial 18 bold'), bg='grey', fg='white')
        self.totalsp_label.place(x=40, y=370)

        self.vendor_label = Label(
            master, text='Vendor Name: ', font=('arial 18 bold'), bg='grey', fg='white')
        self.vendor_label.place(x=40, y=420)

        self.vendor_phoneno_label = Label(
            master, text=' Vendor Phone No', font=('arial 18 bold'), bg='grey', fg='white')
        self.vendor_phoneno_label.place(x=40, y=470)

        # Entries for the Labels
        self.id_entry = Entry(
            master, width=10, font=('arial 15 bold'), bg='lightblue')
        self.id_entry.place(x=350, y=70)

        self.name_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.name_entry.place(x=350, y=120)

        self.stocks_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.stocks_entry.place(x=350, y=170)

        self.cp_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.cp_entry.place(x=350, y=220)

        self.sp_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.sp_entry.place(x=350, y=270)

        self.totalcp_entry = Entry(
            master, width=25, font=('arial 15 bold'), bg='lightblue')
        self.totalcp_entry.place(x=350, y=320)

        self.totalsp_entry = Entry(
            master, width=25, font=('arial 15 bold'), bg='lightblue')
        self.totalsp_entry.place(x=350, y=370)

        self.vendor_entry = Entry(master, width=25, font=(
            'arial 15 bold'), bg='lightblue')
        self.vendor_entry.place(x=350, y=420)

        self.vendor_phoneno_entry = Entry(
            master, width=25, font=('arial 15 bold'), bg='lightblue')
        self.vendor_phoneno_entry.place(x=350, y=470)

        # Button to Update the Database
        self.btnUpdate = Button(master, text='Update Database',
                                width=25, height=2, bg='steelblue', fg='white', command=self.update)
        self.btnUpdate.place(x=450, y=520)

        self.btnSearch = Button(master, text='Search',
                                width=12, height=1, bg='lightgreen', fg='white', command=self.search)
        self.btnSearch.place(x=500, y=80)
        self.master.bind('<Return>', self.search)

        # TextBox for Logs
        self.textBox1 = Text(master, width=75, height=25, bg='lightblue')
        self.textBox1.place(x=670, y=70)
        self.textBox1.insert(END, "ID has reached up to " + str(id))

    def search(self, *args, **kwargs):
        sql = "SELECT  * FROM Inventory WHERE id=?"
        result = c.execute(sql, (self.id_entry.get(), ))
        for r in result:
            self.n1 = r[1]  # name
            self.n2 = r[2]  # stock
            self.n3 = r[3]  # cp
            self.n4 = r[4]  # sp
            self.n5 = r[5]  # totalcp
            self.n6 = r[6]  # totalsp
            self.n7 = r[7]  # assumed_profit
            self.n8 = r[8]  # vendor
            self.n9 = r[9]  # vendor_phoneno

        conn.commit()

        # insert into the entries to update
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, str(self.n1))

        self.stocks_entry.delete(0, END)
        self.stocks_entry.insert(0, str(self.n2))

        self.cp_entry.delete(0, END)
        self.cp_entry.insert(0, str(self.n3))

        self.sp_entry.delete(0, END)
        self.sp_entry.insert(0, str(self.n4))

        self.vendor_entry.delete(0, END)
        self.vendor_entry.insert(0, str(self.n8))

        self.vendor_phoneno_entry.delete(0, END)
        self.vendor_phoneno_entry.insert(0, str(self.n9))

        self.totalcp_entry.delete(0, END)
        self.totalcp_entry.insert(0, str(self.n5))

        self.totalsp_entry.delete(0, END)
        self.totalsp_entry.insert(0, str(self.n6))

    def update(self, *args, **kwargs):
        # get all updated values
        self.uptval1 = self.name_entry.get()
        self.uptval2 = self.stocks_entry.get()
        self.uptval3 = self.cp_entry.get()
        self.uptval4 = self.sp_entry.get()
        self.uptval5 = self.totalcp_entry.get()
        self.uptval6 = self.totalsp_entry.get()
        self.uptval7 = self.vendor_entry.get()
        self.uptval8 = self.vendor_phoneno_entry.get()

        query = "UPDATE Inventory SET name=?, stock=?, cp=?, sp=?, totalcp=?, totalsp=?, vendor=?, vendor_phoneno=? WHERE id=?"
        c.execute(query, (self.uptval1, self.uptval2, self.uptval3, self.uptval4,
                          self.uptval5, self.uptval6, self.uptval7, self.uptval8, self.id_entry.get()))
        conn.commit()
        tkinter.messagebox.showinfo('Success', 'Database Updated')


root = Tk()
z = Database(root)

root.geometry('1366x768+0+0')
root.title('Update the Database')
root.mainloop()
