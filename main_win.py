from tkinter import *

from book_loan_win import *
from borrower_win import *
from book_win import *
from loan_details_win import *
from which_books_late_win import *
from search_book_win import *
from search_borrower_win import *

import sqlite3

#create window
main_win = Tk()
main_win.title('Library Management System (LMS)')
main_win.geometry("400x400")

# (1) book_loan_win
init_book_loan_win_btn = Button(main_win, text = '1. Add Book_Loan', command = create_book_loan_win)
init_book_loan_win_btn.grid(row = 0, column = 0, padx = 120, pady = 15)

# (2) borrower_win
init_borrower_win_btn = Button(main_win, text ='2. Add Borrower', command = create_borrower_win)
init_borrower_win_btn.grid(row = 1, column = 0, padx = 120)

# (3) book_win
init_book_win_btn = Button(main_win, text ='3. Add Book', command = create_book_win)
init_book_win_btn.grid(row = 2, column = 0, padx = 120, pady = 15)

# (4) loan_details_win
init_book_loan_details_win_btn = Button(main_win, text ='4. Check Num_Loaned', command = create_loan_details_win)
init_book_loan_details_win_btn.grid(row = 3, column = 0, padx = 120)

# (5) check_due_date_win
init_which_books_late_win_btn = Button(main_win, text ='5. Which_Books_Late', command = create_which_books_late_win)
init_which_books_late_win_btn.grid(row = 4, column = 0, padx = 120, pady = 15)

# (6.a) search_borrower_win
init_search_borrower_win_btn = Button(main_win, text ='6_a. Search Borrower', command = create_search_borrower_win)
init_search_borrower_win_btn.grid(row = 5, column = 0, padx = 120, pady = 15)

# (6.b) search_book_win
init_search_book_win_btn = Button(main_win, text ='6_b. Search Book', command = create_search_book_win)
init_search_book_win_btn.grid(row = 6, column = 0, padx = 120)

#evoke loop
main_win.mainloop()
