class Sudoku:
    def __init__(self, board):
        self.board = board
        self.original_board = board.copy()
        self.is_solved = False

    def display(self):
        """Display the sudoku board"""
        print("\n".join([" ".join(str(item) for item in row) for row in self.board]))

    def solve(self):
        """Solves the sudoku board"""
        for row in range(9):  # iterate over the rows and columns to find the first empty cell
            for col in range(9):
                if self.board[row][col] == 0:  # cell is empty
                    for possibility in range(1, 10):  # try all the numbers from 1 to 9
                        if not self.is_valid(row, col, possibility):
                            continue
                        self.board[row][col] = possibility
                        self.solve()  # recursively call the solve function to solve the rest of the board
                        if self.is_solved:  # if the board is solved by this possibility, return
                            return
                        # print("Backtracked, resetting row {} and column {} to *, for possibility {}".format(row,
                        # col, possibility))
                        self.board[row][col] = 0  # Backtrack
                    # print("Unsolvable", row, col, "Backtracking")
                    return
        # print("Solved")
        self.is_solved = True

    def is_valid(self, row, column, value):
        """Check if the number k is valid in the sudoku board"""

        # print("Checking if {} is valid in row {} and column {}".format(k, row, column))
        if value in self.board[row]:
            return False
        for i in range(9):
            if self.board[i][column] == value:
                return False
        for i in range(3):
            for j in range(3):
                if self.board[(row // 3) * 3 + i][(column // 3) * 3 + j] == value:
                    return False
        # print("{} is valid in row {} and column {}".format(value, row, column))
        # self.display()
        return True

    def check_if_solved(self):
        """ Check if the sudoku board is solved. Sets is_solved to True if it is solved """
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return
        self.is_solved = True


if __name__ == "__main__":
    test_boards = [
        [[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]],

        [[3, 1, 6, 5, 7, 8, 4, 9, 2],
         [5, 2, 9, 1, 3, 4, 7, 6, 8],
         [4, 8, 7, 6, 2, 9, 5, 3, 1],
         [2, 6, 3, 0, 1, 5, 9, 8, 7],
         [9, 7, 4, 8, 6, 0, 1, 2, 5],
         [8, 5, 1, 7, 9, 2, 6, 4, 3],
         [1, 3, 8, 0, 4, 7, 2, 0, 6],
         [6, 9, 2, 3, 5, 1, 8, 7, 4],
         [7, 4, 5, 0, 8, 6, 3, 1, 0]]

    ]

    board1 = test_boards[1]  # Change this to test different boards

    sudoku1 = Sudoku(board1)
    sudoku1.solve()
    if sudoku1.is_solved:
        sudoku1.display()
    else:
        print("Unsolvable")
