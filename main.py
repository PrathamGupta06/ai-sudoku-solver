class Sudoku:
    def __init__(self, n):
        # Create a n x n sudoku board
        self.board = [["*" for i in range(n)] for j in range(n)]

    def __str__(self):
        # Print the sudoku board
        return "\n".join([" ".join(row) for row in self.board])

    def solve(self):
        # Solve the sudoku board
        pass

if __name__ == "__main__":
    # Create a 9 x 9 sudoku board
    sudoku = Sudoku(9)
    print(sudoku)
