import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import pandas as pd
import numpy as np
import sqlite3 

#Creating a database connection and Table
conn = sqlite3.connect("expense_track.db")

c = conn.cursor()

#c.execute("""CREATE TABLE ExpenseLog (
#            Category text,
#            Amount integer,
#            Date text
#            )""")


#Creating root and GUI Title 
root = Tk()
root.title("Expense Calculator")

expense_list = []

label_1 =  Label(root, text ="Please select an expense:").pack(anchor = W)

#Creating a list of various expenses 
EXPENSES = [
    ("Food","Food"),
    ("Transportation","Transportation"),
    ("Entertainment","Entertainment"),
    ("Clothing","Clothing"),
    ("Medical", "Medical"),
    ("Misc", "Misc"),
    ]

#Declaring string variable for the expenses and setting Misc as the default
my_expense = StringVar()
my_expense.set("Misc")


#Functions to be called 
def clicked(value):
    radio_label = Label(root, text = value)
    radio_label.pack()
    return None

def clicked_amount():
    if amount_input.get().isnumeric():
        amount_entry = Label(root, text= "$ " + amount_input.get())
    else:
        amount_entry = Label(root, text = "Please enter a number...")
    amount_entry.pack()
    return None

def grab_date():
    label_4.config(text = cal.get_date())
    return None 

def pop_up():
    response = messagebox.askyesno("Do you want to save this?", my_expense.get() 
    + "\n" + "$ " + amount_input.get() 
    + "\n" + cal.get_date())
    if response == 1:
        expense_list.append(my_expense.get())
        expense_list.append(amount_input.get()) 
        expense_list.append(cal.get_date())
        Label(root, text = "Changes saved!", command = submit()).pack()
    else:
        Label(root, text = "Changes not saved!").pack()
    return None

def submit():
    conn = sqlite3.connect("expense_track.db")
    c = conn.cursor()

    #Inserting into the table
    c.execute("INSERT INTO ExpenseLog VALUES (:Category, :Amount, :Date)",
                {
                    "Category": my_expense.get(),
                    "Amount": amount_input.get(),
                    "Date": cal.get_date()
                })

    conn.commit()
    conn.close()    

def query():
    conn = sqlite3.connect("expense_track.db")
    c = conn.cursor()

    #Selecting the table
    c.execute("SELECT * FROM ExpenseLog")
    logs = c.fetchall()
    print(logs)
    conn.commit()

    conn.close()   

#For Loop to create Expense Category Radio Buttons
for item, category in EXPENSES:
    Radiobutton(root, text=item, variable=my_expense, value=category).pack(anchor = W)

#"Save Expense" Button
mybutton = Button(root, text= "SAVE EXPENSE", command = lambda: clicked(my_expense.get())).pack(anchor = W) 


#Creating the "Amount" Input and Button
label_2 =  Label(root, text ="Please enter an amount:").pack(anchor = W)
amount_input = Entry(root)
amount_input.pack(anchor = W)
mybutton_1 = Button(root, text= "SAVE AMOUNT", command = clicked_amount).pack(anchor = W) 


#Creating the Calendar
label_3 =  Label(root, text ="Please enter a date:").pack(anchor = W)
cal =  Calendar(root, selectmode="day", year =  2021)
cal.pack(anchor = W)
mybutton_2 = Button(root, text= "SAVE DATE", command = grab_date).pack(anchor = W)
label_4 = Label(root, text = "")

myquit = Button(root, text = "CONTINUE", command = pop_up).pack(anchor = W)
#myquery = Button(root, text = "SHOW DB", command = query).pack(anchor = W)

label_4.pack()

conn.commit()

conn.close()

root.mainloop()


