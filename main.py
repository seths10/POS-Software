#!/usr/bin/python
from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime
import math
import os
import random
import sys

conn = sqlite3.connect("store.db")
c = conn.cursor()

# Date
date = datetime.datetime.now().date()


def addproducts():
    os.system('add_to_db.py')


def updateproducts():
    os.system('update.py')


products_list = []
products_price = []
products_quantity = []
products_id = []

# List for Label
Labels_list = []


class Application:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        # Frames
        self.left = Frame(master, width=700, height=768, bg='grey')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=665, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        self.mid = Frame(master, width=350, height=40, bg='lightblue')
        self.mid.place(x=50, y=185)

        # Components
        self.heading = Label(self.left, text="Seth's Supermarket",
                             font=('courier 25 bold'), bg='grey')
        self.heading.place(x=180, y=20)

        self.date_label = Label(self.right, text="Today's Date: " +
                                str(date), font=('arial 16 bold'), bg='lightblue', fg='black')
        self.date_label.place(x=0, y=0)

        # Table Invoice------------------------------------------------------
        self.tproduct = Label(self.right, text="Products", font=(
            'arial 18 bold'), bg='lightblue', fg='black')
        self.tproduct.place(x=0, y=60)

        self.tquantity = Label(self.right, text="Quantity", font=(
            'arial 18 bold'), bg='lightblue', fg='black')
        self.tquantity.place(x=250, y=60)

        self.tamount = Label(self.right, text="Amount", font=(
            'arial 18 bold'), bg='lightblue', fg='black')
        self.tamount.place(x=500, y=60)

        # Enter Products
        self.enterid = Label(self.left, text="Product's Name: ",
                             font=('arial 18 bold'), fg='black', bg='grey')
        self.enterid.place(x=40, y=80)

        self.enterid_entry = Entry(self.left, font=(
            'arial 18 bold'), bg='lightblue', fg='black')
        self.enterid_entry.place(x=250, y=80)
        self.enterid_entry.focus()

        # Button
        self.btnSearch = Button(
            self.left, text='Search', width=15, height=2, bg='lightblue', command=self.ajax)
        self.btnSearch.place(x=450, y=120)
        self.master.bind('<Return>', self.ajax)

        self.btnQRCode = Button(
            self.left, text='Scan QR CODE', width=15, height=2, bg='lightblue')
        self.btnQRCode.place(x=300, y=120)

        Label(self.mid, text='Admin', font=(
            'helvetica 10 bold'), bg='white', fg='black').pack(side=LEFT)

        self.btnAdd = Button(self.mid, text='Add Products',
                             width=15, height=2, bg='lightblue', command=addproducts)
        self.btnAdd.pack(side=LEFT)

        self.btnUpdate = Button(self.mid, text='Update Products',
                                width=15, height=2, bg='lightblue', command=updateproducts)
        self.btnUpdate.pack(side=RIGHT)

        self.productname = Label(self.left, text='', font=(
            'arial 27 bold'), bg='grey', fg='black')
        self.productname.place(x=0, y=250)

        self.pprice = Label(self.left, text='', font=(
            'arial 27 bold'), bg='grey', fg='black')
        self.pprice.place(x=0, y=290)

        # total Label
        self.total_label = Label(self.right, text='',  font=(
            'arial 40 bold'), bg='lightblue', fg='black')
        self.total_label.place(x=0, y=600)
        self.master.bind('<Return>', self.ajax)
        self.master.bind('<Up>', self.add_to_cart)
        self.master.bind('<space>', self.generate_bill)

    # def barcodescan(self):
    #     self.cap = cv2.VideoCapture(0)

    #     while True:
    #         _, frame = self.cap.read()

    #         self.decodedObjects = pyzbar.decode(frame)
    #         for obj in self.decodedObjects:
    #             print(obj.data)

    #         cv2.imshow("Scan QR CODE", frame)

    #         key = cv2.waitKey(0)
    #         if key == 27:
    #             break

    def ajax(self, *args, **kwargs):
        self.get_id = self.enterid_entry.get()
        # get all products info from id
        query = "SELECT * FROM Inventory WHERE id=?"
        result = c.execute(query, (self.get_id,))
        for self.r in result:
            self.get_id = self.r[0]
            self.get_name = self.r[1]
            self.get_price = self.r[4]
            self.get_stock = self.r[2]
        self.productname.configure(
            text="Product's Name: " + str(self.get_name))
        self.pprice.configure(text="Price: GH¢" + str(self.get_price))

        # Quantity And Discount Label
        self.quantity_label = Label(
            self.left, text='Quantity', font=('arial 18 bold'), bg='grey')
        self.quantity_label.place(x=0, y=370)

        self.quantity_entry = Entry(
            self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.quantity_entry.place(x=190, y=370)
        self.quantity_entry.focus()

        self.discount_label = Label(
            self.left, text='Discount Rate', font=('arial 18 bold'), bg='grey')
        self.discount_label.place(x=0, y=410)

        self.discount_entry = Entry(
            self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.discount_entry.place(x=190, y=410)
        self.discount_entry.insert(END, 0)

        # Add To Cart Button
        self.btnCart = Button(self.left, text='Add To Cart',
                              width=15, height=2, bg='lightblue', command=self.add_to_cart)
        self.btnCart.place(x=400, y=450)

        # Generate Bill and Balance
        self.givenAmt_label = Label(
            self.left, text='Given Amount', font=('arial 18 bold'), bg='grey')
        self.givenAmt_label.place(x=0, y=550)

        self.givenAmt_entry = Entry(
            self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.givenAmt_entry.place(x=190, y=550)

        self.BtnChange = Button(
            self.left, text='Calculate Balance', width=18, height=2, bg='lightblue', command=self.balance_func)
        self.BtnChange.place(x=380, y=590)

        self.btnBill = Button(
            self.left, text='Generate Bill/ Reciept', width=55, height=2, bg='lightgreen', command=self.generate_bill)
        self.btnBill.place(x=160, y=670)

    def add_to_cart(self, *args, **kwargs):
        # Get all the quantity value from database
        self.quantity_value = int(self.quantity_entry.get())
        if self.quantity_value > int(self.get_stock):
            tkinter.messagebox.showinfo(
                'Error', 'Not that many products are in the inventory')
        else:
            self.final_price = (float(
                self.quantity_value) * float(self.get_price)) - (float(self.discount_entry.get()))

            products_list.append(self.get_name)
            products_price.append(self.final_price)
            products_quantity.append(self.quantity_value)
            products_id.append(self.get_id)

            self.x_index = 0
            self.y_index = 100
            self.counter = 0

            for self.p in products_list:
                self.tempname = Label(self.right, text=str(products_list[self.counter]), font=(
                    'arial 14 bold'), bg='lightblue', fg='black')
                self.tempname.place(x=0, y=self.y_index)
                Labels_list.append(self.tempname)

                self.tempqt = Label(self.right, text=str(products_quantity[self.counter]), font=(
                    'arial 14 bold'), bg='lightblue', fg='black')
                self.tempqt.place(x=300, y=self.y_index)
                Labels_list.append(self.tempqt)

                self.tempprice = Label(self.right, text='¢ ' + str(products_price[self.counter]), font=(
                    'arial 14 bold'), bg='lightblue', fg='black')
                self.tempprice.place(x=500, y=self.y_index)
                Labels_list.append(self.tempprice)

                self.y_index += 40
                self.counter += 1

                # operations on total
            self.total_label.configure(
                text='Total: GH¢' + str(sum(products_price)))

            # Delete all entries
            self.quantity_label.place_forget()
            self.quantity_entry.place_forget()
            self.discount_label.place_forget()
            self.discount_entry.place_forget()
            self.productname.configure(text='')
            self.pprice.configure(text='')
            self.btnCart.destroy()

            # Return focus to product Name Entry
            self.enterid_entry.focus()
            self.enterid_entry.delete(0, END)

    def balance_func(self, *args, **kwargs):
        # Get the amount given by customer
        self.amount_given = int(self.givenAmt_entry.get())
        self.our_total = float(sum(products_price))

        self.to_give = self.amount_given - self.our_total

        # Balance Label

        self.c_amount = Label(self.left, text='Balance: ¢ ' +
                              str(self.to_give), font=('Calibri 18 bold'), fg='red')
        self.c_amount.place(x=0, y=590)

    def generate_bill(self, *args, **kwargs):
        # Bill
        directory = "C:/Users/aseth/OneDrive/Desktop/POS Software/Invoice/" + \
            str(date)
        if not os.path.exists(directory):
            os.mkdir(directory)

            # Bill Template
        company = "\t\t\t\tSeth's Supermarket.\n"
        address = "\t\t\t\t   Awoshie,Accra\n"
        phone = "\t\t\t\t   +233559372716\n"
        sample = "\t\t\t\t    Invoice\n"
        dt = "  \t\t\t\t    " + str(date)

        table_header = "\n\n\t\t---------------------------------------------------\n\t\tSN.\tProducts\t\tQty\t\tAmount\n\t\t---------------------------------------------------"
        final = company + address + phone + sample + dt + "\n" + table_header

        # writing to file
        file_name = str(directory) + \
            str(random.randrange(5000, 10000)) + '.rtf'
        f = open(file_name, 'w')
        f.write(final)

        #  Adding Detail to the template
        r = 1
        i = 0
        for t in products_list:
            f.write("\n\t\t" + str(r) + "\t" + str(products_list[i] + "\t\t" + str(
                products_quantity[i]) + "\t\t" + str(products_price[i])))
            i += 1
            r += 1

        f.write("\n\n\t\tTotal: Gh¢ " + str(sum(products_price)))
        f.write("\n\t\tThanks For Visiting")
        os.startfile(file_name, "print")
        f.close()

        # Decrease Stock
        self.x = 0

        initial = "SELECT * FROM Inventory WHERE id=?"
        result = c.execute(initial, (products_id[self.x],))

        for r in result:
            self.old_stock = r[2]
        for i in products_list:
            self.new_stock = int(self.old_stock) - \
                int(products_quantity[self.x])

            # Updating The Stock
            sql = "UPDATE Inventory SET stock=? WHERE id=?"
            c.execute(sql, (self.new_stock, products_id[self.x]))
            conn.commit()

            # Insert Into The Transactions
            sql2 = "INSERT INTO Transactions (product_name, quantity, amount, date) VALUES (?, ?, ?, ?)"
            c.execute(
                sql2, (products_list[self.x], products_quantity[self.x], products_price[self.x], date))
            conn.commit()

            self.x += 1

        for a in Labels_list:
            a.destroy()

        del(products_list[:])
        del(products_id[:])
        del(products_price[:])
        del(products_quantity[:])

        self.total_label.configure(text='')
        self.c_amount.configure(text='')
        self.givenAmt_entry.delete(0, END)
        self.enterid_entry.focus()


root = Tk()
b = Application(root)

root.geometry('1366x768+0+0')
root.title("Seth's Store")
root.mainloop()
