from tkinter import *
import sqlite3

output_label = None

def create_which_books_late_win():
    which_books_late_win = Tk()
    which_books_late_win.title('Which Books Late')
    which_books_late_win.geometry("1000x1000")

    # create text boxes
    due_date_lower_bound_entry = Entry(which_books_late_win, width=30)
    due_date_lower_bound_entry.grid(row=1, column=1)

    due_date_upper_bound_entry = Entry(which_books_late_win, width=30)
    due_date_upper_bound_entry.grid(row=2, column=1)

    # create labels
    due_date_lower_bound_label = Label(which_books_late_win, text='Due Date Lower Bound:')
    due_date_lower_bound_label.grid(row=1, column=0)

    due_date_upper_bound_label = Label(which_books_late_win, text='Due Date Upper Bound:')
    due_date_upper_bound_label.grid(row=2, column=0)

    # create button
    submit_btn = Button(which_books_late_win, text='Search Dates', command=lambda: submit_which_books_late(which_books_late_win, due_date_upper_bound_entry.get(), due_date_lower_bound_entry.get()))
    submit_btn.grid(row=3, column=1)

    global output_label
    output_label = Label(which_books_late_win)
    output_label.grid(row=4, column=1)

def submit_which_books_late(which_books_late_win, due_date_upper_bound, due_date_lower_bound):
    # Check if the input values are not empty
    if not due_date_lower_bound or not due_date_upper_bound:
        return

    # establish connection
    submit_conn = sqlite3.connect('../LMS.sql')
    submit_cur = submit_conn.cursor()

    # perform queries to check due date range
    submit_cur.execute("""  SELECT book_id, branch_id, strftime('%J', date_returned) - strftime('%J', due_date)
                            FROM book_loans
                            WHERE date_returned > due_date
                            AND due_date >= :due_date_lower_bound
                            AND due_date <= :due_date_upper_bound
                            ORDER BY due_date ASC
                        """,
                        {
                            'due_date_lower_bound': due_date_lower_bound,
                            'due_date_upper_bound': due_date_upper_bound
                        })

    # output table
    output_records = submit_cur.fetchall()
    print_record = ''
    for output_record in output_records:
        print_record += str("Book (book_id : " + str(output_record[0]) + ") was returned to its Library (branch_id : " + str(output_record[1]) + ") " + str(output_record[2]) + " day(s) late\n")
    
    global output_label
    if output_label != None:
            output_label.destroy()
    output_label = Label(which_books_late_win, text=print_record)  # create a new label widget
    output_label.grid(row=4, column=1)

    # commit changes
    submit_conn.commit()

    # close the DB connection
    submit_conn.close()
