print("Importing Libraries...")  # noqa
import os
import time
from _solver import Sudoku, SudokuExtractor

# ----------------- Global Program Constants -----------------
Menu = '''
  MAIN MENU
  
1. Enter Sudoku Manually
2. Enter Sudoku from an Image

9. Exit
'''
hr = "----------------------------------------"


# ----------------- Helper Functions -----------------
def is_valid(row=None, row_number=None, column_number=None, cell_value=None, path=None):
    """This function is used for validation of the input"""
    # @param row: The row that is to be validated
    # @type row: str
    # @param row_number: The row number that is to be validated
    # @type row_number: int
    # @param column_number: The column number that is to be validated
    # @type column_number: int
    # @param cell_value: The cell value that is to be validated
    # @type cell_value: int
    # @return: True if the input is valid, False otherwise

    if row_number is not None and row_number not in range(1, 10):
        print("Invalid row number. Row number must be between 1 and 9")
        return False

    if column_number is not None and column_number not in range(1, 10):
        print("Invalid column number. Column number must be between 1 and 9")
        return False

    if cell_value is not None and cell_value not in range(0, 10):
        print("Invalid cell value. Cell value must be between 0 and 9")
        return False

    # Row Checks
    if row is not None:
        if len(row) != 9:  # Row length check
            print("The length of the row is not 9")
            return False
        for i in row:
            if i not in "0123456789":  # Row character check
                print("All the characters in the row must be digits")
                return False
        return True

    if path is not None:
        if not os.path.exists(path):
            print("The path does not exist")
            return False
        return True

    return True  # If the function is called withou any arguments, then return True


def modify_sudoku(sudoku_object):
    """This function allows the user to modify the sudoku"""
    # @param sudoku_object: The sudoku object that is to be modified
    # @type sudoku_object: Sudoku
    # @return: None

    print('''Please enter the row number, column number and the number you want to change it to separated with spaces.
For Example:
If your sudoku is like this:

0 2 3 | 4 5 6 | 7 0 9 
4 5 6 | 0 8 9 | 1 2 3 
7 0 9 | 1 2 3 | 4 5 6 
------|-------|------
2 0 4 | 0 6 7 | 8 9 1 
5 0 7 | 8 9 1 | 0 3 4 
0 9 1 | 2 3 4 | 5 6 0 
------|-------|------
3 0 5 | 6 7 8 | 9 1 2 
6 7 8 | 9 0 2 | 3 0 5 
0 1 2 | 3 4 5 | 6 0 0

And you want to change the 0 in the second row and fourth column to 7, then you should enter: 2 4 7 (with spaces)
If you want to cancel the modification, enter: 0 0 0 (with spaces)''')

    print(hr)

    print("Current Sudoku:")  # Print the current sudoku
    sudoku_object.display()
    print(hr)

    # Get the input from the user
    row, column, number = map(int, input("Enter your choice (row_number column_number cell_value): ").strip().split())
    # If the user wants to cancel the modification, return
    if row == 0 and column == 0 and number == 0:
        return
    # If the input is not valid, keep asking for input
    while not is_valid(row_number=row, column_number=column, cell_value=number):
        row, column, number = map(int, input("Enter your choice: ").strip().split())
        if row == 0 and column == 0 and number == 0:
            return
    # At this point, the input is valid. Change the cell value
    sudoku_object.modify(row, column, number)
    print("Sudoku Modified Successfully")
    print("New Sudoku:")
    sudoku_object.display()


def solve(sudoku_object):
    """This function solves the sudoku"""
    # @param sudoku_object: The sudoku object that is to be solved
    # @type sudoku_object: Sudoku
    # @return: None

    start = time.time()  # Start the timer
    sudoku_object.solve()  # Try solving the sudoku
    end = time.time()  # End the timer

    if sudoku_object.is_solved:  # If the sudoku is solved, print the solution
        sudoku_object.display()
        print("Solved in {} seconds, and {} different possibilities were tried.".format(end - start,
                                                                                        sudoku_object.possibilities_tried))  # noqa
    else:  # If the sudoku is not solved then the given sudoku is unsolvable.
        print("Unsolvable. Took {} seconds, and {} different possibilities were tried.".format(end - start,
                                                                                               sudoku_object.possibilities_tried))  # noqa


# ----------------- Main Functions -----------------
def manual_input():
    """This function allows the user to enter the sudoku manually"""
    # @return: None

    print('''Please enter each line of sudoku one by one, with empty blocks as 0s and press enter after each line.
        For example if your row is: 1 2 3 4 5 _ 7 8 9
        Then you should enter: 123450789''')

    print(hr)
    sudoku = []  # The sudoku that is to be solved
    for i in range(9):
        row = input("Enter row {}: ".format(i + 1))
        while not is_valid(row=row):  # If the row is not valid, keep asking for input
            row = input("Enter row {}: ".format(i + 1))
        # If the row is valid, append it to the sudoku list by converting it to a list of integers
        sudoku.append([int(x) for x in row])

    print("Sudoku Entered Successfully", hr, sep="\n")

    sudoku_object = Sudoku(sudoku)  # Create a sudoku object
    print("Current Sudoku:")  # Print the current sudoku
    sudoku_object.display()
    # Menu for the user to choose what to do with the sudoku
    print("1. Show the solution of the sudoku", "2. Modify the sudoku", "9. Exit to main menu", hr, sep="\n")
    choice = int(input("Enter your choice: "))

    while choice == 2:  # If the user wants to modify the sudoku, call the modify_sudoku function
        modify_sudoku(sudoku_object)

        # Print Menu
        print("1. Show the solution of the sudoku", "2. Modify the sudoku", "9. Exit to main menu", hr, sep="\n")
        choice = int(input("Enter your choice: "))

    if choice == 9:  # If the user wants to exit to the main menu, return
        return

    # Choice is 1
    solve(sudoku_object)


def extract_sudoku():
    """This function extracts the sudoku from the file"""
    # @return: None

    # Taking the path of the image from the user and validation
    path = input("Enter the path of the image: ")
    while not is_valid(path=path):
        print("Invalid Path")
        path = input("Enter the path of the image: ")

    sudoku_extractor = SudokuExtractor(path)

    start = time.time()  # Start the timer
    sudoku_extractor.extract_sudoku()
    end = time.time()  # End the timer
    print("Sudoku Extracted Successfully and it took {} seconds to extract the sudoku".format(end-start), hr, sep="\n")
    print("Your sudoku is")
    sudoku_extractor.display()

    sudoku_object = Sudoku(sudoku_extractor.board)  # Create a sudoku object from the extracted sudoku

    # Menu for the user to choose what to do with the sudoku
    print(hr, "1. Modify the Sudoku", "2. Show the solution of the sudoku", "", "9. Exit to main menu",
          hr, sep="\n")

    choice = int(input("Enter your choice: "))
    print(hr)
    while choice == 1:  # If the user wants to modify the sudoku
        modify_sudoku(sudoku_object)  # Call the modify_sudoku function
        # Print the menu again
        print(hr, "1. Modify the Sudoku", "2. Show the solution of the sudoku", "", "9. Exit to main menu",
              hr, sep="\n")
        choice = int(input("Enter your choice: "))
        print(hr)

    print(hr, "Solving the Sudoku", sep="\n")
    solve(sudoku_object)  # Call the solve function


if __name__ == "__main__":
    while True:
        # Print the menu and take the choice
        print(hr)
        print(Menu)
        print(hr)
        choice = int(input("Enter your choice: "))
        print(hr)

        # Call the respective function based on the choice
        if choice == 1:
            manual_input()
        elif choice == 2:
            extract_sudoku()
        elif choice == 9:
            exit()
        else:
            print("Invalid Choice, Please type 1, 2 or 3")
            continue
