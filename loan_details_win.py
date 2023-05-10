from tkinter import *
import sqlite3

output_label = None

def create_loan_details_win():
	
    loan_details_win = Tk()
    loan_details_win.title('Check Num Loaned')
    loan_details_win.geometry("1000x1000")

	#gui components
	# create text boxes
    book_title = Entry(loan_details_win, width = 30)
    book_title.grid(row = 1, column = 1)

	#create labels
    book_title_label = Label(loan_details_win, text = 'Book Title:')
    book_title_label.grid(row=1, column=0)

    # results label
    result_label = Label(loan_details_win, text = '')
    result_label.grid(row = 3, column = 0, columnspan = 2)
	
	#create button
    submit_btn = Button(loan_details_win, text = 'List Details', command = lambda: submit_loan_details(loan_details_win, book_title.get()))
    submit_btn.grid(row = 2, column = 1, columnspan = 2)

    global output_label 
    output_label = Label(loan_details_win)
    output_label.grid(row = 3, column = 0, columnspan = 2)

def submit_loan_details(loan_details_win, book_title):
    # Check if the input values are not empty
    if not book_title:
        return

    #establish connection
    submit_conn = sqlite3.connect('../LMS.sql')
    submit_cur = submit_conn.cursor()

    #perform query
    submit_cur.execute("SELECT library_branch.branch_name, library_branch.branch_id, COUNT(*) FROM (library_branch NATURAL JOIN book_loans) NATURAL JOIN book_copies NATURAL JOIN book WHERE book.title = ? GROUP BY library_branch.branch_id", (book_title,))
    
    #output table
    output_records = submit_cur.fetchall()
    print_record = ''
    if len(output_records) == 0:
        print_record = "That book has not been loaned out anywhere!\n"
    for output_record in output_records:
        if output_record[2] == 1:
            print_record += str(str(output_record[0]) + ", branch_id(" + str(output_record[1]) + "), has loaned out " + str(output_record[2]) + ' copy\n')
        else:
            print_record += str(str(output_record[0]) + ", branch_id(" + str(output_record[1]) + "), has loaned out " + str(output_record[2]) + ' copies\n')
    global output_label
    if output_label != None:
            output_label.destroy()
    output_label = Label(loan_details_win, text = print_record)
    output_label.grid(row = 3, column = 0, columnspan = 2)

    #commit changes
    submit_conn.commit()

    #close the DB connection
    submit_conn.close()

    
