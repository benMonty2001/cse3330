from tkinter import *
import sqlite3

output_label = None

def create_book_loan_win():
    #create window
    book_loan_win = Tk()
    book_loan_win.title('Add Book_Loan')
    book_loan_win.geometry("1450x1000")

    #gui components

    # create text boxes
    book_id = Entry(book_loan_win, width = 30)
    book_id.grid(row = 1, column = 1)
    branch_id = Entry(book_loan_win, width = 30)
    branch_id.grid(row = 2, column = 1)
    card_no = Entry(book_loan_win, width = 30)
    card_no.grid(row = 3, column = 1)
    date_out = Entry(book_loan_win, width = 30)
    date_out.grid(row = 4, column = 1)
    due_date = Entry(book_loan_win, width = 30)
    due_date.grid(row = 5, column = 1)
    date_returned = Entry(book_loan_win, width = 30)
    date_returned.grid(row = 6, column = 1)

    #create labels
    book_id_label = Label(book_loan_win, text = 'book_id: ')
    book_id_label.grid(row = 1, column = 0)
    branch_id_label = Label(book_loan_win, text = 'branch_id: ')
    branch_id_label.grid(row = 2, column = 0)
    card_no_label = Label(book_loan_win, text = 'card_no: ')
    card_no_label.grid(row = 3, column = 0)
    date_out_label = Label(book_loan_win, text = 'date_out: ')
    date_out_label.grid(row = 4, column = 0)
    due_date_label = Label(book_loan_win, text = 'due_date: ')
    due_date_label.grid(row = 5, column = 0)
    date_returned_label = Label(book_loan_win, text = 'date_returned')
    date_returned_label.grid(row = 6, column = 0)
    submit_btn = Button(book_loan_win, text ='Add Book_Loan', command = lambda: submit_book_loan(book_loan_win, book_id.get(), branch_id.get(), card_no.get(), date_out.get(), due_date.get(), date_returned.get()))
    submit_btn.grid(row = 7, column = 1)

    global output_label  # access the global label widget
    output_label = Label(book_loan_win)
    output_label.grid(row = 10, column = 2, padx = 80)

def submit_book_loan(book_loan_win, book_id, branch_id, card_no, date_out, due_date, date_returned):
    #submit book_loan
    if not book_id or not branch_id or not card_no or not date_out or not due_date:
        return

    book_loans_table_label = Label(book_loan_win, text = '')
    book_loans_table_label.grid(row = 9, column = 0)

    book_copies_table_label = Label(book_loan_win, text = '')
    book_copies_table_label.grid(row = 9, column = 1)

    #establish connection
    submit_conn = sqlite3.connect('../LMS.sql')
    submit_cur = submit_conn.cursor()

    #perform query
    submit_cur.execute("INSERT INTO book_loans VALUES(:book_id, :branch_id, :card_no, :date_out, :due_date, :date_returned, :is_late)",
    {
        'book_id': book_id,
        'branch_id': branch_id,
        'card_no': card_no,
        'date_out': date_out,
        'due_date': due_date,
        'date_returned': date_returned,
        'is_late': '0'
    })

    #update book_copies table
    submit_cur.execute("UPDATE Book_Copies SET No_Of_Copies = No_Of_Copies - 1 WHERE book_id = ? AND branch_id = ?", (book_id, branch_id))


    #output book_loan_table
    book_loans_table_title = Label(book_loan_win, text = 'Book Loans Table')
    book_loans_table_title.grid(row = 9, column = 1)
    submit_cur.execute("SELECT * FROM Book_Loans")
    output_records = submit_cur.fetchall()
    print_record = ''
    for output_record in output_records:
        print_record += str("book_id(" + str(output_record[0]) + ") | branch_id(" + str(output_record[1]) + ") | card_no(" + str(output_record[2]) + ") | date_out(" + str(output_record[3]) + ") | due_date(" + str(output_record[4]) + ") | date_returned(" + str(output_record[5]) + ") | is_late(" + str(output_record[6]) + ')\n')
    book_loans_table_label = Label(book_loan_win, text = print_record)
    book_loans_table_label.grid(row = 10, column = 1)

    #output book_copies_table
    book_table_title = Label(book_loan_win, text = 'Book Copies Table')
    book_table_title.grid(row = 9, column = 2)
    submit_cur.execute("SELECT * FROM Book_Copies")
    output_records = submit_cur.fetchall()
    print_record = ''
    for output_record in output_records:
        print_record += str("book_id(" + str(output_record[0]) + ") | branch_id(" + str(output_record[1]) + ") | No_Of_Copies(" + str(output_record[2]) + ')\n')
    global output_label
    if output_label != None:
        output_label.destroy()
    output_label = Label(book_loan_win, text = print_record)
    output_label.grid(row = 10, column = 2, padx = 80)

    #commit changes
    submit_conn.commit()

    #close the DB connection
    submit_conn.close()
