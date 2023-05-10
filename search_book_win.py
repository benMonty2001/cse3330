from tkinter import *
import sqlite3

output_label = None

def create_search_book_win():

    search_book_win = Tk()
    search_book_win.title('Search Books')
    search_book_win.geometry("1000x1000")

    # create text boxes
    book_id = Entry(search_book_win, width=30)
    book_id.grid(row=1, column=1)
    book_title = Entry(search_book_win, width=30)
    book_title.grid(row=2, column=1)

    # create labels
    book_id_label = Label(search_book_win, text='Book ID:')
    book_id_label.grid(row=1, column=0)
    book_title_label = Label(search_book_win, text='Book Title:')
    book_title_label.grid(row=2, column=0)

    # create search button
    search_btn = Button(search_book_win, text='Search', command=lambda: submit_search_books(search_book_win, book_id.get(), book_title.get()))
    search_btn.grid(row=3, column=1)

    # create results label
    global output_label
    output_label = Label(search_book_win, text='')
    output_label.grid(row=4, column=0, columnspan=2)

def submit_search_books(search_book_win, book_id, book_title):
    # set up query
    query = "SELECT b.book_id AS 'Book ID', b.title AS 'Book Title', ba.Author_Name AS 'Author', CASE WHEN bl.date_returned > bl.due_date THEN ('$' || CAST(ROUND((julianday(bl.date_returned) - julianday(bl.due_date)) * lb.LateFee, 2) AS DECIMAL(10,2))) ELSE 'Non-Applicable' END AS 'Late Fee' FROM book b JOIN Book_Authors ba ON b.book_id = ba.book_id LEFT JOIN Book_Loans bl ON b.book_id = bl.book_id JOIN library_branch lb ON bl.branch_id = lb.branch_id WHERE 1=1"

    # add conditions based on user input
    if book_id:
        query += f" AND b.book_id = {book_id}"
    if book_title:
        query += f" AND b.title LIKE '%{book_title}%'"

    # add remaining clauses to the query
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
        print_record += str("book_id(" + str(output_record[0]) + ") | title(" + str(output_record[1]) + ") | author(" + str(output_record[2]) + ") | latefee(" + str(output_record[3]) + ") " + '\n')
    
    global output_label
    if output_label != None:
        output_label.destroy()
    output_label = Label(search_book_win, text=print_record)
    output_label.grid(row=4, column=0, columnspan=2)

    # commit changes
    submit_conn.commit()

    # close the DB connection
    submit_cur.close()
