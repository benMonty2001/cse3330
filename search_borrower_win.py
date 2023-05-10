from tkinter import *
import sqlite3

output_label = None

def create_search_borrower_win():
    
    search_borrower_win = Tk()
    search_borrower_win.title('Search Borrowers')
    search_borrower_win.geometry("1000x1000")

    #gui components

    # create text boxes
    borrower_id = Entry(search_borrower_win, width = 30)
    borrower_id.grid(row = 1, column = 1)
    borrower_name = Entry(search_borrower_win, width = 30)
    borrower_name.grid(row = 2, column = 1)

    #create labels
    borrower_id_label = Label(search_borrower_win, text = 'Borrower ID: ')
    borrower_id_label.grid(row = 1, column = 0)
    borrower_name_label = Label(search_borrower_win, text = 'Borrower Name: ')
    borrower_name_label.grid(row = 2, column = 0)

    search_btn = Button(search_borrower_win, text ='Search', command = lambda: submit_search_borrowers(search_borrower_win, borrower_id.get(), borrower_name.get()))
    search_btn.grid(row = 3, column = 1)

    global output_label
    output_label = Label(search_borrower_win, text = '')
    output_label.grid(row = 4, column = 0, columnspan = 2)


def submit_search_borrowers(borrower_win, borrower_id, borrower_name):
    
    query = "SELECT b.card_no AS 'Borrower ID', b.name AS 'Borrower Name', CASE WHEN bl.date_returned > bl.due_date THEN ('$' || CAST(ROUND((julianday(bl.date_returned) - julianday(bl.due_date)) * lb.LateFee, 2) AS DECIMAL(10,2))) ELSE '$0.00' END AS 'Late Fee' FROM Book_Loans bl JOIN Borrower b ON bl.card_no = b.card_no JOIN library_branch lb ON bl.branch_id = lb.branch_id WHERE 1=1 "

    if borrower_id:
        query += f"AND b.card_no = {borrower_id} "
    if borrower_name:
        query += f"AND b.name LIKE '%{borrower_name}%' "

    query += " ORDER BY CASE WHEN bl.date_returned > bl.due_date THEN (julianday(bl.date_returned) - julianday(bl.due_date)) * lb.LateFee ELSE NULL END DESC;"

    # establish connection
    submit_conn = sqlite3.connect('../LMS.sql')
    submit_cur = submit_conn.cursor()

    # perform query
    submit_cur.execute(query)

    # output table
    output_records = submit_cur.fetchall()
    print_record = ''
    for output_record in output_records:
        print_record += str(("card_no(" + str(output_record[0])) + ") | name(" + str(output_record[1]) + ") | latefee(" + str(output_record[2]) + ") " + '\n')
    
    global output_label
    if output_label != None:
        output_label.destroy()
    output_label = Label(borrower_win, text = print_record)
    output_label.grid(row = 4, column = 0, columnspan = 2)

    # commit changes
    submit_conn.commit()

    # close the DB connection
    submit_conn.close()
