from tkinter import *
import sqlite3
import ast

output_label = None

def create_book_win():
    book_win = Tk()
    book_win.title('Add Book')
    book_win.geometry("1000x1000")

    #gui components
    # create text boxes
    title = Entry(book_win, width=30)
    title.grid(row=1, column=1)

    publisher = Entry(book_win, width=30)
    publisher.grid(row=2, column=1)

    author = Entry(book_win, width=30)
    author.grid(row=3, column=1)

    #create labels
    title_label = Label(book_win, text='Title:')
    title_label.grid(row=1, column=0)

    publisher_label = Label(book_win, text='Publisher:')
    publisher_label.grid(row=2, column=0)

    author_label = Label(book_win, text='Author:')
    author_label.grid(row=3, column=0)

    #create button
    submit_btn = Button(book_win, text='Add Book', command=lambda: submit_book(book_win, title.get(), publisher.get(), author.get()))
    submit_btn.grid(row=4, column=1)

    global output_label
    output_label = Label(book_win)
    output_label.grid(row=9, column=1)

def submit_book(book_win, title, publisher_name, author_name):
    # Check if the input values are not empty
    if not title or not publisher_name or not author_name:
        return

    #establish connection
    submit_conn = sqlite3.connect('../LMS.sql')
    submit_cur = submit_conn.cursor()

    #the new book's book_id = num_books + 1
    book_id = submit_cur.execute("SELECT count(*) from book").fetchone()[0] + 1


    #perform queries to add book, author, and copies
    submit_cur.execute("INSERT INTO book (book_id, title, publisher_name) VALUES (:book_id, :title, :publisher_name) ",
    {
    'book_id': book_id,
    'title': title,
    'publisher_name': publisher_name
    })

    submit_cur.execute("INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name) VALUES (:Book_Id, :Author_Name) ",
    {
    'Book_Id': book_id,
    'Author_Name': author_name
    })

    # Query branch_id values from LIBRARY_BRANCH table
    submit_cur.execute("SELECT branch_id FROM library_branch")
    branch_ids = submit_cur.fetchall()

    # Loop over all book_id and branch_id combinations, and insert No_Of_Copies = 5
    for branch_id_as_tuple in branch_ids:
        branch_id, = branch_id_as_tuple
        submit_cur.execute("INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies) VALUES (:book_id, :branch_id, :no_of_copies)", 
        {
        'book_id' : str(book_id),
        'branch_id' : str(branch_id),
        'no_of_copies' : '5'
        })

    #output table

    submit_cur.execute("SELECT bc.branch_id, b.book_id, b.title, b.publisher_name, ba.Author_Name, bc.No_Of_Copies FROM book b JOIN BOOK_AUTHORS ba ON b.book_id = ba.Book_Id JOIN BOOK_COPIES bc ON bc.book_id = b.book_id")
    output_records = submit_cur.fetchall()
    print_record = ''
    for output_record in output_records:
        print_record += str("branch_id (" + str(output_record[0]) + ") | book_id(" + str(output_record[1]) + ") | " + str(output_record[2]) + " | " + str(output_record[3]) + "|" + str(output_record[4]) + " | No_Of_Copies(" + str(output_record[5]) + ')\n')
    global output_label
    if output_label != None:
            output_label.destroy()
    output_label = Label(book_win, text = print_record)
    output_label.grid(row = 9, column = 1)


    #commit changes
    submit_conn.commit()

    #close the DB connection
    submit_conn.close()
