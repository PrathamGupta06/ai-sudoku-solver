from solver import *
Menu = '''
1. Enter Sudoku Manually
2. Enter Sudoku from File
3. Exit
'''
separator_line = "----------------------------------------"

def validate(row = None, row_number=None, column_number=None, cell_value=None):

    if row_number != None and row_number not in range(1,10):
        print("Invalid row number. Row number must be between 1 and 9")
        return False

    if column_number != None and column_number not in range(1,10):
        print("Invalid column number. Column number must be between 1 and 9")
        return False

    if cell_value != None and cell_value not in range(0,10):
        print("Invalid cell value. Cell value must be between 0 and 9")
        return False

    # Row Checks
    if row != None:
        if len(row) != 9:  # Row length check
            print("The length of the row is not 9")
            return False
        for i in row:
            if i not in "123456789":  # Row character check
                print("All the characters in the row must be numbers")
                return False
        return True
    return False


def validate_row(row):
    if len(row) != 9:
        print("The length of the row is not 9")
        return False
    for i in row:
        if i not in "123456789":
            print("All the characters in the row must be numbers")
            return False
    return True

def modify_sudoku(sudoku_object):
    print('''Please enter the row number, column number and the number you want to change it to separated with spaces.
    For Example:
    If your sudoku is like this:
    0 2 3 4 5 6 7 0 9
    4 5 6 0 8 9 1 2 3
    7 0 9 1 2 3 4 5 6
    2 0 4 0 6 7 8 9 1
    5 0 7 8 9 1 0 3 4
    0 9 1 2 3 4 5 6 0
    3 0 5 6 7 8 9 1 2
    6 7 8 9 0 2 3 0 5
    0 1 2 3 4 5 6 0 0
    
    And you want to change the 0 in the second row and fourth column to 7, then you should enter: 2 4 7
    ''')
    print(separator_line)
    row, column, number = map(int, input("Enter your choice: ").split())
    while validate(row_number=row, column_number=column, cell_value=number) == False:
        row, column, number = map(int, input("Enter your choice: ").split())
    sudoku_object.modify(row, column, number)
    print("Sudoku Modified Successfully")

def solve(sudokuObject):
    start = time.time()  # Start the timer
    sudokuObject.solve()  # Try solving the sudoku
    end = time.time()  # End the timer

    if sudokuObject.is_solved:  # If the sudoku is solved, print the solution
        sudokuObject.display()
        print("Solved in {} seconds, and {} different possibilities were tried.".format(end - start,
                                                                                        sudokuObject.possibilities_tried))
    else:  # If the sudoku is not solved then the given sudoku is unsolvable.
        print("Unsolvable. Took {} seconds, and {} different possibilities were tried.".format(end - start,
                                                                                               sudokuObject.possibilities_tried))

def manual_input():
    print('''Please enter each line of sudoku one by one, with empty blocks as 0s and press enter after each line.
        For example if your row is: 1 2 3 4 5 _ 7 8 9
        Then you should enter: 123450789''')

    print(separator_line)
    sudoku = []
    for i in range(9):
        row = input("Enter row {}: ".format(i + 1))
        while validate_row(row) == False:  # If the row is not valid, keep asking for input
            row = input("Enter row {}: ".format(i + 1))
        sudoku.append(row)  # If the row is valid, append it to the sudoku list

    print("Sudoku Entered Successfully")
    print(separator_line)
    print("1. Show the solution of the sudoku")
    print("2. Enter the Sudoku again")
    print(separator_line)
    choice = int(input("Enter your choice: "))
    if choice == 2: # If the user wants to enter the sudoku again, call the function again
        manual_input()
        return

    # Choice is 1
    sudoku1 = Sudoku(sudoku)
    solve(sudoku1)

def extract_sudoku():
    path = input("Enter the path of the image: ")
    sudokuExtractor  = SudokuExtractor(path)
    sudokuExtractor.extract_sudoku()
    print("Sudoku Extracted Successfully")
    print(separator_line)
    print("Your sudoku is")
    sudokuExtractor.display()
    sudoku = Sudoku(sudokuExtractor.board)
    print(separator_line)
    print("1. Modify the Sudoku")
    print("2. Show the solution of the sudoku")
    print(separator_line)
    choice = int(input("Enter your choice: "))
    if choice == 1:
        modify_sudoku(sudoku)
    print(separator_line)
    solve(sudoku)


if __name__ == "__main__":
    while True:
        # Print the menu and take the choice
        print(separator_line)
        print(Menu)
        print(separator_line)
        choice = int(input("Enter your choice: "))
        print(separator_line)

        # Call the respective function based on the choice
        if choice == 1:
            manual_input()
        elif choice == 2:
            extract_sudoku()
        elif choice == 3:
            exit()
        else:
            print("Invalid Choice")
            continue
