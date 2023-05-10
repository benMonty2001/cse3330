from tkinter import *
import sqlite3

card_no_label = None
output_label = None

def create_borrower_win():
    # create window
    borrower_win = Tk()
    borrower_win.title('Add Borrower')
    borrower_win.geometry("1000x1000")

    # gui components / button calls submit_borrower

    # create text boxes
    name = Entry(borrower_win, width=30)
    name.grid(row=1, column=1)
    address = Entry(borrower_win, width=30)
    address.grid(row=2, column=1)
    phone = Entry(borrower_win, width=30)
    phone.grid(row=3, column=1)

    # create labels
    name_label = Label(borrower_win, text='Name: ')
    name_label.grid(row=1, column=0)
    address_label = Label(borrower_win, text='Address: ')
    address_label.grid(row=2, column=0)
    phone_label = Label(borrower_win, text='Phone: ')
    phone_label.grid(row=3, column=0)
    submit_btn = Button(borrower_win, text='Add Borrower ', command=lambda: submit_borrower(borrower_win, name.get(), address.get(), phone.get()))
    submit_btn.grid(row=4, column=1)

    global card_no_label
    card_no_label = Label(borrower_win)
    card_no_label.grid(row = 9, column = 1)

    global output_label
    output_label = Label(borrower_win)
    output_label.grid(row = 10, column = 1)

def submit_borrower(borrower_win, name, address, phone):
    # Check if the input values are not empty
    if not name or not address or not phone:
        return

    # establish connection
    submit_conn = sqlite3.connect('../LMS.sql')
    submit_cur = submit_conn.cursor()

    # perform query
    submit_cur.execute("INSERT INTO Borrower VALUES(:card_no, :name, :address, :phone) ",
                        {
                            'card_no': submit_cur.execute("SELECT count(*) from Borrower").fetchone()[0] + 1,
                            'name': name,
                            'address': address,
                            'phone': phone
                        })

    # display card_no
    global card_no_label
    if card_no_label != None:
        card_no_label.destroy()
    card_no_label = Label(borrower_win, text='Borrower card_no is: ' + str(submit_cur.execute("SELECT count(*) from Borrower").fetchone()[0]) + "\n\n")
    card_no_label.grid(row=9, column=1)

    # output table
    submit_cur.execute("SELECT * FROM Borrower")
    output_records = submit_cur.fetchall()
    print_record = ''
    iq_label = Label(borrower_win, text=print_record)
    for output_record in output_records:
        print_record += str("card_no(" + str(output_record[0]) + ") | Name(" + str(output_record[1]) + ") | Address(" + str(output_record[2]) + ") | Phone(" + str(output_record[3]) + ')\n')
    global output_label
    if output_label:
        output_label.destroy()
    output_label = Label(borrower_win, text=print_record)
    output_label.grid(row=10, column=1)

    # commit changes
    submit_conn.commit()

    # close the DB connection
    submit_conn.close()
